'''
This is a modified version of the original flask-elasticsearch-autocomplete https://github.com/ahnaf-zamil/flask-elasticsearch-autocomplete
Credits go to ahnaf-zamil @DevGuyAhnaf 
'''
from flask import Flask, request, render_template
from elasticsearch import Elasticsearch

es = Elasticsearch(hosts=["http://127.0.0.1:9200"])
print(f"Connected to ElasticSearch cluster `{es.info().body['cluster_name']}`")

app = Flask(__name__)

MAX_SIZE = 15

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/search")
def search_autocomplete():
    query = request.args["q"].lower()
    tokens = query.split(" ")
    # Search findings description text and return the title 
    clauses = [
        {
            "span_multi": {
                "match": {"fuzzy": {"description": {"value": i, "fuzziness": "AUTO"}}}
            }
        }
        for i in tokens
    ]

    payload = {
        "bool": {
            "must": [{"span_near": {"clauses": clauses, "slop": 0, "in_order": False}}]
        }
    }

    resp = es.search(index="findings", query=payload, size=MAX_SIZE)
    # We return the title
    return [result['_source']['title'] for result in resp['hits']['hits']]
    

if __name__ == "__main__":
    app.run(debug=True)
