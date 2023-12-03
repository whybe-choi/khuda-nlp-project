import os
from typing import Dict

from chains import (
    analyze_query_chain,
    consult_chain,
    review_chain,
    extract_keywords_chain,
    read_prompt_template,
)
from database import query_db
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

load_dotenv()


app = FastAPI()


class UserRequest(BaseModel):
    user_message: str


CUR_DIR = os.path.dirname(os.path.abspath(__file__))
ANALYZE_QUERY_PROMPT_TEMPLATE = os.path.join(CUR_DIR, "prompt_templates", "analyze_query.txt")

@app.post("/qna")
def gernerate_answer(req: UserRequest) -> Dict[str, str]:
    context = req.dict()
    context["input"] = context["user_message"]
    context["query_list"] = analyze_query_chain.run(context)
    context["consult_list"] = consult_chain.run(context)
    context["keyword_list"] = extract_keywords_chain.run(context)
    context["related_info"] = query_db(context["keyword_list"])
    answer = review_chain.run(context)

    return {"answer": answer}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)