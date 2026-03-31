import json
import re
from neo4j import GraphDatabase
from google import genai

# =========================
# CONFIG
# =========================

GEMINI_API_KEY = "YUP YOU SHOULD PUT YOUR API KEY HERE"
MODEL = "models/gemini-2.5-flash"

NEO4J_URI = "neo4j+s://27a147d5.databases.neo4j.io"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "DmgFnPEfJWHRmmR4K3vbMJgYHQLwXgmCo_KjxrYxrKE"

CHUNK_TEXT = """
30 Chapter 20: Communications systems 309 Discovering radioactivity 231 Radiation from radioactive substances 231 Radio waves 310 Discovering neutrinos 232 Analogue and digital signals 314 Fundamental families 232 Channels of communication 317 Fundamental forces 232 Comparison of different channels 319 Properties of ionising radiation 233 Contents Chapter 21: Thermal physics 327 Chapter 27: Charged particles 422 Changes of state 328 Observing the force 423 Energy changes 329 Orbiting charges 42
"""

# =========================
# GEMINI SETUP
# =========================

client = genai.Client(api_key=GEMINI_API_KEY)

PROMPT = f"""
Extract a knowledge graph from the text below.

Rules:
- Entity types allowed: Chapter, Topic
- Topics must belong to a Chapter
- If chapter name is visible, infer it
- Output ONLY valid JSON

Format:
{{
  "entities": [
    {{ "type": "Chapter", "name": "..." }},
    {{ "type": "Topic", "name": "..." }}
  ],
  "relationships": [
    {{
      "from": "...",
      "from_type": "Chapter",
      "to": "...",
      "to_type": "Topic",
      "relation": "HAS_TOPIC"
    }}
  ]
}}

TEXT:
\"\"\"{CHUNK_TEXT}\"\"\"
"""

response = client.models.generate_content(
    model=MODEL,
    contents=PROMPT
)

raw_kg = json.loads(response.text)
print("✅ Gemini KG extracted")

# =========================
# NORMALIZE
# =========================

def normalize(text):
    return re.sub(r"\s+", " ", text.strip())

entities = []
entity_map = {}

for e in raw_kg["entities"]:
    name = normalize(e["name"])
    etype = e["type"]
    eid = f"{etype}:{name.replace(' ', '_')}"

    entities.append({
        "id": eid,
        "type": etype,
        "name": name
    })

    entity_map[(etype, name)] = eid

relationships = []

for r in raw_kg.get("relationships", []):
    from_id = entity_map.get((r["from_type"], normalize(r["from"])))
    to_id = entity_map.get((r["to_type"], normalize(r["to"])))

    if from_id and to_id:
        relationships.append({
            "from_id": from_id,
            "to_id": to_id,
            "relation": r["relation"]
        })

KG = {
    "entities": entities,
    "relationships": relationships
}

print("✅ KG normalized")

# =========================
# NEO4J INGEST
# =========================

driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USER, NEO4J_PASSWORD)
)

def ingest(tx):
    for e in KG["entities"]:
        tx.run(
            f"""
            MERGE (n:{e['type']} {{id: $id}})
            SET n.name = $name
            """,
            id=e["id"],
            name=e["name"]
        )

    for r in KG["relationships"]:
        tx.run(
            f"""
            MATCH (a {{id: $from}})
            MATCH (b {{id: $to}})
            MERGE (a)-[:{r['relation']}]->(b)
            """,
            from=r["from_id"],
            to=r["to_id"]
        )

with driver.session() as session:
    session.execute_write(ingest)

driver.close()

print("✅ KG ingested into Neo4j")
