# F5 — Analytical DSL Queries

All queries run against the `movies_clean` index.

---

## How to run these queries

**Option 1 — Kibana Dev Tools (recommended)**

1. Open http://localhost:5601
2. Go to **Menu → Management → Dev Tools**
3. Paste any query from this file into the left panel
4. Click the green play button (or press `Ctrl+Enter`)
5. Results appear in the right panel

**Option 2 — curl**

Replace the query body and run from terminal:

```bash
curl -s "http://localhost:9200/movies_clean/_search" \
  -H "Content-Type: application/json" \
  -d '<paste query body here>' | python3 -m json.tool
```

---

## Q1 — Top 10 films by popularity

Returns the 10 most popular films, sorted by the `popularity` field descending.

```json
GET /movies_clean/_search
{
  "size": 10,
  "sort": [
    { "popularity": { "order": "desc" } }
  ],
  "_source": ["title", "popularity", "release_date", "vote_average"]
}
```

---

## Q2 — Number of films by original language

Aggregation showing how many films exist per language, ordered by count.

```json
GET /movies_clean/_search
{
  "size": 0,
  "aggs": {
    "by_language": {
      "terms": {
        "field": "original_language",
        "size": 20
      }
    }
  }
}
```

---

## Q3 — Films with budget over 1M and rating above 7 (bool)

Uses a `bool` query with three `filter` clauses — range on `budget`, range on
`vote_average`, and a minimum `vote_count`. Without the vote count floor, films
with a single 10/10 rating surface at the top and make the results useless.

```json
GET /movies_clean/_search
{
  "size": 20,
  "query": {
    "bool": {
      "filter": [
        { "range": { "budget":       { "gt": 1000000 } } },
        { "range": { "vote_average": { "gt": 7 } } },
        { "range": { "vote_count":   { "gte": 100 } } }
      ]
    }
  },
  "sort": [{ "vote_average": { "order": "desc" } }],
  "_source": ["title", "budget", "vote_average", "vote_count", "release_date"]
}
```

---

## Q4 — Full-text search on title (bool)

Uses a `bool` query with a `must` clause containing a `match` on `title`.
The `english_movie_analyzer` applied at index time means stemming and stopword
removal are active — searching "running" will match "run", etc.

```json
GET /movies_clean/_search
{
  "size": 10,
  "query": {
    "bool": {
      "must": [
        { "match": { "title": "dark knight" } }
      ]
    }
  },
  "_source": ["title", "overview", "vote_average", "release_date"]
}
```

---

## Q5 — Number of films per genre

Aggregation on the `genres` keyword field. Because F3 split the dash-separated
string into an array, each genre value is counted independently.

```json
GET /movies_clean/_search
{
  "size": 0,
  "aggs": {
    "by_genre": {
      "terms": {
        "field": "genres",
        "size": 30
      }
    }
  }
}
```

---

## Q6 — Films released after 2010 with more than 1000 votes (bool)

`bool` with two `filter` clauses — date range on `@timestamp` and range on
`vote_count`. Only well-known recent films surface.

```json
GET /movies_clean/_search
{
  "size": 20,
  "query": {
    "bool": {
      "filter": [
        { "range": { "@timestamp": { "gte": "2010-01-01" } } },
        { "range": { "vote_count": { "gt": 1000 } } }
      ]
    }
  },
  "sort": [{ "vote_count": { "order": "desc" } }],
  "_source": ["title", "release_date", "vote_count", "vote_average"]
}
```

---

## Q7 — Top 10 films by revenue

Returns the 10 highest-grossing films. Excludes films with revenue = 0 since
missing revenue is stored as 0 in the source data.

```json
GET /movies_clean/_search
{
  "size": 10,
  "query": {
    "range": { "revenue": { "gt": 0 } }
  },
  "sort": [{ "revenue": { "order": "desc" } }],
  "_source": ["title", "revenue", "budget", "release_date"]
}
```

---

## Q8 — Average rating by genre

Terms aggregation on `genres` with a nested `avg` sub-aggregation on
`vote_average`. A base filter of `vote_count >= 50` is applied — without it,
films with 1–2 votes skew genre averages down to ~3.0 and the results tell
you nothing useful.

```json
GET /movies_clean/_search
{
  "size": 0,
  "query": {
    "range": { "vote_count": { "gte": 50 } }
  },
  "aggs": {
    "by_genre": {
      "terms": {
        "field": "genres",
        "size": 30
      },
      "aggs": {
        "avg_rating": {
          "avg": { "field": "vote_average" }
        }
      }
    }
  }
}
```

---

## Q9 — Action films with rating above 7.5 (bool)

`bool` query combining a `term` filter on the `genres` keyword field, a
`range` filter on `vote_average`, and a `vote_count` floor. Same reason as Q3 —
without a minimum vote count, obscure films with a single perfect vote dominate.

```json
GET /movies_clean/_search
{
  "size": 20,
  "query": {
    "bool": {
      "filter": [
        { "term":  { "genres": "Action" } },
        { "range": { "vote_average": { "gte": 7.5 } } },
        { "range": { "vote_count":   { "gte": 100 } } }
      ]
    }
  },
  "sort": [{ "vote_average": { "order": "desc" } }],
  "_source": ["title", "genres", "vote_average", "vote_count"]
}
```

---

## Q10 — Popular English-language films (bool)

`bool` query with `term` filter on `original_language` and `range` filter on
`popularity`. Isolates English films with significant audience reach.

```json
GET /movies_clean/_search
{
  "size": 20,
  "query": {
    "bool": {
      "filter": [
        { "term": { "original_language": "en" } },
        { "range": { "popularity": { "gte": 50 } } }
      ]
    }
  },
  "sort": [{ "popularity": { "order": "desc" } }],
  "_source": ["title", "original_language", "popularity", "vote_average"]
}
```

---

## Q11 — Full-text search on overview

`match` query on `overview` using the `english_movie_analyzer`. Useful for
finding films by plot description rather than title.

```json
GET /movies_clean/_search
{
  "size": 10,
  "query": {
    "match": {
      "overview": "space exploration mission"
    }
  },
  "_source": ["title", "overview", "vote_average", "release_date"]
}
```

---

## Q12 — Runtime distribution (histogram)

Histogram aggregation on `runtime` with a 15-minute interval. A base filter
excludes `runtime = 0` — missing runtime is stored as 0 in the source data,
and without the filter that bucket swamps everything else with 238k docs.

```json
GET /movies_clean/_search
{
  "size": 0,
  "query": {
    "range": { "runtime": { "gt": 0 } }
  },
  "aggs": {
    "runtime_distribution": {
      "histogram": {
        "field": "runtime",
        "interval": 15,
        "min_doc_count": 1
      }
    }
  }
}
```
