import os
from google import genai


class LLMFallback:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

    def classify_and_extract(self, transcript: str):

        prompt = f"""
You are an intent classifier.

Allowed intents:
- check_run_status
- list_projects
- list_runs
- greeting

Extract:
- intent
- slots (which, project, detail, run_name)

Return ONLY valid JSON like:

{{
  "intent": "intent_name",
  "slots": {{
      "which": "...",
      "project": "...",
      "detail": "...",
      "run_name": "..."
  }}
}}

User input:
"{transcript}"
"""

        response = self.client.models.generate_content(
            model="models/gemini-2.5-flash",
            contents=prompt
        )

        return response.text


llm_fallback = LLMFallback()