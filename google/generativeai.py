"""Lightweight stub of `google.generativeai` for local tests.

This provides `configure(api_key)` and a minimal `GenerativeModel` with a
`generate_content(prompt)` method that returns an object with a `text`
attribute containing JSON. It's intentionally simple: for CI/tests we don't
invoke real Gemini.
"""
import json

def configure(api_key=None):
    # No-op for tests
    return None

class GenerativeModel:
    def __init__(self, model_name="gemini-2.5-pro"):
        self.model_name = model_name

    def generate_content(self, prompt):
        # Return a minimal parseable JSON response with empty matches.
        class Resp:
            def __init__(self, text):
                self.text = text
        resp_text = json.dumps({"matches": []})
        return Resp(resp_text)
