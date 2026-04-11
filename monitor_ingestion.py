import time
import requests

TOTAL_MOVIES = 769632  # nombre de lignes dans ton CSV

def get_indexed_count():
    try:
        r = requests.get("http://localhost:9200/movies_raw/_count")
        return r.json().get("count", 0)
    except:
        return 0

def progress_bar(current, total, bar_length=50):
    percent = current / total
    filled = int(bar_length * percent)
    bar = "█" * filled + "░" * (bar_length - filled)
    return f"\r[{bar}] {current:,} / {total:,} ({percent:.1%})"

print("Monitoring ingestion into movies_raw...")
while True:
    count = get_indexed_count()
    print(progress_bar(count, TOTAL_MOVIES), end="", flush=True)
    if count >= TOTAL_MOVIES:
        print("\nIngestion complete !")
        break
    time.sleep(1)