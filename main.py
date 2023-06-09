import jwt
import os
import pinecone

from fastapi import FastAPI, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Dict

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
JWT_EXPIRATION_TIME_MINUTES = 30
ORIGINS = ['*']
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()


class PineconeQuery(BaseModel):
    namespace: str | None = None
    top_k: int = 10
    include_values: bool = False
    include_metadata: bool = False
    vector: List[float] | None = None
    sparse_vector: Dict[str, List[float]] | None = None
    filter: Dict[str, Dict[str, List[str]]] | None = None


@app.get("/_status")
def read_root():
    return {"status": "ok"}


# AUTH ROUTES
@app.post("/query")
async def protected_endpoint(credentials: HTTPAuthorizationCredentials = Depends(security),
                             pinecone_query: PineconeQuery = None):
    try:
        payload = jwt.decode(credentials.credentials, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        username = payload.get("username")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.DecodeError:
        raise HTTPException(status_code=401, detail="Invalid token")

    try:
        pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)
        index = pinecone.Index(PINECONE_INDEX_NAME)

        query_response = index.query(
            **pinecone_query.dict()
        )

        return [
            {"id": obj.id, "score": obj.score, "values": obj.values}
            for obj in query_response.matches
        ]
    except pinecone.exceptions.PineconeException as e:
        raise HTTPException(status_code=500, detail="System error")
