# Demo Script — ELK Movies Platform

The recording walks through the full platform lifecycle: stack startup, ingestion monitoring, Kibana dashboard, search engine, and clean shutdown.

---

## Step 1 — Stack startup (`./start.sh`)

Run `./start.sh` from the project root. Docker Compose pulls up three containers: Elasticsearch (port 9200), Logstash, and Kibana (port 5601). The script waits for each service to pass its health check before starting the next one. No manual ordering needed.

## Step 2 — Monitor ingestion (`python3 monitor_ingestion.py`)

Open a second terminal. Run `python3 monitor_ingestion.py` to track how many documents Logstash has pushed into `movies_raw` in real time. Wait until the count stabilises at 662,083. The remaining ~107,549 rows from the source CSV were dropped due to malformed lines.

## Step 3 — Wait for `./start.sh` to finish

Back in the first terminal, `./start.sh` finishes once ingestion is confirmed and Kibana is ready. No further action needed at this point.

## Step 4 — Elasticsearch index check

Open a browser or run `curl` to verify both indices are present and green:

- `movies_raw` — 662,083 documents, raw ingestion
- `movies_clean` — same data, explicitly mapped, with custom analyzer

Both indices show status `green` (replicas set to 0 for single-node cluster).

## Step 5 — Kibana dashboard

Open Kibana at `http://localhost:5601`. Import `docs/kibana_export.ndjson` via **Stack Management → Saved Objects → Import**. Open the "Movies Analytics Dashboard". The time filter is pre-set to an absolute date range covering the full dataset.

Six visualizations load:

- **Pie — Films by genre** (Drama 25.99%, Documentary 17.06%, Comedy 16.2%): Drama and Documentary together account for 43% of the catalogue. Their dominance reflects structurally lower production costs, which removes barriers for independent and volume producers.

- **Line — Films per year**: Production was flat through most of the 20th century, then accelerates sharply post-2000. The inflection point maps to the digital transition and the rise of global streaming platforms, which radically lowered entry barriers for new producers.

- **Bar — Average budget by genre** (Adventure ~$8M highest, Documentary lowest): Heavy investment in Adventure and Action confirms a blockbuster economy where capital concentrates on technological spectacle. Drama stays near the median budget — high volume, controlled cost.

- **Histogram — Rating distribution** (`vote_average` clusters 6–7): The market is saturated with content rated "average." Films above 8 are statistical outliers — rare prestige anchors for studios rather than the norm.

- **Bar — Top 10 films by popularity** (scores 2,000–4,000): The gap between rank 1 and rank 10 is large, illustrating an ultra-polarised attention economy where a handful of modern franchises capture most of global cultural visibility.

- **Pie — Films by original language** (English 51.53%, French 6.32%, Spanish 5.72%): English confirms commercial dominance, but French and Spanish together reach 12% — a sign of strong international reach for Latin-language cinemas despite the Anglo-American industry's scale advantage.

## Step 6 — CineSearch search engine

```bash
cd search_engine
source .venv/bin/activate
python app.py
```

Open `http://localhost:5000`. Type a movie title in the search bar. Results return with poster images, vote averages, and release years. Apply filters from the left panel: original language, genre, release year range, minimum score. All filters combine into a single Elasticsearch `bool` query.

## Step 7 — Shutdown

```bash
./stop.sh          # graceful stop — preserves Elasticsearch data and sincedb state
./stop.sh --reset  # full reset — destroys volumes and deletes logs/sincedb_movies
```

Both commands run in sequence. The `--reset` flag wipes all persistent state so the stack can be reproduced from scratch.

---

## Backlinks

[[runbook.md]] [[queries.md]] [[kibana_export.ndjson]] [[data_cleaning.md]] [[data_dictionary.md]]
