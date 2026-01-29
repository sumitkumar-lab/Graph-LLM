import os
import time
from langchain_community.graphs import Neo4jGraph

def seed_database():
    print("🌱 Checking database state...")
    
    # 1. Connection Config (pulled from env vars)
    url = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
    username = os.environ.get("NEO4J_USERNAME", "neo4j")
    password = os.environ.get("NEO4J_PASSWORD", "password123")

    # 2. Retry Logic (Wait for DB to start)
    graph = None
    for i in range(10):
        try:
            graph = Neo4jGraph(url=url, username=username, password=password)
            graph.query("RETURN 1") # Test connection
            print("✅ Connected to Neo4j.")
            break
        except Exception as e:
            print(f"⏳ Database not ready... retrying ({i+1}/10)")
            time.sleep(5)
    
    if not graph:
        print("❌ Could not connect to Neo4j after retries.")
        return

    # 3. Check if empty
    result = graph.query("MATCH (n) RETURN count(n) as count")
    count = result[0]['count']
    
    if count > 0:
        print(f"✨ Database already contains {count} nodes. Skipping seed.")
        return

    # 4. The Seed Data (The "Company Knowledge")
    print("🚜 Database empty. Seeding data...")
    seed_query = """
    MERGE (alice:Person {name: "Alice", role: "Sr. Engineer", email: "alice@nexus.ai"})
    MERGE (bob:Person {name: "Bob", role: "Product Manager", email: "bob@nexus.ai"})
    MERGE (charlie:Person {name: "Charlie", role: "DevOps", email: "charlie@nexus.ai"})

    MERGE (payment_service:Service {name: "Payment Gateway API", status: "Active"})
    MERGE (auth_service:Service {name: "Auth Service", status: "Deprecated"})

    MERGE (doc1:Document {title: "Payment Migration Plan", date: "2023-10-01", url: "/wiki/pay-mig"})
    MERGE (doc2:Document {title: "Incident Report 505", date: "2023-11-15", url: "/jira/505"})
    MERGE (doc3:Document {title: "API V2 Specs", date: "2024-01-20", url: "/wiki/api-v2"})

    # Relationships
    MERGE (alice)-[:MAINTAINS]->(payment_service)
    MERGE (charlie)-[:MAINTAINS]->(auth_service)
    MERGE (bob)-[:WROTE]->(doc1)
    MERGE (doc1)-[:DESCRIBES]->(payment_service)
    MERGE (alice)-[:RESOLVED]->(doc2)
    MERGE (doc2)-[:AFFECTED]->(auth_service)
    MERGE (charlie)-[:REVIEWED]->(doc3)
    MERGE (doc3)-[:REPLACES]->(doc1)
    """
    
    graph.query(seed_query)
    graph.refresh_schema() # Important: Tell LangChain the schema changed
    print("🌳 Database seeded successfully!")

if __name__ == "__main__":
    seed_database()