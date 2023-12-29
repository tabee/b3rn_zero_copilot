import os
from haystack import Document
from haystack.document_stores import InMemoryDocumentStore
from haystack.pipeline_utils import build_rag_pipeline
from haystack.document_stores import InMemoryDocumentStore
from haystack.pipeline_utils import build_rag_pipeline, build_indexing_pipeline
from haystack.pipeline_utils.indexing import download_files

API_KEY = "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"
print(API_KEY)

# We are model agnostic :) In this getting started you can choose any OpenAI or Huggingface TGI generation model
generation_model = "gpt-3.5-turbo"

# We support many different databases. Here, we load a simple and lightweight in-memory database.
document_store = InMemoryDocumentStore()


# Download example files from web
files = download_files(sources=[
    "https://www.eak.admin.ch/eak/de/home/dokumentation/pensionierung/altersrente.html",
    "https://www.eak.admin.ch/eak/de/home/reform-ahv21/ueberblick/ausgleichsmassnahmen.html"])

# Pipelines are our main abstratcion.
# Here we create a pipeline that can index TXT and HTML. You can also use your own private files.
indexing_pipeline = build_indexing_pipeline(
    document_store=document_store,
    embedding_model="intfloat/e5-base-v2",
    supported_mime_types=["text/plain", "text/html"],  # "application/pdf"
)
indexing_pipeline.run(files=files)  # you can also supply files=[path_to_directory], which is searched recursively

# RAG pipeline with vector-based retriever + LLM
rag_pipeline = build_rag_pipeline(
    document_store=document_store,
    embedding_model="intfloat/e5-base-v2",
    generation_model=generation_model,
    llm_api_key=API_KEY,
)

# For details, like which documents were used to generate the answer, look into the result object
result = rag_pipeline.run(query="Wie wird eine Altersrente berechnet? Erwähne alles")
print(result.data)