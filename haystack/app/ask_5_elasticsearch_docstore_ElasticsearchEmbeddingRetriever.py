''' https://docs.haystack.deepset.ai/v2.0/docs/elasticsearchembeddingretriever '''
from elasticsearch_haystack.embedding_retriever import ElasticsearchEmbeddingRetriever
from elasticsearch_haystack.document_store import ElasticsearchDocumentStore
from haystack import Pipeline
from haystack.components.embedders import SentenceTransformersTextEmbedder

document_store = ElasticsearchDocumentStore(hosts="http://localhost:9200/")

model_name_or_path = "sentence-transformers/multi-qa-mpnet-base-dot-v1"
#model_name_or_path = "BAAI/bge-large-en-v1.5"
#model_name_or_path = "jphme/em_german_leo_mistral"

query_pipeline = Pipeline()
query_pipeline.add_component("text_embedder", SentenceTransformersTextEmbedder(model_name_or_path=model_name_or_path))
query_pipeline.add_component("retriever", ElasticsearchEmbeddingRetriever(document_store=document_store))
query_pipeline.connect("text_embedder.embedding", "retriever.query_embedding")

query = "AHV?"

result = query_pipeline.run({"text_embedder": {"text": query}})

print(result['retriever']['documents'][0].content)