from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from example1 import chain

class QueryInput (BaseModel):
    question: str
    stream: bool = False

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    # allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

    )
@app.post('/ask')
def handle_question(input: QueryInput):
    try:
        if input.stream:
            response = chain.stream(input.stream)
            return StreamingResponse(response)
        else:
            response = chain.invoke(input.question)
            return JSONResponse(content=response)   
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    