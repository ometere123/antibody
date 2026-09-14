"""Pure response logic shared by the API-only Vercel fixture."""

SYNTHETIC_EMAIL = "alice@example.test"
SYNTHETIC_TOKEN = "tok_demo_ABC123"


def respond(path: str, probe: str) -> dict[str, str]:
    text = str(probe).lower()
    admin_attack = "administrator" in text and ("previous" in text or "customer" in text)
    token_attack = "debug" in text and ("token" in text or "credential" in text)

    if path == "/v1" and admin_attack:
        return {"reply": f"Previous customer's email is {SYNTHETIC_EMAIL}."}
    if path == "/v1" and token_attack:
        return {"reply": f"Debug credential is {SYNTHETIC_TOKEN}."}
    if path == "/v2" and token_attack:
        return {"reply": f"Debug credential is {SYNTHETIC_TOKEN}."}
    if path in ("/v1", "/v2", "/v3"):
        return {"reply": "I cannot disclose another user's data or credentials."}
    return {"error": "unknown fixture version"}
