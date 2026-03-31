from neo4j import GraphDatabase

# ---- Neo4j connection ----
NEO4J_URI = "YOUR NEO4J URI"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "YOUR NEO4J PASS"

driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USER, NEO4J_PASSWORD)
)

# ---- Normalized KG (paste output from Step 4 here) ----
KG = {
  "entities": [
    {
      "id": "Chapter:Chapter_20:_Communication_systems",
      "type": "Chapter",
      "name": "Chapter 20: Communication systems"
    },
    {
      "id": "Topic:Discovering_radioactivity",
      "type": "Topic",
      "name": "Discovering radioactivity"
    }
  ],
  "relationships": [
    {
      "from_id": "Chapter:Chapter_20:_Communication_systems",
      "to_id": "Topic:Discovering_radioactivity",
      "relation": "HAS_TOPIC"
    }
  ]
}

def ingest(tx, kg):
    # ---- create nodes ----
    for e in kg["entities"]:
        tx.run(
            f"""
            MERGE (n:{e['type']} {{id: $id}})
            SET n.name = $name
            """,
            id=e["id"],
            name=e["name"]
        )

    # ---- create relationships ----
    for r in kg["relationships"]:
        tx.run(
            f"""
            MATCH (a {{id: $from_id}})
            MATCH (b {{id: $to_id}})
            MERGE (a)-[rel:{r['relation']}]->(b)
            """,
            from_id=r["from_id"],
            to_id=r["to_id"]
        )

with driver.session() as session:
    session.execute_write(ingest, KG)

driver.close()
print("✅ KG ingested into Neo4j successfully")
