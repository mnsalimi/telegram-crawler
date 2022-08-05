from datetime import datetime
from elasticsearch import Elasticsearch
import warnings
warnings.filterwarnings('ignore')
es = Elasticsearch()

# doc = {
#     'author': 'kimchy',
#     'text': 'Elasticsearch: cool. bonsai cool.',
#     'timestamp': datetime.now(),
# }
# resp = es.index(index="test-index", id=1, document=doc)
# print(resp['result'])


# res = es.indices.get_alias("*")
# print(res)

res = es.search(index="posts", doc_type="_doc", body = {
'size' : 100,
'query': {
    'match_all' : {}
}
})

# resp = es.get(index="cars", id=1)
print(res)
# print(resp['_source'])

# es.indices.refresh(index="test-index")

# resp = es.search(index="test-index", query={"match_all": {}})
# print("Got %d Hits:" % resp['hits']['total']['value'])
# for hit in resp['hits']['hits']:
#     print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])