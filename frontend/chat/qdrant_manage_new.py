import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    PayloadSchemaType,
    Filter,
    FieldCondition,
    MatchValue
)

import uuid
from datetime import datetime
from qdrant_client.models import PointStruct
from chat.embeddings import get_embedding_chat, get_embedding_knowledge
from langchain_core.tools import tool

load_dotenv()

qdrant_url = os.getenv("QDRANT_URL")

if not qdrant_url:
    raise ValueError("QDRANT_URL belum diisi di .env")

if "localhost" in qdrant_url:
    qdrant = QdrantClient(url=qdrant_url)
else:
    qdrant = QdrantClient(
        url=qdrant_url,
        api_key=os.getenv("QDRANT_CLOUD_API")
    )

    print("QDRANT_URL RAW:", repr(os.getenv("QDRANT_URL")))

VECTOR_SIZE = 384


def create_collections():

    collections = [
        "knowledge_base",
        "memory_chat"
    ]

    existing = [
        c.name
        for c in qdrant.get_collections().collections
    ]

    for collection in collections:

        if collection not in existing:

            qdrant.create_collection(
                collection_name=collection,

                vectors_config=VectorParams(
                    size=VECTOR_SIZE,
                    distance=Distance.COSINE
                )
            )

            print(
                f"{collection} berhasil dibuat"
            )

        else:

            print(
                f"{collection} sudah ada"
            )

def save_chat(
    session_id,
    role,
    content
):

    vector = get_embedding_chat(content)

    qdrant.upsert(
        collection_name="memory_chat",
        points=[
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={
                    "session_id": session_id,
                    "role": role,
                    "content": content,
                    "timestamp": datetime.now().isoformat()
                }
            )
        ]
    )

def create_payload_indexes():

    try:

        qdrant.create_payload_index(
            collection_name="memory_chat",
            field_name="session_id",
            field_schema=PayloadSchemaType.KEYWORD
        )

        print("Index session_id dibuat")

    except Exception as e:

        print(e)

def load_knowledge_to_qdrant(documents,collection_name="knowledge_base",batch_size=50):
    points = []
    total = 0

    for i, doc in enumerate(documents):

        # embedding
        vector = get_embedding_knowledge(doc["page_content"])

        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={
                    "text": doc["page_content"],
                    **doc["metadata"]
                }
            )
        )

        total += 1
        #upload perbatch
        if len(points) >= batch_size:
            qdrant.upsert(
                collection_name=collection_name,
                points=points
            )
            print(f"Uploaded batch: {len(points)} vectors")
            points = []
    #upload sisa data
    if points:
        qdrant.upsert(
            collection_name=collection_name,
            points=points
        )
        print(f"Uploaded final batch: {len(points)} vectors")

    print(f"DONE - Total uploaded: {total} vectors")
    
def retrieve_chat_memory(session_id):
    """
    Retrieve user profile and conversation memory.
    """

    points, _ = qdrant.scroll(

        collection_name="memory_chat",

        scroll_filter=Filter(
            must=[
                FieldCondition(
                    key="session_id",

                    match=MatchValue(
                        value=str(session_id)
                    )
                )
            ]
        ),

        limit=1000,

        with_payload=True,

        with_vectors=False
    )

    points = sorted(
        points,
        key=lambda x: x.payload["timestamp"]
    )

    return points

@tool
def retrieve_knowledge(query, collection_name="knowledge_base", limit=5):
    """
    Retrieve health and nutrition information from knowledge base.
    """
    vector = get_embedding_knowledge(query)

    results = qdrant.query_points(
        collection_name=collection_name,
        query=vector,
        limit=limit
    )

    docs = []

    for point in results.points:
        payload = point.payload
        docs.append(payload.get("text", ""))

    return docs

print(qdrant.get_collections())
print("Collection siap")