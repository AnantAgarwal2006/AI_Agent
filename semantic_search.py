import os
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)
def get_embedding(text):
    response=client.embeddings.create(
        model=os.getenv("EMBED_MODEL"),
        input=text
    )
    return response.data[0].embedding

def cosine_similarity(A,B):
    dot_prod=np.dot(A,B)
    norm_a=np.linalg.norm(A)
    norm_b=np.linalg.norm(B)
    return dot_prod/(norm_a *norm_b)

text1="Python is a good programming language"
text2="Python is used to write code snippets"
text3="I do not eat apples"

embedding1=get_embedding(text1)
embedding2=get_embedding(text2)
embedding3=get_embedding(text3)

similarity12=cosine_similarity(embedding1,embedding2)
similarity13=cosine_similarity(embedding1,embedding3)

print("Similarity between text1 and text2 :",f"{similarity12:.2f}")
print("Similarity between text1 and text2 :",f"{similarity13:.2f}")