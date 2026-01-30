pub const TECHNIQUE_ID: &str = "T1562.001";
pub const TACTIC_ID: &str = "TA0005";
pub const TECHNIQUE_NAME: &str = "Impair Defenses: Disable or Modify Tools";

pub fn safe_steps() -> Vec<&'static str> {
    vec![
        "Verify scope authorization and approvals.",
        "Inventory security controls from read-only sources.",
        "Review telemetry for unexpected service stops or policy tampering.",
        "Confirm integrity signals (config drift, checksum mismatch).",
        "Package evidence for HiL validation and reporting.",
    ]
}

pub fn do_not() -> Vec<&'static str> {
    vec![
        "Do not disable or modify security tools.",
        "Do not attempt evasion or bypass behaviors.",
    ]
}
