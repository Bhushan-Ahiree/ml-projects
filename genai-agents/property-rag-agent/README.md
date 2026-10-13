# Property RAG Agent

Natural-language search over Indian rental listings. It retrieves matching properties with semantic search plus hard filters, and the next step is an LLM that answers only from the retrieved listings.

## Status

**Built**

- Data loading and cleaning for Delhi, Mumbai and Pune rental listings (`app/ingestion/loader.py`)
- One text document per listing, combining structured fields and the free-text description (`app/embeddings/text_builder.py`)
- Embeddings with sentence-transformers `all-MiniLM-L6-v2` (`app/embeddings/build_embeddings.py`)
- Retrieval: hard filters on city, max price and BHK, then cosine similarity to rank the remaining listings (`app/retrieval/vector_search.py`)
- Context builder that formats the top results for an LLM prompt (`app/retrieval/context_builder.py`)

**Next**

- LLM answer step that uses only the retrieved listings
- Small evaluation set: retrieval precision@k and answer faithfulness
- Hybrid retrieval (BM25 + dense) and reranking, kept only if the evaluation shows a gain
- Calculation tools (EMI, rent per sq ft) and a router that decides between retrieval and calculation
- FastAPI endpoint

## The problem

Filter-based search needs exact inputs: city, BHK, budget. Real users write things like:

> "Spacious 2 BHK in Pune around 30k, good for a family."

Some of that is a hard constraint (city, BHK, budget) and some of it is fuzzy (spacious, family-friendly). This project treats them differently.

## How retrieval works

1. Each listing becomes a short text document: type, location, area, rent, bathrooms and description.
2. All documents are embedded once with `all-MiniLM-L6-v2`.
3. The user query is embedded with the same model.
4. Hard constraints are applied first as an exact mask: city, max price, BHK.
5. Only the listings that pass are ranked by cosine similarity, and the top k are returned.

Why filter first: similarity scores can't enforce a budget. A 45k flat can be "similar" to a 30k query. Exact constraints are applied exactly, and similarity is used only for ranking.

## Data

Indian rental listings for Delhi, Mumbai and Pune ([Kaggle: `bhavyadhingra00020/india-rental-house-price`](https://www.kaggle.com/datasets/bhavyadhingra00020/india-rental-house-price), scraped April 2024).

`price` is **monthly rent**, not a sale price.

```text
data/raw/
├── Indian_housing_Delhi_data.csv
├── Indian_housing_Mumbai_data.csv
└── Indian_housing_Pune_data.csv
```

Raw files are never modified. Processed output is written to `data/processed/`.

### Data decisions

Based on null-rate analysis across all three cities.

**Columns dropped**

| Field | Reason |
| --- | --- |
| `currency` | Constant (always INR) |
| `numBalconies` | ~53% missing |
| `isNegotiable` | ~77% missing |
| `priceSqFt` | ~85% missing |
| `latitude` / `longitude` | Out of scope for v1: no proximity search planned yet |
| `verificationDate` | Relative text ("posted 2 years ago") with no anchor date |

**Rows dropped**

| Field | % null | Decision |
| --- | --- | --- |
| `numBathrooms` | ~0.3% | Drop the rows: negligible loss |
| `description` | ~5% | Drop the rows: no text means no embedding signal |

## Design principle: the LLM is not the database

When the generation step is added, every property fact in an answer must come from a retrieved listing. If the data doesn't say whether a flat has parking, the answer should say that, not guess. This will be measured with the evaluation set, not assumed.

## Project structure

```text
property-rag-agent/
├── app/
│   ├── ingestion/loader.py
│   ├── embeddings/
│   │   ├── embedder.py
│   │   ├── text_builder.py
│   │   └── build_embeddings.py
│   └── retrieval/
│       ├── vector_search.py
│       └── context_builder.py
├── data/
│   ├── raw/
│   └── processed/        # generated, not committed
├── notebooks/01_data_inspection.ipynb
└── requirements.txt
```

## Run

```bash
pip install -r requirements.txt
# build data/processed/properties.jsonl with app/ingestion/loader.py (see the notebook), then:
python -m app.embeddings.build_embeddings
```

`properties.jsonl` and `property_embeddings.npy` are generated files and are not stored in the repo.
