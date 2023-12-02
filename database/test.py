import os

from dotenv import load_dotenv
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma

load_dotenv()

CUR_DIR = os.path.dirname(os.path.abspath(__file__))

CHROMA_PERSIST_DIR = os.path.join(CUR_DIR, "chroma-persist")
CHROMA_COLLECTION_NAME = "doctor-khu"

if __name__ == "__main__":
    from pprint import pprint

    db = Chroma(
        persist_directory=CHROMA_PERSIST_DIR,
        embedding_function=OpenAIEmbeddings(),
        collection_name=CHROMA_COLLECTION_NAME,
    )

    docs = db.similarity_search("루테인 등의 영양제를 섭취할 때는 과다 섭취를 피하고 필요한 영양소만 섭취해야 합니다. 새우 알러지가 있으므로 알러지 유발 가능성이 있는 영양제는 피해야 합니다.")

    pprint(docs)