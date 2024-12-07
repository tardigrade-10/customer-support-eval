import numpy as np
from openai import OpenAI, AsyncOpenAI
import os
import dotenv

dotenv.load_dotenv()

client = OpenAI(
    project=os.environ.get("PROJECT_ID"),
    api_key=os.environ.get("OPENAI_API_KEY")
)

aclient = AsyncOpenAI(
    project=os.environ.get("PROJECT_ID"),
    api_key=os.environ.get("OPENAI_API_KEY")
)


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


async def get_embedding_async(text: str, model="text-embedding-3-small", **kwargs):
    # replace newlines, which can negatively affect performance.
    text = text.replace("\n", " ")

    response = await aclient.embeddings.create(input=[text], model=model, **kwargs)

    return response.data[0].embedding

def get_embedding(text: str, model="text-embedding-3-small", **kwargs):
    # replace newlines, which can negatively affect performance.
    text = text.replace("\n", " ")

    response = client.embeddings.create(input=[text], model=model, **kwargs)

    return response.data[0].embedding
