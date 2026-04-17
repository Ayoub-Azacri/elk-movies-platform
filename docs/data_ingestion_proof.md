# Data Ingestion Proof — movies_raw

## 1. Document count

curl http://localhost:9200/movies_raw/_count

Résultat :
{"count":662083,"_shards":{"total":1,"successful":1,"skipped":0,"failed":0}}%

## 2. Index status

curl "http://localhost:9200/_cat/indices/movies_raw?v"

Résultat :
health status index      uuid                   pri rep docs.count docs.deleted store.size pri.store.size dataset.size
green  open   movies_raw vubIM9lnReK9ajXZgBHYQA   1   0     662083        58086   1006.4mb       1006.4mb     1006.4mb

## 3. Sample document

curl http://localhost:9200/movies_raw/_search?pretty -H "Content-Type: application/json" -d '{"size": 1}'

Résultat : {

              "took" : 13,
              "timed_out" : false,
              "_shards" : {
                "total" : 1,
                "successful" : 1,
                "skipped" : 0,
                "failed" : 0
              },
              "hits" : {
                "total" : {
                  "value" : 10000,
                  "relation" : "gte"
                },
                "max_score" : 1.0,
                "hits" : [
                  {
                    "_index" : "movies_raw",
                    "_id" : "424783",
                    "_score" : 1.0,
                    "_ignored" : [
                      "credits.keyword",
                      "overview.keyword"
                    ],
                    "_source" : {
                      "title" : "Bumblebee",
                      "status" : "Released",
                      "genres" : "Action-Adventure-Science Fiction",
                      "vote_average" : 6.7,
                      "poster_path" : "/fw02ONlDhrYjTSZV8XO6hhU3ds3.jpg",
                      "release_date_raw" : "2018-12-15",
                      "keywords" : "technology-based on toy-transformers-robot-spin off-1980s-autobot",
                      "runtime" : 114.0,
                      "overview" : "On the run in the year 1987 Bumblebee finds refuge in a junkyard in a small Californian beach town. Charlie on the cusp of turning 18 and trying to find her place in the world discovers Bumblebee battle-scarred and broken.  When Charlie revives him she quickly learns this is no ordinary yellow VW bug.",
                      "recommendations" : "297802-428078-324857-335983-287947-375588-399579-299537-404368-335988-480530-363088-338952-450465-166428-400650-383498-268896-299534-456740-280217",
                      "revenue" : 4.67989645E8,
                      "production_companies" : "Paramount-Allspark Pictures-Bay Films-Di Bonaventura Pictures-Tom DeSanto/Don Murphy Production",
                      "original_language" : "en",
                      "@timestamp" : "2026-04-16T19:25:25.368324002Z",
                      "popularity" : 58.658,
                      "budget" : 1.35E8,
                      "tagline" : "Every hero has a beginning.",
                      "credits" : "Hailee Steinfeld-John Cena-Jorge Lendeborg Jr.-John Ortiz-Jason Ian Drucker-Pamela Adlon-Stephen Schneider-Len Cariou-Glynn Turman-Gracie Dzienny-Ricardo Hoyos-Lenny Jacobson-Megyn Price-Kollin Holtz-Fred Dryer-Isabelle Ellingson-Mika Kubo-Felicia Stiles-George Anagnostou-Brandon Wardle-Krystin Goodwin-Nick Pilla-Sachin Bhatt-Tim Martin Gleason-David Waters-Antonio D. Charity-Courtney Coker-Edwin Hodge-Jake Huang-Holland Diaz-Dave Cutler-Lars Slind-Dylan O'Brien-Peter Cullen-Angela Bassett-Justin Theroux-David Sobolov-Grey DeLisle-Jon Bailey-Steve Blum-Andrew Morgado-Kirk Baily-Dennis Singletary-Vanessa Ross-Tony Toste-Nico Abiera-Jiana Alvarez-Jace Areff-Manny Avina-William W. Barbour-Jesse Stoudt-DeMark Thompson-John Lobato-Ed Moy",
                      "backdrop_path" : "/17nDJQsGVim6oows2TlN98UacbO.jpg",
                      "id" : 424783,
                      "release_date" : "2018-12-15T00:00:00.000Z",
                      "vote_count" : 4999
                    }
                  }
                ]
              }
            }

## 4. Missing documents

- Total lines in CSV : 769,632
- Successfully indexed : 662,083 (86%)
- Missing : 107,549 (14%)

Cause : malformed CSV lines — commas inside unquoted fields, broken
encoding, or missing required columns. Full analysis in data_cleaning.md.