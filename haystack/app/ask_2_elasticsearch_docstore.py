
from elasticsearch_haystack.document_store import ElasticsearchDocumentStore
from haystack import Document

document_store = ElasticsearchDocumentStore(hosts = "http://localhost:9200")

#print(document_store.count_documents())
bm25_retrieval_results = document_store._bm25_retrieval(query="AHV", filters=None, top_k=1)
if bm25_retrieval_results:
    print(f"**************\n {bm25_retrieval_results[0].content} \n **************\n")
    print(f"File path: {bm25_retrieval_results[0].meta['file_path']}")