# Data Ingestion Proof — movies_raw

## 1. Document count

curl http://localhost:9200/movies_raw/_count

Résultat :
{"count":662083,"_shards":{"total":1,"successful":1,"skipped":0,"failed":0}}

## 2. Index status

curl "http://localhost:9200/_cat/indices/movies_raw?v"

Résultat :
health status index      uuid                   pri rep docs.count docs.deleted store.size pri.store.size dataset.size
green  open   movies_raw GNrQ6Y0jSfaO8PBXI7svsw   1   0     662083        81474        1gb            1gb          1gb

## 3. Sample document

curl http://localhost:9200/movies_raw/_search?pretty -H "Content-Type: application/json" -d '{"size": 1}'

Résultat :
{
  "took" : 2,
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
        "_id" : "640923",
        "_score" : 1.0,
        "_ignored" : [
          "credits.keyword"
        ],
        "_source" : {
          "id" : 640923,
          "title" : "Kidz",
          "genres" : "Comedy",
          "original_language" : "it",
          "overview" : "Sara and Nicola are expecting their second son. Through the late Mattia Torre's sharp look all the joys and sorrows of being a parent in the modern day Italy are unraveled in an absolutely brilliant and witty way.",
          "popularity" : 5.296,
          "production_companies" : "Wildside-Vision Distribution-The Apartment-Sky Italia-Amazon Studios",
          "release_date" : "2020-01-23",
          "release_date_raw" : "2020-01-23",
          "@timestamp" : "2020-01-23T00:00:00.000Z",
          "budget" : 0.0,
          "revenue" : 3700000.0,
          "runtime" : 98.0,
          "status" : "Released",
          "tagline" : null,
          "vote_average" : 5.9,
          "vote_count" : 315,
          "credits" : "Valerio Mastandrea-Paola Cortellesi-Stefano Fresi-Valerio Aprea-Paolo Calabresi-Andrea Sartoretti-Massimo De Lorenzo-Gianfelice Imparato-Carlo Luca De Ruggieri-Betti Pedrazzi-Giorgio Barchiesi-Cristina Pellegrino-Arianna Dell'Arti-Riccardo Goretti-Daria Deflorian",
          "keywords" : "parenthood",
          "poster_path" : "/w5hEwTG2P9YKn0SYpaxjeLei28h.jpg",
          "backdrop_path" : "/984bqrN5ni3fMzPRcDmk3BKiD2T.jpg",
          "recommendations" : "606954-614292-640915-606312-606952-614418-614427-571485-624484-575568-563907-630220-593660-141810-56783-625501-60046-419372-608649-608655-583029"
        }
      }
    ]
  }
}

## 4. Missing documents

- Total lignes dans le CSV : 769,632
- Indexés avec succès : 662,083 (86%)
- Ignorés : 107,549 (14%)

Cause : lignes CSV malformées -- virgules dans des champs non protégés, encodage cassé, ou colonnes manquantes.
