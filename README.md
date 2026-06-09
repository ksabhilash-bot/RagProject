# RagProject

A production-ready Retrieval-Augmented Generation (RAG) backend built with FastAPI, LangChain, Google Gemini embeddings, Mistral LLM, and ChromaDB. Designed to answer questions about documents with semantic search and a full API layer including cookie-based rate limiting, TTL response caching, and CORS support.

---

## Tech Stack

| Layer | Technology |
|---|---|
| API framework | FastAPI + Uvicorn |
| LLM | Mistral (`mistral-large-latest`) via `langchain-mistralai` |
| Embeddings | Google Gemini (`gemini-embedding-2`) via `langchain-google-genai` |
| Vector store | ChromaDB (persisted to disk) |
| Orchestration | LangChain (LCEL chain) |
| Caching | `cachetools` TTLCache (server-side, 10 min TTL) |
| Rate limiting | Sliding window keyed on `ragcookie` |
| Package manager | `uv` |
| Deployment | Docker → Render |

---

## Project Structure

```
RagProject/
├── main.py              # FastAPI app — routes, middleware, lifespan
├── chain.py             # LangChain QA chain (Mistral LLM + prompt)
├── retriever.py         # ChromaDB similarity retriever
├── embedding.py         # Gemini embeddings — create & load vectorstore
├── splitter.py          # Document chunking
├── document_loader.py   # PDF / TXT loader
├── ingest.py            # One-time ingestion script
├── config.py            # Pydantic settings (env vars)
├── debug.py             # Manual retrieval testing
├── AKS.txt              # Source document
├── AKS.pdf              # Source document (PDF)
├── chroma_db/           # Persisted vector store (committed for production)
├── Dockerfile
├── .dockerignore
├── requirements.txt
└── .env
```

---

## Local Setup

### Prerequisites

- Python 3.11+
- [`uv`](https://github.com/astral-sh/uv) installed
- Mistral API key — [console.mistral.ai](https://console.mistral.ai)
- Google API key — [aistudio.google.com](https://aistudio.google.com)

### 1. Clone and install

```bash
git clone https://github.com/ksabhilash-bot/RagProject.git
cd RagProject

uv venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux

uv add fastapi "uvicorn[standard]" slowapi cachetools httpx
uv pip install -r requirements.txt
```

### 2. Environment variables

Create a `.env` file in the project root:

```dotenv
MISTRAL_API_KEY="your_mistral_key"
GOOGLE_API_KEY="your_google_key"
FRONTEND_URL="http://localhost:3000"
```

### 3. Ingest documents

Run this once to build the ChromaDB vector store from your source documents:

```bash
uv run ingest.py
```

This creates the `chroma_db/` directory with embedded chunks ready for retrieval.

### 4. Start the server

```bash
uvicorn main:app --reload --port 8000
```

API is live at `http://localhost:8000`. Swagger docs at `http://localhost:8000/docs`.

---

## API Reference

### `POST /query`

Ask a question. Requires a `ragcookie` cookie (set automatically by the Next.js frontend on first request).

**Request**
```json
{ "question": "What are Abhilash's backend skills?" }
```

**Response**
```json
{
  "answer": "Abhilash has experience with FastAPI, PostgreSQL...",
  "cached": false
}
```

**Error responses**

| Status | Reason |
|---|---|
| `403` | Missing `ragcookie` |
| `429` | Rate limit exceeded — includes `Retry-After` header |

---

### `GET /health`

Liveness check. Returns cache and rate tracker stats.

```json
{
  "status": "ok",
  "cache_size": 12,
  "tracked_users": 3
}
```

---

### `DELETE /cache`

Flushes the response cache and rate tracker. Requires a valid `ragcookie`.

```json
{ "detail": "Cache and rate tracker flushed." }
```

---

## Rate Limiting

Sliding window rate limiter — **5 requests per 60 seconds** per user, keyed on the `ragcookie` value. When exceeded, the response includes a `Retry-After` header with the exact number of seconds to wait.

---

## Caching

Server-side TTL cache using `cachetools.TTLCache`. Cache key is `sha256(ragcookie + normalized_question)` — each user gets independent cache entries. Answers expire after **10 minutes**. A `"cached": true` flag in the response indicates a cache hit (no LLM call was made).

---

## RAG Pipeline

```
Question
   ↓
retriever.py  →  ChromaDB similarity search (top 4 chunks)
   ↓
chain.py      →  LangChain LCEL: context + question → Mistral prompt → answer
   ↓
Answer
```

The prompt instructs the model to answer only from the retrieved context. If the answer isn't in the documents, it responds with `"I don't have enough information to answer this."`

---

## Deployment (Render)

The vector store is pre-built locally and committed to the repo — no ingestion runs on the server.

### 1. Push to GitHub

```bash
git add chroma_db/ Dockerfile .dockerignore
git commit -m "production build"
git push origin main
```

### 2. Render dashboard

- New → Web Service → connect this repo
- Runtime: **Docker** (auto-detected)
- Add environment variables:

```
MISTRAL_API_KEY     your_key
GOOGLE_API_KEY      your_key
FRONTEND_URL        https://your-portfolio.vercel.app
```

`RENDER_EXTERNAL_URL` is injected automatically by Render — do not set it manually.

### 3. Keep-alive

The app pings its own `/health` endpoint every 10 minutes to prevent Render's free tier from spinning down.

---

## Frontend Integration

This backend is consumed by the portfolio chatbot at [abhilash-psi.vercel.app](https://abhilash-psi.vercel.app). The Next.js API route at `/api/chat` acts as a secure proxy — it mints a `ragcookie` (UUID v4, `httpOnly`, 30-day expiry) on first visit and forwards requests to this backend with the cookie in the server-to-server `Cookie` header.

---

## License

MIT
