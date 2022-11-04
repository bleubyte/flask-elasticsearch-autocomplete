from elasticsearch import Elasticsearch

import yaml


es = Elasticsearch(hosts=["http://127.0.0.1:9200"])

print(f"Connected to ElasticSearch cluster `{es.info().body['cluster_name']}`")

with open('findings.yml', 'r') as file:
    for doc in yaml.safe_load_all(file):
        document = {
                    "title": doc['title'],
                    "description": doc['description'],
                }
        es.index(index="findings", document=document)

