from neo4j import GraphDatabase

NEO4J_URI = "YOU KNOW WHAT TO PUT HERE"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "YOU KNOW WHAT TO PUT HERE"

# 🔹 Paste normalized KG JSON here (from Step 4 output)
NORMALIZED_KG = {
  "entities": [
    {
      "id": "Textbook:Class_11_Physics",
      "type": "Textbook",
      "name": "Class 11 Physics"
    },
    {
      "id": "Chapter:Units_And_Measurements",
      "type": "Chapter",
      "name": "Units And Measurements"
    }
  ],
  "relationships": [
    {
      "from_id": "Textbook:Class_11_Physics",
      "to_id": "Chapter:Units_And_Measurements",
      "relation": "HAS_CHAPTER"
    }
  ]
}

driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USER, NEO4J_PASSWORD)
)

def create_nodes(tx, entities):
    for e in entities:
        tx.run(
            f"""
            MERGE (n:{e['type']} {{id: $id}})
            SET n.name = $name
            """,
            id=e["id"],
            name=e["name"]
        )

def create_relationships(tx, relationships):
    for r in relationships:
        tx.run(
            f"""
            MATCH (a {{id: $from_id}})
            MATCH (b {{id: $to_id}})
            MERGE (a)-[:{r['relation']}]->(b)
            """,
            from_id=r["from_id"],
            to_id=r["to_id"]
        )

with driver.session() as session:
    session.execute_write(create_nodes, NORMALIZED_KG["entities"])
    session.execute_write(create_relationships, NORMALIZED_KG["relationships"])

print("Full Knowledge Graph ingested successfully ✅")

driver.close()
