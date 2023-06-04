import jwt
import os
import pinecone

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

app = FastAPI()

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
JWT_EXPIRATION_TIME_MINUTES = 30

security = HTTPBearer()


@app.get("/_status")
def read_root():
    return {"status": "ok"}


# AUTH ROUTES
@app.post("/query")
async def protected_endpoint(credentials: HTTPAuthorizationCredentials = Depends(security), query: str = None):
    try:
        payload = jwt.decode(credentials.credentials, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        username = payload.get("username")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.DecodeError:
        raise HTTPException(status_code=401, detail="Invalid token")

    pinecone.init(api_key="YOUR_API_KEY", environment="YOUR_ENVIRONMENT")
    index = pinecone.Index("example-index")

    query_response = index.query(
        namespace="example-namespace",
        top_k=10,
        include_values=True,
        include_metadata=True,
        vector=[0.1, 0.2, 0.3, 0.4],
        sparse_vector={
            'indices': [10, 45, 16],
            'values': [0.5, 0.5, 0.2]
        },
        filter={
            "genre": {"$in": ["comedy", "documentary", "drama"]}
        }
    )

    return {"message": f"Protected endpoint accessed successfully by {username}"}
