from kai11.core.policy_engine import allowed


def test_policy_denies_vuln_execute_for_analyst():
    assert allowed("analyst", "execute", "vuln", "medium") is False


def test_policy_allows_plan_for_operator():
    assert allowed("operator", "plan", "osint", "low") is True
