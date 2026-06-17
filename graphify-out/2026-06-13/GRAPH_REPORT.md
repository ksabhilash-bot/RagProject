# Graph Report - D:\RagProject  (2026-06-13)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 50 nodes · 75 edges · 6 communities
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 2 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `34f7cd6d`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]

## God Nodes (most connected - your core abstractions)
1. `query()` - 7 edges
2. `vectorload()` - 6 edges
3. `lifespan()` - 6 edges
4. `create_vectorstore()` - 5 edges
5. `get_user_id()` - 5 edges
6. `get_retriever()` - 5 edges
7. `RagProject` - 5 edges
8. `build_chain()` - 3 edges
9. `ask()` - 3 edges
10. `get_embeddings()` - 3 edges

## Surprising Connections (you probably didn't know these)
- `RagProject` --semantically_similar_to--> `RAG-Based Portfolio Assistant`  [INFERRED] [semantically similar]
  README.md → AKS.txt
- `graphify` --conceptually_related_to--> `RagProject`  [INFERRED]
  AGENTS.md → README.md
- `query()` --calls--> `ask()`  [EXTRACTED]
  main.py → chain.py
- `lifespan()` --calls--> `vectorload()`  [EXTRACTED]
  main.py → embedding.py
- `lifespan()` --calls--> `build_chain()`  [EXTRACTED]
  main.py → chain.py

## Import Cycles
- 1-file cycle: `main.py -> main.py`

## Communities (6 total, 0 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.27
Nodes (7): ask(), build_chain(), FastAPI, keep_alive(), lifespan(), get_retriever(), Chroma

### Community 1 - "Community 1"
Cohesion: 0.22
Nodes (11): BaseModel, check_rate_limit(), flush_cache(), get_user_id(), make_cache_key(), query(), QueryRequest, Sliding window rate limiter keyed on ragcookie value. (+3 more)

### Community 2 - "Community 2"
Cohesion: 0.33
Nodes (7): create_vectorstore(), get_embeddings(), Chroma, Document, vectorload(), Document, retrieve_docs()

### Community 3 - "Community 3"
Cohesion: 0.25
Nodes (8): graphify, Abhilash K S, CampusDesk, RAG-Based Portfolio Assistant, ChromaDB, FastAPI, LangChain, RagProject

### Community 4 - "Community 4"
Cohesion: 0.47
Nodes (3): document_loader(), Document, split_documents()

### Community 5 - "Community 5"
Cohesion: 0.50
Nodes (3): BaseSettings, Config, Settings

## Knowledge Gaps
- **10 isolated node(s):** `Config`, `Document`, `Chroma`, `Document`, `Document` (+5 more)
  These have ≤1 connection - possible missing edges or undocumented components.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `vectorload()` connect `Community 2` to `Community 0`?**
  _High betweenness centrality (0.048) - this node is a cross-community bridge._
- **Why does `create_vectorstore()` connect `Community 2` to `Community 4`?**
  _High betweenness centrality (0.044) - this node is a cross-community bridge._
- **Why does `get_user_id()` connect `Community 1` to `Community 0`?**
  _High betweenness centrality (0.043) - this node is a cross-community bridge._
- **What connects `Config`, `Document`, `Read ragcookie sent by Next.js. 403 if missing.` to the rest of the system?**
  _13 weakly-connected nodes found - possible documentation gaps or missing edges._