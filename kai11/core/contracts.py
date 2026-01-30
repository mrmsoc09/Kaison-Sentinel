from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime

@dataclass
class EvidenceRef:
    kind: str
    path: str
    hash_sha256: Optional[str] = None

@dataclass
class MitigationBlock:
    tier: str  # minimal | standard | deep
    dry_run_cmds: List[str]
    apply_cmds: List[str]
    verify_steps: List[str]
    rollback_steps: List[str]
    rotation_steps: List[str] = field(default_factory=list)
    cloud_cmds: Dict[str, List[str]] = field(default_factory=dict)  # gcp/aws/azure/cloudflare
    code_fix: Optional[str] = None

@dataclass
class Finding:
    id: str
    title: str
    severity: str
    confidence: float
    target: str
    evidence: List[EvidenceRef]
    status: str  # hypothesis | signal | likely | validated | invalid
    signals: int = 1
    reportability: float = 0.0
    duplicate_risk: str = "low"
    duplicate_matches: int = 0
    duplicate_validated: int = 0
    mitigation: Optional[MitigationBlock] = None
    intel_state: str = "raw"
    scope_match: bool = True
    freshness: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    labels: List[str] = field(default_factory=list)
    repro_steps: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

@dataclass
class Approval:
    required: bool
    approved: bool
    approver: Optional[str] = None
    approved_at: Optional[str] = None

@dataclass
class RunRecord:
    run_id: str
    mode: str
    scope: Dict
    plan: Dict
    approvals: Approval
    findings: List[Finding] = field(default_factory=list)
    evidence_bundle: List[EvidenceRef] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
