# Data Cleaning — F3

This document covers the cleaning rules applied to transform `movies_raw` into `movies_clean`, and the before/after impact of each rule.

---

## Source and context

The raw dataset is a 769,632-row CSV of movie metadata (20 columns). Logstash ingests it and routes each event through two paths simultaneously: one copy lands in `movies_raw` with minimal transformation (basic type casting only), and a cleaned copy lands in `movies_clean`.

The cleaning pipeline runs inside the same Logstash process using the `clone` filter. The original event goes to `movies_raw`; the clone gets the full cleaning treatment before going to `movies_clean`.

---

## Before / after counts

| Index | Documents | Notes |
|-------|-----------|-------|
| CSV source | 769,632 rows | header excluded |
| `movies_raw` | 662,083 docs | 107,549 rows rejected by Logstash (malformed CSV lines — 14.0%) |
| `movies_clean` | 662,077 docs | 6 additional rows dropped by cleaning rules |

The 107,549 rows rejected at ingestion are malformed CSV lines — fields split across multiple lines due to unescaped newlines in text fields like `overview`. These never reach either index.

The 6 rows dropped during cleaning had a missing or empty `id` or `title` field after parsing. Without a valid `id` there is no document key; without a `title` the record has no analytical value.

---

## Cleaning rules

### Rule 1 — Drop records with missing id or title

**Filter step:** STEP 7  
**Condition:** `id` is absent or empty, or `title` is absent or empty  
**Action:** `drop {}`  
**Applied to:** `movies_clean` clone only — `movies_raw` keeps all parsed rows  

**Impact:** 6 rows removed  

These rows passed CSV parsing but had no usable identifier or name. Keeping them would pollute aggregations and make document lookup by id unreliable.

---

### Rule 2 — Split dash-separated fields into arrays

**Filter step:** STEP 8  
**Fields affected:** `genres`, `keywords`, `credits`, `production_companies`  
**Action:** `mutate { split => { "field" => "-" } }`  
**Applied to:** `movies_clean` clone only  

**Impact:** all 662,077 documents — those fields change from a single string to an array of strings  

In the source CSV, multi-value fields are encoded as dash-separated strings (e.g. `Action-Comedy-Drama`, `Warner Bros-Universal`). Splitting them into arrays makes terms aggregations and exact filters work correctly in Elasticsearch.

**Known limitation:** the `credits` field contains hyphenated names such as `Jean-Claude Van Damme` or `Daniel Day-Lewis`. Splitting on `-` breaks these names into fragments. This affects a subset of records and is a known trade-off of the encoding format used in the source data. The impact is documented but not corrected — a future improvement would require a different delimiter or a dedicated name parser.

---

### Rule 3 — Recast numeric fields to integer

**Filter step:** STEP 9  
**Fields affected:** `budget`, `revenue`, `runtime`  
**Action:** `mutate { convert => { "field" => "integer" } }`  
**Applied to:** `movies_clean` clone only  

**Impact:** all 662,077 documents — those fields change type from float to integer  

In `movies_raw`, `budget`, `revenue`, and `runtime` are stored as floats (permissive casting at ingestion time). For `movies_clean` they are cast to integers — they represent whole currency amounts and minutes, so decimal precision adds no information and wastes storage.

---

## Fields unchanged between raw and clean

All other fields carry over from `movies_raw` to `movies_clean` without modification:

- `id`, `title`, `original_language`, `overview`, `tagline`, `poster_path`, `backdrop_path`, `recommendations`, `status` — kept as-is
- `popularity`, `vote_average` — kept as float
- `vote_count` — kept as integer
- `release_date` — kept as string; `@timestamp` holds the parsed date
- `tags` — Logstash failure tags, kept for diagnostics

---

## Pipeline implementation

Cleaning is implemented in `logstash/pipeline/logstash.conf`, STEP 6 through STEP 9.

The `clone` filter uses `add_field => { "[@metadata][target]" => "movies_clean" }` to mark the clone. This metadata field drives all downstream conditionals and the output routing. The `[type]` field from the clone filter is not used — in Logstash 8.13 with ECS v8, `[type]` is not evaluated correctly in output conditionals, causing both events to route to the same index.
