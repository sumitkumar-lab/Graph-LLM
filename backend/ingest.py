from langchain_neo4j import Neo4jGraph
from dotenv import load_dotenv
import os

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

if not all([NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD]):
    raise RuntimeError("Neo4j credentials are missing from environment variables")


graph = Neo4jGraph(
    url=NEO4J_URI,
    username=NEO4J_USERNAME,
    password=NEO4J_PASSWORD,
)

seed_query = """
MERGE (alice:Person {id: "person_alice"})
SET alice.name = "Alice", alice.role = "Sr. Engineer"

MERGE (bob:Person {id: "person_bob"})
SET bob.name = "Bob", bob.role = "Product Manager"

MERGE (payment:Service {id: "svc_payment"})
SET payment.name = "Payment Gateway API"

MERGE (auth:Service {id: "svc_auth"})
SET auth.name = "Auth Service"

MERGE (doc1:Document {id: "doc_payment_migration"})
SET doc1.title = "Payment Migration Plan", doc1.date = "2023-10-01"

MERGE (doc2:Document {id: "doc_incident_505"})
SET doc2.title = "Incident Report 505", doc2.date = "2023-11-15"

MERGE (alice)-[:MAINTAINS]->(payment)
MERGE (bob)-[:WROTE]->(doc1)
MERGE (doc1)-[:DESCRIBES]->(payment)
MERGE (alice)-[:RESOLVED]->(doc2)
MERGE (doc2)-[:AFFECTED]->(auth)
"""

graph.query(seed_query)
print("Graph populated successfully.")
