import json
import random
import time
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, List

from .config import OUTPUT_DIR
from .hardware import hardware_profile
from .programs import list_programs


def _clamp(value: int, low: int, high: int) -> int:
    return max(low, min(high, value))


def _tier_factor(tier: str) -> float:
    return {"economy": 0.6, "standard": 1.0, "max": 1.4}.get(tier, 1.0)


def _stealth_factor(level: str) -> float:
    return {"high": 0.6, "standard": 1.0, "low": 1.2}.get(level, 1.0)


def compute_scan_profile(scope: Dict[str, Any], options: Dict[str, Any]) -> Dict[str, Any]:
    hw = hardware_profile()
    tier = scope.get("budget_tier") or options.get("budget_default_tier", "standard")
    budget_presets = options.get("budget_presets", {})
    preset = budget_presets.get(tier, {})
    daily_budget = scope.get("daily_budget_usd") or preset.get("daily_budget_usd") or 25
    stealth = scope.get("stealth") or preset.get("stealth") or options.get("stealth_default", "standard")

    base_parallel = max(1, min(int(hw.get("cpu_count", 2)), int((hw.get("mem_total_gb", 4) or 4) / 2)))
    parallel = int(base_parallel * _tier_factor(tier) * _stealth_factor(stealth))
    cap = int(preset.get("max_parallel_cap") or base_parallel)
    max_parallel = _clamp(parallel, 1, max(1, cap))

    duration_days = int(scope.get("scan_duration_days") or options.get("scan_duration_days", 42))
    swap_window_days = int(options.get("swap_window_days", 14))
    pool_size_min = int(options.get("pool_size_min", 50))
    pool_size_max = int(options.get("pool_size_max", 500))
    pool_size = int(scope.get("scan_pool_size") or max(pool_size_min, max_parallel * 25))
    pool_size = _clamp(pool_size, pool_size_min, pool_size_max)
    active_limit = int(scope.get("max_active_scans") or max(1, min(max_parallel, pool_size // 10 or 1)))

    return {
        "budget_tier": tier,
        "daily_budget_usd": float(daily_budget),
        "stealth": stealth,
        "duration_days": duration_days,
        "swap_window_days": swap_window_days,
        "pool_size": pool_size,
        "active_limit": active_limit,
        "max_parallel": max_parallel,
        "hardware": hw,
    }


def build_scan_pool(profile: Dict[str, Any]) -> Dict[str, Any]:
    programs = [p for p in list_programs() if p.get("public", True)]
    now = datetime.now(timezone.utc)
    pool_end = now + timedelta(days=int(profile["duration_days"]))
    swap_until = now + timedelta(days=int(profile["swap_window_days"]))
    ids = [p.get("id") for p in programs if p.get("id")]
    seed = int(time.time() // 86400)
    rng = random.Random(seed)
    if len(ids) <= profile["pool_size"]:
        pool = ids
    else:
        pool = rng.sample(ids, profile["pool_size"])
    active = pool[: profile["active_limit"]]
    return {
        "pool_programs": pool,
        "active_programs": active,
        "pool_size": profile["pool_size"],
        "active_limit": profile["active_limit"],
        "duration_days": profile["duration_days"],
        "swap_window_days": profile["swap_window_days"],
        "pool_start": now.isoformat(),
        "pool_end": pool_end.isoformat(),
        "swap_allowed_until": swap_until.isoformat(),
        "swap_policy": "High-confidence opportunities may replace active slots during swap window.",
        "program_count": len(ids),
    }


def write_scan_plan(run_id: str, profile: Dict[str, Any], pool: Dict[str, Any]) -> str:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_DIR / f"{run_id}_scan_plan.json"
    payload = {"scan_profile": profile, "scan_pool": pool}
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2))
    return str(path)


def build_scan_plan(scope: Dict[str, Any], options: Dict[str, Any], run_id: str) -> Dict[str, Any]:
    profile = compute_scan_profile(scope, options)
    pool = build_scan_pool(profile)
    path = write_scan_plan(run_id, profile, pool)
    return {"scan_profile": profile, "scan_pool": pool, "scan_plan_path": path}
