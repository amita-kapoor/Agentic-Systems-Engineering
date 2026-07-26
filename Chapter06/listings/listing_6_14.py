def _mock_llm(system: str, user: str, want_json: bool) -> str:
    """Deterministic stand-in for an LLM. Returns plausible shapes, not smart answers."""
    seed = hashlib.sha256((system + user).encode()).hexdigest()

    if not want_json:
        return f"[mock-llm] response keyed on {seed[:8]}"

    # Detect what kind of JSON the caller wants from cues in the prompt
    if "draft a compliance report" in user.lower() or "draft a report" in user.lower():
        return json.dumps(
            {
                "summary": "The product processes customer payment data.",
                "clauses": [
                    {"id": "REG-1", "claim": "Encrypts data at rest.", "evidence": "uses AES-256"},
                    {"id": "REG-2", "claim": "Logs access events.", "evidence": "audit log"},
                ],
                "open_issues": [],
            }
        )

    if "critique" in user.lower() or "evaluate" in user.lower():
        # Alternate between needs_revision and acceptable so the loop terminates
        status = "needs_revision" if seed[0] in "0123456789ab" else "acceptable"
        return json.dumps(
            {
                "status": status,
                "issues": ["missing cross-reference for REG-3"]
                if status == "needs_revision"
                else [],
                "feedback": "Add an explicit reference to clause REG-3 on data retention.",
            }
        )

    return json.dumps({"result": f"mock-{seed[:8]}"})


def llm_call(
    system: str, user: str, schema: Optional[dict] = None, temperature: float = 0.2
) -> Any:
    """Single entry point for all model calls in this notebook."""
    want_json = schema is not None

    if not USE_REAL_LLM:
        text = _mock_llm(system, user, want_json)
    else:
        from openai import OpenAI

        client = OpenAI(api_key=OPENAI_API_KEY)
        kwargs = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "temperature": temperature,
        }
        if want_json:
            kwargs["response_format"] = {"type": "json_object"}
        resp = client.chat.completions.create(**kwargs)
        text = resp.choices[0].message.content

    if want_json:
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return {"_raw": text, "_parse_error": True}

    return text


print(llm_call("you are a test", "say hi", schema=None))  # Smoke test
