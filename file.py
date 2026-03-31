from neo4j import GraphDatabase

# -----------------------------
# UPDATE THESE WITH YOUR VALUES
# -----------------------------
NEO4J_URI = "YOUR NEO4J URL"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "YOUR NEO4J PASSWORD"

class Neo4jClient:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            NEO4J_URI,
            auth=(NEO4J_USER, NEO4J_PASSWORD)
        )

    def close(self):
        self.driver.close()

    def test_connection(self):
        with self.driver.session() as session:
            result = session.run("RETURN 'Neo4j connected!' AS msg")
            return result.single()["msg"]


if __name__ == "__main__":
    client = Neo4jClient()
    print(client.test_connection())
    client.close()
