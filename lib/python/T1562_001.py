TECHNIQUE_ID = "T1562.001"
TACTIC_ID = "TA0005"
TECHNIQUE_NAME = "Impair Defenses: Disable or Modify Tools"

SAFE_PROFILE = {
    "objective": "Assess potential impairment of defenses without altering target state.",
    "risk": "high",
    "steps": [
        "Verify scope authorization and approvals.",
        "Inventory security controls (EDR/AV/agents) from read-only sources.",
        "Review telemetry for unexpected service stops or policy tampering.",
        "Confirm integrity signals (config drift, policy checksum mismatch).",
        "Package evidence for HiL validation and reporting.",
    ],
    "do_not": [
        "Do not disable or modify security tools.",
        "Do not attempt evasion or bypass behaviors.",
    ],
}


def get_assessment_profile():
    return SAFE_PROFILE.copy()
