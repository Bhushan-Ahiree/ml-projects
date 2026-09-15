 # 🏠 PropertyAI — Intelligent Property Search

> **Natural language property search powered by RAG, semantic retrieval, and LLMs.**

**PropertyAI** is an end-to-end AI/ML engineering project that turns messy Indian rental listings into an intelligent property search system.

Instead of forcing users to search with rigid filters, PropertyAI lets them describe what they want naturally — and retrieves the most relevant properties using **semantic search + structured data + LLM reasoning**.

---

## ⚡ The Problem

Traditional property search looks like:

```text
City → Pune
BHK → 2
Budget → ₹30,000
Location → Baner
```

But real users ask:

> *"I'm looking for a spacious 2 BHK in Pune around 30k, preferably in a good area and suitable for a family."*

Keyword search struggles with this.

PropertyAI aims to bridge that gap:

```text
Natural Language
       ↓
Understand Intent
       ↓
Retrieve Relevant Properties
       ↓
Rank Results
       ↓
Generate Grounded Answer
```

---

## 🧠 What I'm Building

A property intelligence pipeline capable of:

* 🔎 Semantic property search
* 🧩 Structured + unstructured retrieval
* 🤖 RAG-based question answering
* 📊 Property comparison
* 🎯 Constraint-aware retrieval
* 🛡️ Grounded responses
* 📈 Retrieval & generation evaluation

The goal isn't to build another "ChatGPT wrapper".

The goal is to understand **how production AI systems are actually built.**

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
                  └─────────┬──────────┘
                            ▲
                            │
                     User Query
                            │
                            ▼
                  ┌────────────────────┐
                  │ Query Understanding│
                  └─────────┬──────────┘
                            │
                            ▼
                  ┌────────────────────┐
                  │ Retrieval + Rank   │
                  └─────────┬──────────┘
                            │
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

The system currently uses real-world Indian rental listing data from:

**Delhi · Mumbai · Pune**

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
Raw Data
   ↓
Cleaning
   ↓
Validation
   ↓
Normalization
   ↓
Processed Data
```

The original data should never be modified.

---

# 🧹 Data Decisions

After inspecting the complete datasets, the initial normalized schema is:

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

Some fields were intentionally removed because they provided little reliable value for the initial system:

| Field                    | Decision                     |
| ------------------------ | ---------------------------- |
| `currency`               | Constant → remove            |
| `numBalconies`           | ~53% missing → remove        |
| `isNegotiable`           | ~77% missing → remove        |
| `priceSqFt`              | ~85% missing → remove        |
| `latitude` / `longitude` | Out of v1 scope              |
| `verificationDate`       | Relative/unreliable → remove |

These aren't arbitrary preprocessing decisions.

**They are based on the actual data.**

---

# 🔍 RAG Pipeline

The core system follows:

### 01 — Ingest

Load and validate raw listings.

### 02 — Normalize

Convert inconsistent property data into a predictable schema.

### 03 — Build Documents

Combine structured property information with descriptions.

Example:

```text
2 BHK Apartment
Baner, Pune

Rent: ₹28,000
Bathrooms: 2
Security Deposit: ₹84,000

Spacious apartment located near...
```

### 04 — Embed

Convert each property document into a semantic vector.

```text
Property
   ↓
Embedding Model
   ↓
[0.21, -0.43, 0.77, ...]
```

### 05 — Retrieve

Convert the user's query into an embedding and retrieve similar properties.

### 06 — Generate

Pass the retrieved properties to an LLM and generate an answer grounded in those results.

---

# 🛡️ No Hallucinated Properties

One of the most important design principles:

> **The LLM is not the database.**

Property information must come from retrieved records.

If the dataset doesn't contain parking information:

❌

> "This apartment has dedicated parking."

Instead:

✅

> "Parking availability isn't specified in the available listing data."

This project treats **grounding and failure handling as engineering problems**, not just prompting problems.

---

# 🧪 Evaluation

A RAG system isn't successful just because the response sounds impressive.

So this project will measure it.

### Retrieval

* Precision@K
* Recall@K
* MRR
* Ranking quality

### Generation

* Faithfulness
* Relevance
* Completeness
* Unsupported claims

### System

* Latency
* Token usage
* Cost
* Failure rate

The goal is to answer:

> **"Is the system actually getting better?"**

—not just:

> "Does the demo look cool?"

---

# 🔬 Experiments

The project will deliberately compare different approaches.

### Retrieval

```text
Keyword Search
      vs
Dense Search
      vs
Hybrid Search
```

### Ranking

```text
Vector Similarity
      vs
Vector + Reranker
```

### Documents

```text
Raw Description
      vs
Structured + Description
```

### Embeddings

Compare embedding models based on actual retrieval performance.

Every optimization should have a measurable reason.

---

# 🧰 Tech Stack

The stack will evolve as the system develops.

**Core**

* Python
* Pandas
* NumPy
* Git / GitHub

**ML / Retrieval**

* Embedding models
* Vector database
* Similarity search
* Ranking / reranking

**GenAI**

* LLM APIs
* RAG
* Prompt engineering
* Structured outputs

**Engineering**

* FastAPI
* Testing
* Logging
* Environment configuration
* Docker
* CI/CD

> Tools will be introduced only when the problem requires them.

---

# 📁 Project Structure

```text
property-ai/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── src/
│   ├── ingestion/
│   ├── retrieval/
│   ├── embeddings/
│   ├── generation/
│   └── evaluation/
│
├── tests/
│
├── notebooks/
│
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
[x] Initial schema design

[ ] Data loader
[ ] Data validation
[ ] Normalization pipeline
[ ] Processed dataset

[ ] Document generation
[ ] Embeddings
[ ] Vector index
[ ] Baseline retrieval

[ ] RAG pipeline
[ ] Grounded responses
[ ] Metadata filtering
[ ] Hybrid retrieval

[ ] Evaluation dataset
[ ] Retrieval metrics
[ ] Generation evaluation
[ ] Failure analysis

[ ] API
[ ] Docker
[ ] Deployment
[ ] Monitoring
```

---

# 💡 What Makes This Project Different?

This project isn't about using the maximum number of AI technologies.

It's about learning to build an AI system **the way an engineer would.**

```text
Real Data
   ↓
Understand the Problem
   ↓
Make Data Decisions
   ↓
Build Baseline
   ↓
Measure
   ↓
Find Failure
   ↓
Improve
   ↓
Measure Again
```

No unnecessary agents.

No unnecessary fine-tuning.

No "AI" added just for the sake of saying AI.

---

# 🎓 Skills I'm Developing

This project is being used as a hands-on learning path across:

### Data

`Data Cleaning` · `Validation` · `Normalization` · `Pipelines`

### ML

`Similarity` · `Embeddings` · `Ranking` · `Evaluation`

### GenAI

`LLMs` · `RAG` · `Prompting` · `Vector Search` · `Grounding`

### Engineering

`Python` · `Git` · `APIs` · `Testing` · `Docker` · `Deployment`

### Most importantly

**Problem solving.**

Taking imperfect data and turning it into a measurable, reliable system.

---

# 🏁 Final Goal

The finished project should let me demonstrate more than:

> *"I know Python and I have used an LLM API."*

It should demonstrate that I can:

**Understand → Build → Debug → Evaluate → Improve → Deploy**

a real AI/ML system.

---

## 📌 Project Status

🚧 **Active Development**

Currently working on the **data ingestion and normalization pipeline**.

More importantly, this project is being built incrementally — every architectural decision is backed by an actual problem, experiment, or measurement.

---

### Built to learn.

### Measured to improve.

### Engineered to ship.
