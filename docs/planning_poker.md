# Planning Poker

Fibonacci scale used: 1, 2, 3, 5, 8, 13, 21.

Session held at project kickoff, April 2026. Estimates reflect complexity and uncertainty at time of planning, not actual hours spent.

## Backlog

| Feature | Description | Estimate | Assignee | Status |
|---|---|---|---|---|
| F1 Bootstrap ELK stack | Docker Compose setup: Elasticsearch, Logstash, Kibana. Healthchecks, volume mounts, heap tuning, network. | 5 | Youssef El Hajji | Done |
| F2 Raw CSV ingestion | Logstash pipeline: CSV parse, type casting, sincedb, idempotent output to `movies_raw`. Tag on failure. | 8 | Ayoub Azacri| Done |
| F3 Data cleaning pipeline | Build `movies_clean`. Null handling, type coercion, dash-split arrays, drop malformed rows. | 13 | Omar Hakik | Done |
| F4 Explicit mapping | Define and apply explicit ES mapping for `movies_clean`: custom analyzer, `keyword`/`text` split, strict types. Reindex from `movies_raw`. | 8 | Omar Hakik | Done |
| F5 Analytical DSL queries | 12 commented DSL queries in `docs/queries.md`. At least 5 must be `bool` queries. Required topics: top 10 by popularity, by language, budget + rating filter, full-text on title, aggregation by genre. | 5 | Ayoub Azacri| Done |
| F6 Kibana dashboard | 6 visualizations: genre pie, films per year line, top 10 popularity bar, rating histogram, average budget by genre bar, language pie. Assembled into 1 dashboard. Export as `kibana_export.ndjson`. | 8 | Youssef DEKHAIL | Done |
| F7 Documentation | `data_dictionary.md`, `data_cleaning.md`, `runbook.md`, `planning_poker.md`, `projet_management.md`, `demo_script.md`. | 5 | Youssef DEKHAIL| Done |
| F8 Search engine | Full-text search on `title` and `overview`. At least one exact filter (language, genre, or year). Free choice of tech (API or UI). | 13 | Youssef El Hajji | Done |

## Total estimate

62 points across 8 features.

## Notes on estimates

F3 got the highest estimate (13) because cleaning an unknown dataset is always unpredictable. You do not know how many nulls, type mismatches, or encoding issues exist until you look at the data. It ended up warranting the score.

F8 also got 13. Building a working search UI or API on top of ES is straightforward in principle, but integrating filters, handling edge cases, and making it actually usable takes time.

F5 got 5 because the queries themselves are not complex once the mapping is in place. The main dependency was F4.

## Related files

[[projet_management.md]] [[queries.md]] [[data_cleaning.md]]