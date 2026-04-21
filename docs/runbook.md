# Runbook — Reproduce the ELK Movies Platform from scratch

This document covers a full reproduction on a clean machine: from git clone to a working Kibana dashboard. Follow the steps in order.

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

## Step 1 — Clone the repo

```bash
git clone https://github.com/<org>/elk-movies-platform.git
cd elk-movies-platform
```

## Step 2 — Get the dataset

The CSV is not in the repo (769,632 rows, ~500 MB — gitignored).

Download from Kaggle: https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset

Place the file at:

```bash
DATA/movies.csv
```

Expected row count: 769,632 (including header). Confirm with:

```bash
wc -l DATA/movies.csv
# expected: 769632
```

## Step 3 — Create the logs directory

Logstash writes its sincedb state to `./logs/sincedb_movies`. The directory must exist and be world-writable before the container starts, or Logstash exits silently.

```bash
mkdir -p logs
chmod 777 logs
```

## Step 4 — Start the stack

```bash
./start.sh
```

`start.sh` does the following in order:

1. Ensures `logs/sincedb_movies` exists with the right ownership (uid 1000 — Logstash user).
2. Runs `docker compose up -d`.
3. Waits for Elasticsearch to pass its health check before Logstash starts.
4. Applies the explicit mapping for `movies_clean` before any data lands.

Expected output (approximate):

```
[+] Running 3/3
 ✔ elasticsearch  Started
 ✔ logstash       Started
 ✔ kibana         Started
```

Elasticsearch takes 20–40 seconds to become healthy on a typical laptop. If Logstash exits immediately, check `docker compose logs logstash` — the most common cause is a missing or unwritable sincedb path.

## Step 5 — Monitor ingestion

In a second terminal:

```bash
python3 monitor_ingestion.py
```

The script polls `movies_raw/_count` every few seconds and prints progress. Ingestion takes 5–15 minutes depending on hardware. Expected final count: ~662,083 documents. The remaining ~107,549 rows fail parsing (malformed CSV lines) and are tagged but not indexed — this is expected.

```
[14:23:11] movies_raw: 662083 docs  (86.0% of 769632)
```

## Step 6 — Verify via Elasticsearch API

Wait until the doc count stabilises, then run these checks:

```bash
... (92lignes restantes)