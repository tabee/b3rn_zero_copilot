from elasticsearch_haystack.document_store import ElasticsearchDocumentStore
from haystack.pipeline import Pipeline
from haystack.components.embedders import SentenceTransformersTextEmbedder 
from elasticsearch_haystack.embedding_retriever import ElasticsearchEmbeddingRetriever

model_name_or_path = "sentence-transformers/multi-qa-mpnet-base-dot-v1"

document_store = ElasticsearchDocumentStore(hosts = "http://localhost:9200")


retriever = ElasticsearchEmbeddingRetriever(document_store=document_store)
text_embedder = SentenceTransformersTextEmbedder(model_name_or_path=model_name_or_path)

query_pipeline = Pipeline()
query_pipeline.add_component("text_embedder", text_embedder)
query_pipeline.add_component("retriever", retriever)
query_pipeline.connect("text_embedder.embedding", "retriever.query_embedding")

result = query_pipeline.run({"text_embedder": {"text": "Altersrente"}})

# http://localhost:9200/_search?q=Altersrente
print(result)
