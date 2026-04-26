# Runbook — Reproduce the ELK Movies Platform from scratch

This document covers a full reproduction on a clean machine: from git clone to a working Kibana dashboard and search engine. Follow the steps in order.

---

## Prerequisites

| Tool | Version tested | Install |
|---|---|---|
| Docker | 24.x | https://docs.docker.com/get-docker/ |
| Docker Compose | v2.x (plugin) | bundled with Docker Desktop; `apt install docker-compose-plugin` on Linux |
| Python 3 | 3.9+ | system package or pyenv |
| git | any recent | system package |

Check all four are present before continuing:

```bash
docker --version
docker compose version
python3 --version
git --version
```

---

## Step 1 — Clone the repo

```bash
git clone https://github.com/<org>/elk-movies-platform.git
cd elk-movies-platform
```

---

## Step 2 — Get the dataset

The CSV is not in the repo (769,632 rows, ~500 MB — gitignored).

Download from Kaggle: https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset

Place the file at:

```bash
DATA/movies.csv
```

Confirm row count:

```bash
wc -l DATA/movies.csv
# expected: 769632
```

---

## Step 3 — Create the logs directory

Logstash writes its sincedb state to `./logs/sincedb_movies`. The directory must exist and be world-writable before the container starts, or Logstash exits silently.

```bash
mkdir -p logs
chmod 777 logs
```

---

## Step 4 — Start the stack

```bash
./start.sh
```

`start.sh` does the following in order:

1. Ensures `logs/sincedb_movies` exists with the right ownership (uid 1000 — Logstash user).
2. Starts Elasticsearch first and waits for it to be healthy.
3. Applies the explicit mapping for `movies_clean` before any data lands.
4. Starts Logstash and Kibana.

Expected output (approximate):

```
[+] Running 3/3
 ✔ elasticsearch  Started
 ✔ logstash       Started
 ✔ kibana         Started
```

Elasticsearch takes 20–40 seconds on a typical laptop. If Logstash exits immediately, check:

```bash
docker compose logs logstash
```

Most common cause: missing or unwritable sincedb path.

---

## Step 5 — Monitor ingestion

Open a second terminal:

```bash
python3 monitor_ingestion.py
```

The script polls `movies_raw/_count` and `movies_clean/_count` every few seconds. Ingestion takes 5–15 minutes depending on hardware.

Expected final counts:

| Index | Documents |
|---|---|
| `movies_raw` | 662,083 |
| `movies_clean` | 662,077 |

The remaining ~107,549 rows fail CSV parsing and are tagged but not indexed. This is expected — documented in `docs/data_cleaning.md`.

Wait until the script reports completion and `./start.sh` exits cleanly before continuing.

---

## Step 6 — Verify via Elasticsearch API

```bash
# Both indices present and green
curl "http://localhost:9200/_cat/indices/movies_raw,movies_clean?v"

# Document counts
curl "http://localhost:9200/movies_raw/_count"
curl "http://localhost:9200/movies_clean/_count"

# Sample document from movies_clean
curl "http://localhost:9200/movies_clean/_search?pretty&size=1"
```

Expected index status: `green`. If `yellow`, replicas are unassigned — normal for a single-node cluster, does not affect functionality.

---

## Step 7 — Import the Kibana dashboard

1. Open Kibana at `http://localhost:5601`
2. Go to **Stack Management → Saved Objects → Import**
3. Select `docs/kibana_export.ndjson`
4. Click **Import**

The "Movies Analytics Dashboard" will appear under **Analytics → Dashboard**.

Open it. If charts show no data, check the time filter — it must be set to an absolute range covering historical data, not "Last 15 minutes". The export already includes the correct time range; it will load automatically on import.

---

## Step 8 — Run the search engine

```bash
cd search_engine
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open `http://localhost:5000`.

Type a movie title in the search bar. Use the filter panel to narrow by original language, genre, release year range, or minimum rating. Results return with poster images and vote averages.

Elasticsearch must be running (Step 4) before starting the search engine.

---

## Step 9 — Run analytical queries (optional)

All 12 DSL queries are in `docs/queries.md` with comments and expected results.

To run them:

1. Open Kibana at `http://localhost:5601`
2. Go to **Dev Tools**
3. Paste any query from `docs/queries.md` and press the play button

Or run via curl:

```bash
curl -X GET "http://localhost:9200/movies_clean/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": { "match_all": {} },
  "size": 1
}
'
```

---

## Step 10 — Shutdown

Graceful stop (preserves Elasticsearch data and sincedb state):

```bash
./stop.sh
```

Full reset (destroys volumes and deletes logs/sincedb_movies — next `./start.sh` re-ingests from scratch):

```bash
./stop.sh --reset
```

Use `--reset` only when you need a clean slate. It wipes all indexed data.

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Logstash exits immediately | `logs/` missing or wrong permissions | `mkdir -p logs && chmod 777 logs` |
| `movies_clean` count stays at 0 | `@version` not removed in clone, or mapping not applied before start | Run `./stop.sh --reset && ./start.sh` |
| Kibana shows empty charts | Time filter set to "Last 15 minutes" | Set absolute date range in the dashboard |
| Search engine 500 error | Elasticsearch not running | Start the stack first (Step 4) |
| Index status `yellow` | Single-node cluster, replicas unassigned | Expected — no action needed |

---

## Related files

[[data_dictionary.md]] [[data_cleaning.md]] [[queries.md]] [[planning_poker.md]] [[projet_management.md]] [[demo_script.md]]
