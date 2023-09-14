curl -XPUT http://${HOST}:${PORT}/movies -H 'Content-Type: application/json' -d @es_indexes/film.json
curl -XPUT http://${HOST}:${PORT}/genre -H 'Content-Type: application/json' -d @es_indexes/genre.json
curl -XPUT http://${HOST}:${PORT}/person -H 'Content-Type: application/json' -d @es_indexes/person.json