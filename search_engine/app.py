from flask import Flask, request, jsonify, render_template
from elasticsearch import Elasticsearch
import os

app = Flask(__name__)
es = Elasticsearch(os.getenv("ES_HOST", "http://localhost:9200"))
INDEX = "movies_clean"


def _build_query(q, lang, genre, year, score):
    must = (
        [{"multi_match": {"query": q, "fields": ["title^3", "overview"], "type": "best_fields", "fuzziness": "AUTO"}}]
        if q
        else [{"match_all": {}}]
    )
    filters = [{"range": {"vote_count": {"gte": 50}}}]
    if lang:
        filters.append({"term": {"original_language": lang}})
    if genre:
        filters.append({"term": {"genres": genre}})
    if year:
        # @timestamp is the parsed date field (type: date); release_date is keyword — range on keyword is lexicographic only
        filters.append({"range": {"@timestamp": {"gte": f"{year}-01-01", "lte": f"{year}-12-31"}}})
    if score is not None:
        filters.append({"range": {"vote_average": {"gte": score}}})
    return {"bool": {"must": must, "filter": filters}}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search")
def search():
    q = request.args.get("q", "").strip()
    lang = request.args.get("lang", "").strip()
    genre = request.args.get("genre", "").strip()
    year = request.args.get("year", "").strip()

    try:
        score = float(request.args.get("score", "").strip()) if request.args.get("score", "").strip() else None
    except ValueError:
        score = None

    try:
        page = max(int(request.args.get("page", 1)), 1)
    except ValueError:
        page = 1

    size = 20
    from_offset = min((page - 1) * size, 9980)  # ES default max from+size = 10000

    body = {
        "query": _build_query(q, lang, genre, year, score),
        "size": size,
        "from": from_offset,
        "sort": [{"popularity": {"order": "desc"}}] if not q else ["_score"],
        "_source": ["title", "overview", "release_date", "vote_average", "vote_count",
                    "original_language", "genres", "poster_path", "popularity", "id"],
    }

    try:
        res = es.search(index=INDEX, **body)
    except Exception as e:
        return jsonify({"error": str(e), "total": 0, "hits": []}), 500

    hits = [h["_source"] for h in res["hits"]["hits"]]
    total = res["hits"]["total"]["value"]
    return jsonify({"total": total, "hits": hits, "page": page, "pages": (total + size - 1) // size})


@app.route("/facets")
def facets():
    body = {
        "size": 0,
        "aggs": {
            "languages": {"terms": {"field": "original_language", "size": 30}},
            "genres": {"terms": {"field": "genres", "size": 50}},
        },
    }
    try:
        res = es.search(index=INDEX, **body)
        return jsonify({
            "languages": [b["key"] for b in res["aggregations"]["languages"]["buckets"]],
            "genres": [b["key"] for b in res["aggregations"]["genres"]["buckets"]],
        })
    except Exception as e:
        return jsonify({"languages": [], "genres": [], "error": str(e)})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
