from typing import List

from .contracts import Finding, EvidenceRef
from .cve_store import extract_cve_ids, find_cve_by_id, load_cve_store


def enrich_findings_with_cve(findings: List[Finding]) -> List[Finding]:
    store = load_cve_store()
    if not store:
        return findings
    for f in findings:
        ids = set(extract_cve_ids(f.title))
        for label in f.labels:
            ids.update(extract_cve_ids(label))
        if not ids:
            continue
        for cve_id in ids:
            record = find_cve_by_id(cve_id, store)
            if not record:
                continue
            if cve_id not in f.labels:
                f.labels.append(cve_id)
            f.evidence.append(EvidenceRef(kind="cve", path=f"outputs/cve_store.jsonl#{cve_id}"))
            # Adjust confidence slightly if CVSS is high
            cvss = record.get("cvss") or 0
            if isinstance(cvss, (int, float)) and cvss >= 7:
                f.confidence = min(1.0, f.confidence + 0.1)
    return findings
