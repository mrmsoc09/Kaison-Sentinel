#include <string>
#include <vector>

static const char* TECHNIQUE_ID = "T1562.001";
static const char* TACTIC_ID = "TA0005";
static const char* TECHNIQUE_NAME = "Impair Defenses: Disable or Modify Tools";

static std::vector<std::string> safe_steps() {
    return {
        "Verify scope authorization and approvals.",
        "Inventory security controls from read-only sources.",
        "Review telemetry for unexpected service stops or policy tampering.",
        "Confirm integrity signals (config drift, checksum mismatch).",
        "Package evidence for HiL validation and reporting."
    };
}

// NOTE: This file is a defensive assessment profile only.
// It must not disable or modify security tools.
