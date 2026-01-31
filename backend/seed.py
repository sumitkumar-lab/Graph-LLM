import os
import time
from langchain_community.graphs import Neo4jGraph
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Neo4jVector
from dotenv import load_dotenv
import os

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

def seed_database():
    print("🌱 Checking database state...")
    
    url=NEO4J_URI
    username=NEO4J_USERNAME
    password=NEO4J_PASSWORD

    # Retry logic (same as before)
    graph = None
    for i in range(10):
        try:
            graph = Neo4jGraph(url=url, username=username, password=password)
            graph.query("RETURN 1")
            print("✅ Connected to Neo4j.")
            break
        except Exception as e:
            print(f"⏳ Database not ready... retrying ({i+1}/10)")
            time.sleep(5)
    
    if not graph:
        print("Could not connect to Neo4j")
        return

    # Check if empty
    result = graph.query("MATCH (n) RETURN count(n) as count")
    if result[0]['count'] > 0:
        print("✨ Database already seeded.")
        return

    print("🚜 Seeding Data & Creating Vectors...")

    # 1. Create the Graph Structure (Nodes & Edges)
    seed_query = """
    MERGE (alice:Person {name: "Alice", role: "Sr. Engineer"})
    MERGE (bob:Person {name: "Bob", role: "Product Manager"})
    
    MERGE (payment_service:Service {name: "Payment Gateway API", description: "Handles all money transactions, credit card processing, and refunds."})
    MERGE (auth_service:Service {name: "Auth Service", description: "Manages user login, tokens, and security sessions."})

    MERGE (doc1:Document {title: "Migration Plan", text: "We are moving the money handling system to Stripe.", date: "2023-10-01"})
    
    MERGE (alice)-[:MAINTAINS]->(payment_service)
    MERGE (bob)-[:WROTE]->(doc1)
    MERGE (doc1)-[:DESCRIBES]->(payment_service)
    """
    graph.query(seed_query)

    # 2. CREATE VECTOR INDEX (The "Hybrid" Upgrade)
    # This reads the 'text' and 'description' properties, converts them to vectors using HuggingFace,
    # and stores them back in Neo4j.
    
    print("🧠 Generating Embeddings (This uses your CPU, might take a moment)...")
    
    # Free, high-quality embeddings model
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # Index the 'Service' nodes so we can search them by meaning
    Neo4jVector.from_existing_graph(
        embedding=embeddings,
        url=url,
        username=username,
        password=password,
        index_name="service_index",
        node_label="Service",
        text_node_properties=["name", "description"], # What we search against
        embedding_node_property="embedding"
    )

    # Index the 'Document' nodes
    Neo4jVector.from_existing_graph(
        embedding=embeddings,
        url=url,
        username=username,
        password=password,
        index_name="document_index",
        node_label="Document",
        text_node_properties=["title", "text"],
        embedding_node_property="embedding"
    )

    print("🌳 Database seeded & Vectorized successfully!")

if __name__ == "__main__":
    seed_database()