# Data Dictionary — `movies_raw` / `movies_clean`

Source: `DATA/movies.csv` — 769,632 rows, 20 columns, Kaggle movies metadata.
After ingestion: 662,083 docs in `movies_raw`. 107,549 rows dropped (malformed CSV lines).

Type column shows the field type in `movies_clean` (explicit mapping). Where `movies_raw` differs, it is noted in the Notes column.

| Field | ES Type | Description | Example | Nulls / Anomalies |
|---|---|---|---|---|
| `id` | `integer` | Unique movie ID from the source dataset. Used as `document_id` in ES — reruns are idempotent. | `550` | No nulls observed. Treat as primary key. |
| `title` | `text` (english analyzer) | Movie title. Supports full-text search. | `"Fight Club"` | Some titles contain special characters or non-ASCII. A few are empty strings. |
| `genres` | `keyword[]` | Genre tags. Dash-separated in CSV; split by Logstash. Each tag is a separate keyword. | `["Action", "Comedy"]` | Many films have no genre. The dash separator breaks hyphenated genre names, but genre names are rarely hyphenated. |
| `original_language` | `keyword` | ISO 639-1 language code. Used for exact-match filters and aggregations. | `"en"`, `"fr"`, `"ja"` | A small number of rows have non-standard codes or empty values. |
| `overview` | `text` (english analyzer) | Plot summary. Supports full-text search. | `"An insomniac office worker..."` | High null rate. Many entries are empty strings rather than true nulls. |
| `popularity` | `float` | Kaggle popularity score. No fixed upper bound. | `87.4`, `3245.2` | Several films have scores above 3000 — likely data anomalies. Distribution is heavily right-skewed. |
| `production_companies` | `keyword[]` | Production company names. Dash-separated in CSV; split by Logstash. | `["Warner Bros", "Legendary"]` | Hyphenated company names (e.g. "20th-Century-Fox") are broken by the dash split. This is ugly but it is what the dataset gave us. |
| `release_date` | `date` (yyyy-MM-dd) | Release date. Parsed into `@timestamp` by Logstash. Raw value kept in `release_date_raw`. | `"1999-10-15"` | Some dates are malformed or missing, triggering `_date_parse_failure` tags. |
| `release_date_raw` | `keyword` | Original release date string before date parsing. Not in source CSV — added by Logstash filter. | `"1999-10-15"` | Present only when `release_date` parses successfully. |
| `budget` | `integer` | Film budget in USD. `float` in `movies_raw` (Logstash default). | `63000000` | A large share of entries are `0`, which means the data is missing, not that the film had no budget. Do not treat zero as a valid budget. |
| `revenue` | `integer` | Box office revenue in USD. `float` in `movies_raw`. | `100853753` | Same zero-means-missing problem as `budget`. |
| `runtime` | `integer` | Film duration in minutes. `float` in `movies_raw`. | `139` | Zero values present — missing data, not zero-length films. A handful exceed 600 minutes. |
| `status` | `keyword` | Production status at the time of the data snapshot. | `"Released"`, `"Post Production"`, `"Rumored"` | A small number have blank or non-standard values. |
| `tagline` | `text` | Short marketing phrase. Not used for aggregations. | `"Mischief. Mayhem. Soap."` | High null rate. Many rows have an empty string instead of null. |
| `vote_average` | `float` | Average user rating on a 0–10 scale. | `8.4` | Some films have a score of `0.0` with a `vote_count` of `0` — these are unrated, not bad. Filter them out for any rating analysis. |
| `vote_count` | `integer` | Number of user votes. | `26280` | Many films have only 1 vote. Ratings from single-vote entries are statistically meaningless. Queries involving ratings should include a `vote_count` floor (e.g. `>= 100`). |
| `credits` | `keyword[]` | Actor and director names. Dash-separated in CSV; split by Logstash. | `["Brad Pitt", "Edward Norton"]` | Hyphenated names (e.g. "Jean-Pierre Jeunet") are broken into separate tokens by the dash split. Known issue with no clean fix at the Logstash level. |
| `keywords` | `keyword[]` | Thematic tags. Dash-separated in CSV; split by Logstash. | `["neo-noir", "twist ending"]` | Hyphenated keywords are also broken. Many films have no keywords. |
| `poster_path` | `keyword` | Relative URL path to the poster image. Prepend `https://image.tmdb.org/t/p/w500` to build a full URL. | `"/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg"` | Some rows have null or empty paths. |
| `backdrop_path` | `keyword` | Relative URL path to the backdrop image. Same URL base as `poster_path`. | `"/fCayJrkfRaCRCTh8GqN30f8oyQF.jpg"` | Higher null rate than `poster_path`. |
| `recommendations` | `keyword` | Comma-separated list of related movie IDs. Not split into an array. | `"11,245,550,680"` | Format is inconsistent across rows. Not used in any current query or visualization. |

## Notes on type differences between `movies_raw` and `movies_clean`

In `movies_raw`, Logstash dynamic mapping stored `budget`, `revenue`, and `runtime` as `float`. The explicit mapping on `movies_clean` corrects these to `integer`. The `genres`, `production_companies`, `credits`, and `keywords` fields are indexed as `keyword` arrays after the dash-split.

## Related files

[[data_cleaning.md]] [[queries.md]]