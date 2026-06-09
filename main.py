import os
import hashlib
import time
from contextlib import asynccontextmanager
from collections import defaultdict

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from cachetools import TTLCache
from dotenv import load_dotenv

from embedding import vectorload
from retriever import get_retriever
from chain import build_chain, ask

load_dotenv()


CHROMA_DIR        = "chroma_db"
CACHE_TTL_SECONDS = 600          # cached answer expires after 10 min
CACHE_MAX_SIZE    = 500          # max unique questions cached
RATE_LIMIT_MAX    = 5           # max requests per window per user
RATE_LIMIT_WINDOW = 60           # window size in seconds

ALLOWED_ORIGINS = [
    "http://localhost:3000",     # Next.js dev
    "https://yourdomain.com",    # production — replace this
]

# ─── App state ────────────────────────────────────────────────────────────────

# response cache: key = hash(ragcookie + question), value = answer string
response_cache: TTLCache = TTLCache(maxsize=CACHE_MAX_SIZE, ttl=CACHE_TTL_SECONDS)

# rate limit tracker: key = ragcookie value, value = list of request timestamps
rate_tracker: dict[str, list[float]] = defaultdict(list)

# RAG components (populated at startup)
rag_chain = None


# ─── Lifespan ─────────────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    global rag_chain
    vectorstore = vectorload(CHROMA_DIR)
    retriever   = get_retriever(vectorstore)
    rag_chain   = build_chain(retriever)
    print("RAG pipeline ready.")
    yield
    print("Shutting down.")


# ─── FastAPI app ──────────────────────────────────────────────────────────────

app = FastAPI(lifespan=lifespan)

# ─── CORS ─────────────────────────────────────────────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,       # required for cookies to pass through
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── Helpers ──────────────────────────────────────────────────────────────────

def get_user_id(request: Request) -> str:
    """Read ragcookie sent by Next.js. 403 if missing."""
    user_id = request.cookies.get("ragcookie")
    if not user_id:
        raise HTTPException(status_code=403, detail="Missing ragcookie.")
    return user_id


def check_rate_limit(user_id: str) -> None:
    """Sliding window rate limiter keyed on ragcookie value."""
    now        = time.time()
    window_start = now - RATE_LIMIT_WINDOW
    timestamps = rate_tracker[user_id]

    # drop timestamps outside the current window
    rate_tracker[user_id] = [t for t in timestamps if t > window_start]

    if len(rate_tracker[user_id]) >= RATE_LIMIT_MAX:
        oldest = rate_tracker[user_id][0]
        retry_after = int(RATE_LIMIT_WINDOW - (now - oldest)) + 1
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded. Retry after {retry_after}s.",
            headers={"Retry-After": str(retry_after)},
        )

    rate_tracker[user_id].append(now)


def make_cache_key(user_id: str, question: str) -> str:
    """Cache key = hash of (ragcookie + normalized question)."""
    raw = f"{user_id}::{question.strip().lower()}"
    return hashlib.sha256(raw.encode()).hexdigest()


# ─── Schema ───────────────────────────────────────────────────────────────────

class QueryRequest(BaseModel):
    question: str


# ─── Routes ───────────────────────────────────────────────────────────────────

@app.post("/query")
async def query(payload: QueryRequest, request: Request):
    user_id = get_user_id(request)
    check_rate_limit(user_id)

    cache_key = make_cache_key(user_id, payload.question)

    if cache_key in response_cache:
        return JSONResponse({
            "answer": response_cache[cache_key],
            "cached": True,
        })

    answer = ask(rag_chain, payload.question)
    response_cache[cache_key] = answer

    return JSONResponse({
        "answer": answer,
        "cached": False,
    })


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "cache_size": len(response_cache),
        "tracked_users": len(rate_tracker),
    }


@app.delete("/cache")
async def flush_cache(request: Request):
    get_user_id(request)        # still requires a valid ragcookie
    response_cache.clear()
    rate_tracker.clear()
    return {"detail": "Cache and rate tracker flushed."}