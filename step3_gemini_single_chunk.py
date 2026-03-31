from google import genai
import json

# 🔑 Gemini setup
API_KEY = "YOUR GEMINI API KEY"
client = genai.Client(api_key=API_KEY)

MODEL = "models/gemini-2.5-flash"

# ---- load chunk from file (SAFE) ----
with open("neo4j_python/chunk_sample.txt", "r", encoding="utf-8") as f:
    chunk_text = f.read()

print("✅ Chunk loaded")
print("📏 Characters:", len(chunk_text))

prompt = f"""
You are a knowledge graph extraction engine.

STRICT SCHEMA

Allowed node types:
- Chapter
- Topic
- Concept

Allowed relationships:
- Chapter HAS_TOPIC Topic
- Topic HAS_CONCEPT Concept

Rules:
- Output ONLY valid JSON
- No markdown
- No explanations
- No extra text

JSON format:

{{
  "entities": [
    {{ "type": "", "name": "" }}
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
{chunk_text}
>>>
"""

response = client.models.generate_content(
    model=MODEL,
    contents=prompt
)

# ---- validate JSON ----
try:
    data = json.loads(response.text)
    print("✅ Gemini JSON parsed successfully\n")
    print(json.dumps(data, indent=2))
except json.JSONDecodeError:
    print("❌ Invalid JSON output\n")
    print(response.text)
