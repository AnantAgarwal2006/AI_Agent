import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)
response=client.embeddings.create(
    model=os.getenv("EMBED_MODEL"),
    input=["I am a good boy","Python is a good language","he ia a good coder"]
)
for i ,emb in enumerate(response.data):
    print(f"Embeddings {i} length: {len(emb.embedding)}")

