# F5 — Analytical DSL Queries

This file contains 12 verified DSL queries for the `movies_clean` index. They follow the formatting and technical standards required for the Master Data & AI exam project (ES 8.13).

---

## How to run these queries

**Option 1 — Kibana Dev Tools (recommended)**
1. Open http://localhost:5601
2. Go to **Menu → Management → Dev Tools**
3. Paste any query from this file into the left panel
4. Click the green play button (or press `Ctrl+Enter`)

**Option 2 — curl**
```bash
curl -s -XGET "http://localhost:9200/movies_clean/_search?pretty" \
  -H "Content-Type: application/json" \
  -d '<paste query body here>'
```

---

### 1. Top 10 films by popularity

**Goal:** Identify the films with the highest audience reach and engagement scores.
**Type:** Sort

```json
{
  "size": 10,
  "sort": [
    { "popularity": { "order": "desc" } }
  ],
  "_source": ["title", "popularity", "release_date", "vote_average"]
}
```

**Expected:** Top 10 documents sorted by `popularity` descending.

---

### 2. Global film distribution by language

**Goal:** Understand the linguistic diversity of the dataset by counting movies per original language.
**Type:** Aggregation

```json
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

**Expected:** A list of buckets containing language codes (e.g., "en", "fr") and their respective document counts.

---

### 3. Blockbuster quality filter (Budget vs. Rating)

**Goal:** Find high-budget films that also achieved critical acclaim, using a vote floor to ensure statistical significance.
**Type:** bool (Filter)

```json
{
  "size": 20,
  "query": {
    "bool": {
      "filter": [
        { "range": { "budget":       { "gt": 1000000 } } },
        { "range": { "vote_average": { "gt": 7 } } },
        { "range": { "vote_count":   { "gte": 500 } } }
      ]
    }
  },
  "sort": [{ "vote_average": { "order": "desc" } }],
  "_source": ["title", "budget", "vote_average", "vote_count"]
}
```

**Expected:** 20 highly-rated movies with budgets over 1 million, excluding obscure titles with few votes.

---

### 4. Full-text search on title with fuzziness

**Goal:** Allow users to find movies even if they make slight spelling mistakes in the title.
**Type:** match

```json
{
  "size": 10,
  "query": {
    "match": {
      "title": {
        "query": "dark knight",
        "fuzziness": "AUTO"
      }
    }
  },
  "_source": ["title", "overview", "vote_average", "release_date"]
}
```

**Expected:** Results matching "Dark Knight" or similar terms, sorted by relevance score.

---

### 5. Genre-based market share

**Goal:** Determine which genres are most prevalent in the movie industry.
**Type:** Aggregation

```json
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

**Expected:** Buckets for each genre (Action, Comedy, etc.) with the count of movies belonging to them.

---

### 6. Modern hits (Post-2010 acclaim)

**Goal:** Identify well-known movies released in the last decade that have maintained high engagement.
**Type:** bool (Filter)

```json
{
  "size": 20,
  "query": {
    "bool": {
      "filter": [
        { "range": { "@timestamp": { "gte": "2010-01-01" } } },
        { "range": { "vote_count": { "gt": 2000 } } }
      ]
    }
  },
  "sort": [{ "vote_count": { "order": "desc" } }],
  "_source": ["title", "release_date", "vote_count", "vote_average"]
}
```

**Expected:** A list of 20 modern films sorted by the number of user votes.

---

### 7. Net Profitability Analysis

**Goal:** Calculate the financial success of films by subtracting budget from revenue, excluding documents with missing financial data.
**Type:** bool (Filter) + Scripted Sort

```json
{
  "size": 10,
  "query": {
    "bool": {
      "filter": [
        { "range": { "budget": { "gt": 1000000 } } },
        { "range": { "revenue": { "gt": 0 } } }
      ]
    }
  },
  "sort": [
    {
      "_script": {
        "type": "number",
        "script": {
          "source": "doc['revenue'].value - doc['budget'].value"
        },
        "order": "desc"
      }
    }
  ],
  "_source": ["title", "revenue", "budget"]
}
```

**Expected:** Top 10 films with the highest net profit (Revenue - Budget).

---

### 8. Critical reception by genre

**Goal:** Find which genres generally receive the highest average ratings from viewers.
**Type:** Aggregation (Nested)

```json
{
  "size": 0,
  "query": {
    "range": { "vote_count": { "gte": 100 } }
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

**Expected:** Average `vote_average` calculated for each genre, excluding low-vote outliers.

---

### 9. High-Rated Action Cinema

**Goal:** Target a specific niche: high-quality Action movies for fans of the genre.
**Type:** bool (Filter)

```json
{
  "size": 20,
  "query": {
    "bool": {
      "filter": [
        { "term":  { "genres": "Action" } },
        { "range": { "vote_average": { "gte": 8.0 } } },
        { "range": { "vote_count":   { "gte": 200 } } }
      ]
    }
  },
  "sort": [{ "vote_average": { "order": "desc" } }],
  "_source": ["title", "genres", "vote_average"]
}
```

**Expected:** Top-rated Action movies with a significant number of reviews.

---

### 10. Multi-field search (Title and Overview)

**Goal:** Increase search recall by looking for keywords in both the movie title and its plot description.
**Type:** bool (Should)

```json
{
  "size": 10,
  "query": {
    "bool": {
      "should": [
        { "match": { "title": { "query": "space travel", "boost": 2 } } },
        { "match": { "overview": "space travel" } }
      ]
    }
  },
  "_source": ["title", "overview"]
}
```

**Expected:** Movies that mention "space travel" in either the title (weighted higher) or the description.

---

### 11. Top Revenue-Generating Production Companies

**Goal:** Identify which studios or production companies have the highest total gross revenue.
**Type:** Aggregation

```json
{
  "size": 0,
  "aggs": {
    "top_companies": {
      "terms": {
        "field": "production_companies",
        "size": 10,
        "order": { "total_revenue": "desc" }
      },
      "aggs": {
        "total_revenue": {
          "sum": { "field": "revenue" }
        }
      }
    }
  }
}
```

**Expected:** A list of the top 10 production companies sorted by their cumulative revenue.

---

### 12. Film length distribution

**Goal:** Analyze the standard duration of movies in the dataset.
**Type:** Aggregation (Histogram)

```json
{
  "size": 0,
  "query": {
    "range": { "runtime": { "gt": 0 } }
  },
  "aggs": {
    "runtime_distribution": {
      "histogram": {
        "field": "runtime",
        "interval": 30,
        "min_doc_count": 1
      }
    }
  }
}
```

**Expected:** Document counts grouped by 30-minute runtime intervals (e.g., 90m, 120m, 150m).
