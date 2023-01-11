from elasticsearch_dsl import connections
from elasticsearch import Elasticsearch

connections.create_connection(hosts=['localhost'], timeout=100)
client = Elasticsearch()



