from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from app.services.langchain_service import get_answer

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:9000",
        "http://127.0.0.1:9000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuestionRequest(BaseModel):
    question: str

@app.post("/get-answer")
async def get_answer_from_llm(request: QuestionRequest):
    print(f"Received question: {request.question}")
    try:
        answer = get_answer(request.question)
        print(f"LLM answer: {answer}")
        if not answer:
            return {"error": "No answer returned from LLM."}
        return {"answer": answer}
    except Exception as e:
        print(f"Error while getting answer: {e}")
        return {"error": str(e)}

@app.get("/test-cors")
def test_cors():
    return {"message": "CORS working!"}
