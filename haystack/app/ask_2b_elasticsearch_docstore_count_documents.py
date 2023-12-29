''' This script is used to check if the documents are stored in the Elasticsearch Document Store. '''
from elasticsearch_haystack.document_store import ElasticsearchDocumentStore
from haystack import Document

document_store = ElasticsearchDocumentStore(hosts = "http://localhost:9200")
print(document_store.count_documents())
