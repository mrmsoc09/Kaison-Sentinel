package mitre

type AssessmentProfile struct {
	TechniqueID   string
	TacticID      string
	TechniqueName string
	Objective     string
	Risk          string
	Steps         []string
	DoNot         []string
}

func T1562_001_Profile() AssessmentProfile {
	return AssessmentProfile{
		TechniqueID:   "T1562.001",
		TacticID:      "TA0005",
		TechniqueName: "Impair Defenses: Disable or Modify Tools",
		Objective:     "Assess potential impairment of defenses without altering target state.",
		Risk:          "high",
		Steps: []string{
			"Verify scope authorization and approvals.",
			"Inventory security controls from read-only sources.",
			"Review telemetry for unexpected service stops or policy tampering.",
			"Confirm integrity signals (config drift, checksum mismatch).",
			"Package evidence for HiL validation and reporting.",
		},
		DoNot: []string{
			"Do not disable or modify security tools.",
			"Do not attempt evasion or bypass behaviors.",
		},
	}
}
