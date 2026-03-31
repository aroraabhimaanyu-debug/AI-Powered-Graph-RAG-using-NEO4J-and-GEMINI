from google import genai
import json

API_KEY = "YOUR GEMINI API KEY"

client = genai.Client(api_key=API_KEY)

MODEL = "models/gemini-2.5-flash"

TEXT = """
Units and Measurements is the first chapter of Class 11 Physics.
It introduces SI units.
The metre is the SI unit of length.
"""

prompt = f"""
You are a knowledge graph extraction engine.

Graph schema (STRICT):
Node types allowed:
- Textbook
- Chapter
- Topic
- Definition

Relationships allowed:
- Textbook HAS_CHAPTER Chapter
- Chapter HAS_TOPIC Topic
- Topic HAS_DEFINITION Definition

Rules:
- Use ONLY the above node types
- Use ONLY the above relationships
- Do NOT invent extra nodes or relations
- Output ONLY valid JSON
- No markdown
- No explanations

JSON format EXACTLY:

{{
  "entities": [
    {{
      "type": "Textbook",
      "name": ""
    }}
  ],
  "relationships": [
    {{
      "from": "",
      "from_type": "",
      "to": "",
      "to_type": "",
      "relation": ""
    }}
  ]
}}

Text:
<<<
{TEXT}
>>>
"""

response = client.models.generate_content(
    model=MODEL,
    contents=prompt
)

# Validate JSON
try:
    data = json.loads(response.text)
    print("KG extraction JSON parsed successfully ✅")
    print(json.dumps(data, indent=2))
except json.JSONDecodeError:
    print("❌ Invalid JSON output")
    print(response.text)
