import time
import requests

# total number of rows in movies.csv (header excluded)
# source: wc -l DATA/movies.csv → 769,632
TOTAL_MOVIES  = 769632
STALL_TIMEOUT = 20

# ~14% of rows are malformed and rejected by Logstash — the real completion
# target is ~662k docs, not 769k. Using TOTAL_MOVIES as the threshold means
# the completion check never fires and the script always exits via stall timeout.
DOCS_ATTENDUS = 662083


def get_docs_stats():
    try:
        r = requests.get("http://127.0.0.1:9200/movies_raw/_stats/docs", timeout=5)
        r.raise_for_status()
        data = r.json()
        docs    = data["_all"]["primaries"]["docs"]
        count   = docs.get("count", 0)
        deleted = docs.get("deleted", 0)
        return count, deleted
    except Exception:
        return None, None


print("Monitoring ingestion into movies_raw...")
print("=" * 60)

prev_count  = 0
prev_time   = time.time()
stall_since = None

while True:
    count, deleted = get_docs_stats()
    now = time.time()

    if count is None:
        print("\rElasticsearch non accessible, on réessaie...", end="", flush=True)
        time.sleep(2)
        continue

    elapsed = now - prev_time
    speed   = int((count - prev_count) / elapsed) if elapsed > 0 else 0

    # Progress bar is calculated against DOCS_ATTENDUS so it reaches 100% correctly
    percent    = min(count / DOCS_ATTENDUS, 1.0)
    bar_length = 20
    filled     = int(bar_length * percent)
    bar        = "█" * filled + "░" * (bar_length - filled)

    print(
        f"\r[{bar}] {count:,} / {DOCS_ATTENDUS:,} ({percent:.1%}) — {speed:,} docs/sec",
        end="",
        flush=True,
    )

    if count >= DOCS_ATTENDUS:
        print("\n" + "=" * 60)
        print("Ingestion terminée.")
        # Show how many raw CSV rows were dropped by Logstash
        print(f"  Indexés  : {count:,} docs")
        print(f"  Ignorés  : {TOTAL_MOVIES - count:,} lignes malformées ({(TOTAL_MOVIES - count) / TOTAL_MOVIES:.1%})")
        break

    if count == prev_count:
        if stall_since is None:
            stall_since = now
        elif now - stall_since > STALL_TIMEOUT:
            print(f"\n\nAucune nouvelle opération depuis {STALL_TIMEOUT}s.")
            print(f"Actifs    : {count:,}")
            print(f"Supprimés : {deleted:,}")
            print(f"Manquants : {TOTAL_MOVIES - count:,} / {TOTAL_MOVIES:,} ({percent:.1%})")
            break
    else:
        stall_since = None

    prev_count = count
    prev_time  = now
    time.sleep(2)
