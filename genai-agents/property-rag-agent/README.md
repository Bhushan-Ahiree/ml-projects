# 🏠 Property RAG Agent

> **Natural language property search powered by RAG, semantic retrieval, an agentic decision layer, and LLMs.**

**Property RAG Agent** is an end-to-end AI/ML engineering project that turns messy Indian rental listings into an intelligent property search system.

Instead of forcing users to search with rigid filters, it lets them describe what they want naturally — and either retrieves the most relevant properties using **semantic search + structured data + LLM reasoning**, or, when the question needs computation instead of retrieval, routes it to a calculation tool.

---

## ⚡ The Problem

Traditional property search looks like:

```text
City → Pune
BHK → 2
Budget → ₹30,000
Location → Baner
```

But real users ask things like:

> *"I'm looking for a spacious 2 BHK in Pune around 30k, preferably in a good area and suitable for a family."*

> *"What's the EMI on this listing at 8.5% for 20 years?"*

Keyword search struggles with the first. Pure retrieval can't answer the second at all — it needs a tool call, not a lookup.

```text
Natural Language
       ↓
Understand Intent
       ↓
Route: Retrieval, Calculation, or Insufficient Info
       ↓
Retrieve / Compute
       ↓
Rank Results (if retrieval)
       ↓
Generate Grounded Answer
```

---

## 🧠 What I'm Building

A property intelligence pipeline capable of:

* 🔎 Semantic property search
* 🧩 Structured + unstructured retrieval
* 🤖 RAG-based question answering
* 🧮 Agentic routing between retrieval, calculation, and "insufficient info"
* 📊 Property comparison
* 🎯 Constraint-aware retrieval
* 🛡️ Grounded responses
* 📈 Retrieval & generation evaluation

The goal isn't to build another "ChatGPT wrapper."

The goal is to understand **how production AI systems — including the agentic layer employers are hiring for in 2026 — are actually built.**

---

# 🏗️ Architecture

```text
                   ┌──────────────────┐
                   │   Rental Data    │
                   │ Delhi • Mumbai   │
                   │      • Pune      │
                   └────────┬─────────┘
                            │
                            ▼
                  ┌────────────────────┐
                  │ Data Engineering   │
                  │ Validation         │
                  │ Cleaning           │
                  │ Normalization      │
                  └─────────┬──────────┘
                            │
                            ▼
                  ┌────────────────────┐
                  │ Property Documents │
                  └─────────┬──────────┘
                            │
                            ▼
                  ┌────────────────────┐
                  │    Embeddings      │
                  └─────────┬──────────┘
                            │
                            ▼
                  ┌────────────────────┐
                  │   Vector Search    │
                  │ (Hybrid: BM25 +    │
                  │  Dense + Rerank)   │
                  └─────────┬──────────┘
                            ▲
                            │
                     User Query
                            │
                            ▼
                  ┌────────────────────┐
                  │ Agent Router:      │
                  │ Retrieval? Calc?   │
                  │ Insufficient info? │
                  └─────────┬──────────┘
                       ┌────┴────┐
                       ▼         ▼
              ┌──────────────┐ ┌──────────────┐
              │  Retrieval   │ │ Tool Call     │
              │  + Rank      │ │ (EMI, ₹/sqft) │
              └──────┬───────┘ └──────┬────────┘
                     └────────┬───────┘
                               ▼
                  ┌────────────────────┐
                  │       LLM          │
                  │ Grounded Generation│
                  └─────────┬──────────┘
                            │
                            ▼
                       🎯 Answer
```

---

# 📊 Data

Real-world Indian rental listing data from **Delhi · Mumbai · Pune** ([Kaggle: `bhavyadhingra00020/india-rental-house-price`](https://www.kaggle.com/datasets/bhavyadhingra00020/india-rental-house-price), scraped April 2024, ~16,300 listings).

**Note:** `price` is **monthly rent**, not a sale/resale price. All comparisons in this system are rent comparisons.

Raw datasets are intentionally preserved:

```text
data/
├── raw/
│   ├── delhi.csv
│   ├── mumbai.csv
│   └── pune.csv
│
└── processed/
```

### Why keep raw data?

Because preprocessing should be reproducible.

```text
Raw Data → Cleaning → Validation → Normalization → Processed Data
```

The original data is never modified.

---

# 🧹 Data Decisions

After inspecting the complete datasets (null-rate analysis across all three cities), the normalized schema is:

```text
house_type
house_size
location
city
price
num_bathrooms
description
security_deposit
status
```

**Column-level drops** — insufficient signal across the full dataset:

| Field | Decision | Reason |
| --- | --- | --- |
| `currency` | Remove | Constant (always INR) — metadata, not a feature |
| `numBalconies` | Remove | ~53% missing |
| `isNegotiable` | Remove | ~77% missing |
| `priceSqFt` | Remove | ~85% missing |
| `latitude` / `longitude` | Remove (v1) | Out of scope — no proximity-search feature planned yet. Deliberate scope cut, not a data-quality call |
| `verificationDate` | Remove | Relative text ("posted 2 years ago") with no scrape-date anchor — can't be converted to a real timestamp |

**Row-level drops** — column kept, but incomplete rows removed:

| Field | % null | Decision |
| --- | --- | --- |
| `numBathrooms` | ~0.3% | Drop the null rows — negligible loss, not worth imputation complexity |
| `description` | ~5% | Drop the null rows — no text means no embedding signal, so the row is unusable for RAG regardless of other fields |

These aren't arbitrary preprocessing decisions. **They're based on the actual data.**

---

# 🔍 Pipeline

### 01 — Ingest
Load and validate raw listings.

### 02 — Normalize
Convert inconsistent property data into the schema above.

### 03 — Build Documents
Combine structured property fields with the free-text description.

```text
2 BHK Apartment
Baner, Pune

Rent: ₹28,000/month
Bathrooms: 2
Security Deposit: ₹84,000

Spacious apartment located near...
```

### 04 — Embed
Convert each property document into a semantic vector.

### 05 — Retrieve
Hybrid search (BM25 + dense vector) over the query, then re-rank the top-k with a cross-encoder.

### 06 — Route
Classify the query: does it need retrieval, a calculation (EMI, price-per-sqft), or is there insufficient information to answer at all?

### 07 — Generate
Pass retrieved context (or tool output) to an LLM and generate a grounded answer.

---

# 🛡️ No Hallucinated Properties

> **The LLM is not the database.**

Property information must come from retrieved records or an explicit tool call — never invented.

If the dataset doesn't contain parking information:

❌ *"This apartment has dedicated parking."*

✅ *"Parking availability isn't specified in the available listing data."*

Grounding and failure handling are treated as **engineering problems**, not just prompting problems — the router logging which path it chose (and whether that choice was correct) is itself an evaluation artifact.

---

# 🧪 Evaluation

A RAG system isn't successful just because the response sounds impressive — this project measures it.

**Retrieval:** Precision@K · Recall@K · MRR · ranking quality

**Generation:** Faithfulness · relevance · completeness · unsupported claims

**Agent:** routing accuracy (did it choose retrieval / calculation / insufficient-info correctly?)

**System:** latency · token cost · failure rate

The goal is to answer *"is the system actually getting better?"* — not *"does the demo look cool?"*

---

# 🔬 Experiments

Every optimization should have a measurable reason, tracked as a config change against a fixed evaluation set:

```text
Retrieval:   Keyword  vs  Dense  vs  Hybrid
Ranking:     Vector similarity  vs  Vector + Reranker
Documents:   Raw description  vs  Structured + description
Embeddings:  Compare models on actual retrieval performance
```

---

# 🧰 Tech Stack

**Core:** Python, Pandas, NumPy, Git

**ML / Retrieval:** sentence-transformer embeddings, FAISS, BM25 (`rank_bm25`), cross-encoder reranking

**GenAI:** LLM APIs, RAG, prompt engineering, structured outputs, agentic tool-calling

**Engineering:** FastAPI (serving), **Celery** (async ingestion/embedding jobs), **Redis** (query caching), **MLflow** (experiment tracking), Docker, testing, CI/CD

---

# 📁 Project Structure

```text
property-rag-agent/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── models/schemas.py
│   ├── ingestion/
│   ├── embeddings/
│   ├── retrieval/          # + hybrid_search.py, reranker.py
│   ├── generation/
│   ├── agent/               # router.py, tools.py
│   ├── eval/                # golden_set.json, evaluator.py
│   ├── tasks/                # celery_tasks.py
│   └── cache/                 # redis_cache.py
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
├── tests/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

# 🚀 Roadmap

```text
[x] Dataset acquisition
[x] Raw data organization
[x] Schema investigation
[x] Missing-value analysis
[x] Final schema design

[ ] Data loader
[ ] Normalization pipeline
[ ] Processed dataset

[ ] Document generation
[ ] Embeddings
[ ] Vector index (FAISS)
[ ] Baseline (naive) retrieval

[ ] Evaluation golden set
[ ] Retrieval metrics
[ ] Generation evaluation (faithfulness/relevance)

[ ] Hybrid retrieval (BM25 + dense)
[ ] Reranking
[ ] Query rewriting

[ ] Agent router (retrieval / calculation / insufficient-info)
[ ] Calculation tools (EMI, price-per-sqft)
[ ] Agent routing evaluation

[ ] FastAPI service
[ ] Celery async jobs
[ ] Redis query caching
[ ] MLflow experiment tracking
[ ] Docker
[ ] Live deployment
```

---

# 🎓 Skills Developed

**Data:** cleaning · validation · normalization · pipelines

**ML:** similarity · embeddings · ranking · evaluation · unsupervised learning (clustering as an embedding sanity-check)

**GenAI:** LLMs · RAG · hybrid search · reranking · agentic routing · grounding

**Engineering:** Python · Git · FastAPI · Celery · Redis · MLflow · Docker · deployment

**Most importantly:** taking imperfect data and turning it into a measurable, reliable, production-shaped system — not just a notebook that works once.

---

## 📌 Project Status

🚧 **Active development** — currently building the data ingestion and normalization pipeline (`loader.py`).

Every architectural decision here is backed by an actual measurement, not a default choice — see the Data Decisions section above.