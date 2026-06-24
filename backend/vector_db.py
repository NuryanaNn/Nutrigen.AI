from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from sentence_transformers import SentenceTransformer
from qdrant_client.models import SearchRequest, VectorParams
from qdrant_client.models import QueryRequest
import sqlite3
import os

# =========================
# CONFIG
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "nutrition.db")

client = QdrantClient("localhost", port=6333)

COLLECTION_NAME = "nutrigen_foods"

# embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


# =========================
# CREATE COLLECTION
# =========================
def create_collection():
    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=384,
            distance=Distance.COSINE
        )
    )
    print("✅ Collection created:", COLLECTION_NAME)


# =========================
# LOAD DATA SQLITE → QDRANT
# =========================
def load_data_to_qdrant():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM foods")
    rows = cursor.fetchall()

    if not rows:
        print("❌ Tidak ada data di SQLite")
        return

    points = []

    for i, r in enumerate(rows):
        # r = (id, calories, proteins, fat, carbohydrate, name, image)

        text = (
            f"{r[5]} "
            f"kalori {r[1]} "
            f"protein {r[2]} "
            f"lemak {r[3]} "
            f"karbo {r[4]}"
        )

        vector = model.encode(text).tolist()

        points.append(
            PointStruct(
                id=i,
                vector=vector,
                payload={
                    "name": r[5],
                    "calories": r[1],
                    "proteins": r[2],
                    "fat": r[3],
                    "carbohydrate": r[4],
                    "image": r[6]
                }
            )
        )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )

    conn.close()

    print(f"✅ {len(points)} data berhasil masuk ke Qdrant")


# =========================
# SEMANTIC SEARCH (RAG CORE)
# =========================
def search_food(query, limit=5):
    query_vector = model.encode(query).tolist()

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=limit,
        with_payload=True
    )

    return results.points