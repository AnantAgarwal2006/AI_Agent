import os
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

EMBED_MODEL = os.getenv("EMBED_MODEL")
KB_FOLDER = os.getenv("KB_FOLDER")


# get the embedding of the text from the embedding model
def get_embedding(text):
    response = client.embeddings.create(
        model=EMBED_MODEL,
        input=text
    )
    return response.data[0].embedding


# cosine similarity
def cosine_similarity(A, B):
    dot_prod = np.dot(A, B)
    norm_a = np.linalg.norm(A)
    norm_b = np.linalg.norm(B)

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot_prod / (norm_a * norm_b)


# load the documents
def load_documents(folder=KB_FOLDER):
    documents = []

    for filename in sorted(os.listdir(folder)):
        if not filename.endswith(".txt"):
            continue

        path = os.path.join(folder, filename)

        with open(path, "r", encoding="utf-8") as f:
            documents.append(
                {
                    "source": filename,
                    "text": f.read()
                }
            )

    return documents


# add embeddings in the documents
def add_embeddings(documents):
    for document in documents:
        vector = get_embedding(document["text"])
        document["vector"] = vector

    return documents


# search method to search top_k documents
def search(query, documents, top_k=3):

    query_vector = get_embedding(query)

    results = []

    for document in documents:

        score = cosine_similarity(
            query_vector,
            document["vector"]
        )

        results.append(
            {
                "score": float(score),
                "source": document["source"],
                "text": document["text"],
                "size": len(document["text"])
            }
        )


    results.sort(
        key=lambda rec: rec["score"],
        reverse=True
    )

    return results[:top_k]


# testing method
def test(user_query, documents, top_k=3):

    print(f"\nUser Query: {user_query}\n")

    results = search(user_query, documents, top_k)

    for r in results:
        print(
            f"{r['score']:.2f} - {r['source']} - {r['size']} characters"
        )

        print(r["text"][:200])
        print("-"*50)



# start testing

documents = load_documents()

documents = add_embeddings(documents)

print(f"We have embedded {len(documents)} documents")


user_query = "How many days i will get for maternity leave"


test(user_query, documents, 3)