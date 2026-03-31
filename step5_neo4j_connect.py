from neo4j import GraphDatabase

NEO4J_URI = "YOUR NEO4J UR"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "YOUR NEO4J PASS"

driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USER, NEO4J_PASSWORD)
)

with driver.session() as session:
    session.run(
        """
        MERGE (t:Textbook {id: $id})
        SET t.name = $name
        """,
        {
            "id": "Textbook:Class_11_Physics",
            "name": "Class 11 Physics"
        }
    )

print("Neo4j connection + MERGE successful ✅")

driver.close()
