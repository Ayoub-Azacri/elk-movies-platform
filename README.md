# ELK Movies Platform

Welcome to the **ELK Movies Platform** repository! 🎬
This project builds a full data pipeline and analytics platform on top of a 769,632-row movie dataset — from raw ingestion to a live search engine. Built as a Master Data & AI exam project, it covers the full ELK stack with Docker, explicit Elasticsearch mappings, Kibana dashboards, and a Flask-based search UI.

---

## 🏗️ Data Architecture

```
DATA/movies.csv  →  Logstash (ETL)  →  Elasticsearch :9200
                                               ↑
                                    Kibana :5601 · CineSearch :5000
```

The pipeline follows a two-index strategy:

1. **`movies_raw`**: Raw ingestion — 662,083 documents, partial type casting, no array splitting. Malformed CSV rows (~107k) are tagged and excluded.
2. **`movies_clean`**: Cleaned and explicitly mapped index — null handling, type coercion, dash-split arrays, custom English analyzer on `title` and `overview`.

---

## 🚀 Project Features

### F1 — ELK Stack Bootstrap
Docker Compose setup with Elasticsearch 8.13.0, Logstash, and Kibana. Health checks, volume mounts, heap tuning, and single-node configuration.

### F2 — Raw CSV Ingestion
Logstash pipeline reads `DATA/movies.csv` (769,632 rows), parses 20 columns, casts types, and indexes into `movies_raw`. Sincedb state makes re-runs resumable and idempotent.

### F3 — Data Cleaning Pipeline
Logstash filter chain transforms `movies_raw` into `movies_clean`: null handling, type coercion, dash-split arrays for `genres`/`credits`/`keywords`, and drop rules for malformed records.

### F4 — Explicit Mapping
`movies_clean` index with a hand-written mapping: custom `english_movie_analyzer` (stemming + stopwords) on free-text fields, `keyword` sub-fields for aggregations, `long` for budget/revenue, `date` for `@timestamp`.

### F5 — Analytical DSL Queries
12 commented DSL queries in `docs/queries.md` — including 5 `bool` queries. Topics: top films by popularity and rating, budget distribution, full-text search, genre and language breakdowns. All rating queries use a `vote_count >= 50` floor to filter statistical noise.

### F6 — Kibana Dashboard
6 Lens visualizations assembled into one dashboard and exported as `docs/kibana_export.ndjson`:
- Pie: films by genre
- Line: films per year
- Bar: average budget by genre
- Histogram: rating distribution
- Bar: top 10 films by popularity
- Pie: films by original language

### F7 — Documentation
Full documentation suite: data dictionary, cleaning rules, runbook (fresh machine → working platform), planning poker backlog, project management, demo script, and a 5-page synthesis report.

### F8 — CineSearch Search Engine
Flask app with full-text fuzzy search on `title` and `overview` (title boosted ×3). Dynamic filters for language, genre, year range, and minimum score. Poster images via TMDB. Starts with `python app.py`.

---

## ⚡ Quick Start

```bash
# 1. Clone
git clone https://github.com/Ayoub-Azacri/elk-movies-platform.git
cd elk-movies-platform

# 2. Add dataset (not in repo — download from Kaggle)
# https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset
# Place at DATA/movies.csv

# 3. Prepare logs directory
mkdir -p logs && chmod 777 logs

# 4. Start the stack
./start.sh

# 5. Monitor ingestion (second terminal)
python3 monitor_ingestion.py

# 6. Open Kibana
# http://localhost:5601
# Import docs/kibana_export.ndjson via Stack Management → Saved Objects

# 7. Start search engine
cd search_engine && source .venv/bin/activate && python app.py
# http://localhost:5000
```

Full step-by-step: [`docs/runbook.md`](docs/runbook.md)

---

## 📊 Key Numbers

| Metric | Value |
|--------|-------|
| Source rows | 769,632 |
| Indexed (`movies_raw`) | 662,083 (86%) |
| Dropped (malformed CSV) | 107,549 (14%) |
| Indexed (`movies_clean`) | 662,077 |
| DSL queries | 12 (5 bool) |
| Kibana visualizations | 6 |

---

## 👥 Team

| Member | Role | Features |
|--------|------|----------|
| Youssef El Hajji | Lead Tech | F1 Bootstrap · F8 Search Engine |
| Ayoub Azacri | Data Engineer | F2 Raw Ingestion · F5 DSL Queries |
| Omar Hakik | Data Quality | F3 Data Cleaning · F4 Mapping |
| Youssef DEKHAIL | Data Analyst | F6 Kibana Dashboard · F7 Documentation |

---

## 📁 Repository Structure

```
elk-movies-platform/
├── DATA/                   # movies.csv (gitignored)
├── logstash/pipeline/      # logstash.conf — ETL pipeline
├── mapping/                # movies_clean_mapping.json
├── search_engine/          # Flask app (F8)
├── docs/
│   ├── queries.md          # 12 DSL queries
│   ├── kibana_export.ndjson
│   ├── data_dictionary.md
│   ├── data_cleaning.md
│   ├── runbook.md
│   ├── planning_poker.md
│   ├── document_synthese.pdf
│   └── demo.gif
├── docker-compose.yml
├── start.sh / stop.sh
└── monitor_ingestion.py
```

---

## 🛡️ License

This project is licensed under the [MIT License](LICENSE).

## 🌟 About Me

Hi there! I'm **Ayoub Azacri**, a Data Engineer passionate about building data pipelines and working with large-scale datasets.
