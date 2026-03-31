from google import genai
import json

API_KEY = "YOUR GEMINI API KEY"

client = genai.Client(api_key=API_KEY)

MODEL = "models/gemini-2.5-flash"

prompt = """
You are a knowledge graph extraction engine.

Rules:
- Output ONLY valid JSON
- No markdown
- No explanations
- No extra text

Return JSON in EXACTLY this format:

{
  "entities": [
    {
      "type": "Chapter",
      "name": "Units and Measurements"
    }
  ],
  "relationships": []
}
"""

response = client.models.generate_content(
    model=MODEL,
    contents=prompt
)

# Validate JSON (important)
try:
    data = json.loads(response.text)
    print("JSON parsed successfully ✅")
    print(json.dumps(data, indent=2))
except json.JSONDecodeError as e:
    print("❌ Invalid JSON")
    print(response.text)
