import json
from qdrant_client import QdrantClient, models
from sentence_transformers import SentenceTransformer

client = QdrantClient(url="http://localhost:6333")
model_name = "sentence-transformers/all-MiniLM-L6-v2"

# Load embedding model
model = SentenceTransformer(model_name)

# ------------------------------------------------------
# Load JSON
# ------------------------------------------------------
# with open("ace_react/playbook.json", "r") as f:
#     data = json.load(f)

# bullets = data["bullets"]

# if not bullets:
#     raise ValueError("No bullets found in playbook.json")

# vectors = []
# ids = []
# payloads = []

# # Embed all documents
# for idx, (key, item) in enumerate(bullets.items(), start=1):
#     text = item["content"]
#     section = item["section"]

#     vec = model.encode(text).tolist()

#     ids.append(idx)
#     payloads.append({
#         "text": text,
#         "section": section,
#         "original_id": item["id"]
#     })
#     vectors.append(vec)

# # ------------------------------------------------------
# # Create collection
# # ------------------------------------------------------
# try:
#     client.create_collection(
#         "agent3_collection",
#         vectors_config=models.VectorParams(
#             size=len(vectors[0]),
#             distance=models.Distance.COSINE
#         )
#     )
#     print("Collection created!")
# except Exception as e:
#     if "already exists" in str(e).lower():
#         print("Collection already exists!")
#     else:
#         raise

# # ------------------------------------------------------
# # Upload data using upsert for idempotency
# # ------------------------------------------------------
# client.upsert(
#     collection_name="agent3_collection",
#     points=models.Batch(
#         ids=ids,
#         vectors=vectors,
#         payloads=payloads
#     )
# )

# print(f"Uploaded {len(bullets)} bullets from playbook.json!")

# ------------------------------------------------------
# Query function
# ------------------------------------------------------
def ask(query, limit=5):
    vec = model.encode(query).tolist()

    result = client.query_points(
        collection_name="agent3_collection",
        query=vec,
        limit=limit
    )

    print(f"\nQuery: {query}\n")
    for p in result.points:
        score = getattr(p, 'score', 'N/A')
        print(p.payload['text'])
    
    print(result)
    return result
