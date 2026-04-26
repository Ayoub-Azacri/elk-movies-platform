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


def get_count(index):
    try:
        r = requests.get(f"http://127.0.0.1:9200/{index}/_stats/docs", timeout=5)
        r.raise_for_status()
        data = r.json()
        docs    = data["_all"]["primaries"]["docs"]
        count   = docs.get("count", 0)
        deleted = docs.get("deleted", 0)
        return count, deleted
    except Exception:
        return None, None


print("Monitoring ingestion into movies_raw and movies_clean...")
print("=" * 60)

prev_count  = 0
prev_time   = time.time()
stall_since = None

while True:
    raw_count, deleted = get_count("movies_raw")
    clean_count, _     = get_count("movies_clean")
    now = time.time()

    if raw_count is None:
        print("\rElasticsearch non accessible, on réessaie...", end="", flush=True)
        time.sleep(2)
        continue

    elapsed = now - prev_time
    speed   = int((raw_count - prev_count) / elapsed) if elapsed > 0 else 0

    # Progress bar is calculated against DOCS_ATTENDUS so it reaches 100% correctly
    percent    = min(raw_count / DOCS_ATTENDUS, 1.0)
    bar_length = 20
    filled     = int(bar_length * percent)
    bar        = "█" * filled + "░" * (bar_length - filled)

    clean_str = f"{clean_count:,}" if clean_count is not None else "N/A"

    print(
        f"\r[{bar}] raw: {raw_count:,} — clean: {clean_str} ({percent:.1%}) — {speed:,} docs/sec",
        end="",
        flush=True,
    )

    if raw_count >= DOCS_ATTENDUS:
        print("\n" + "=" * 60)
        print("Ingestion terminée.")
        print(f"  movies_raw   : {raw_count:,} docs")
        print(f"  movies_clean : {clean_str} docs")
        print(f"  Ignorés      : {TOTAL_MOVIES - raw_count:,} lignes malformées ({(TOTAL_MOVIES - raw_count) / TOTAL_MOVIES:.1%})")
        break

    if raw_count == prev_count:
        if stall_since is None:
            stall_since = now
        elif now - stall_since > STALL_TIMEOUT:
            print(f"\n\nAucune nouvelle opération depuis {STALL_TIMEOUT}s.")
            print(f"movies_raw   : {raw_count:,}")
            print(f"movies_clean : {clean_str}")
            print(f"Supprimés    : {deleted:,}")
            print(f"Manquants    : {TOTAL_MOVIES - raw_count:,} / {TOTAL_MOVIES:,} ({percent:.1%})")
            break
    else:
        stall_since = None

    prev_count = raw_count
    prev_time  = now
    time.sleep(2)
