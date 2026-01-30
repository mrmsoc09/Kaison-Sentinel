from kai11.core.redact import redact_text


def test_redact_password_pattern():
    text = "user=alice password=secret"
    red = redact_text(text)
    assert "secret" not in red
    assert "[REDACTED]" in red
