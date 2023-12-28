from elasticsearch_haystack.document_store import ElasticsearchDocumentStore
from haystack.components.embedders import SentenceTransformersDocumentEmbedder
from haystack.components.converters import TextFileToDocument
from haystack.components.preprocessors import DocumentSplitter
from haystack.components.writers import DocumentWriter
from haystack.pipeline_utils import build_indexing_pipeline
from haystack.pipeline_utils.indexing import download_files

document_store = ElasticsearchDocumentStore(hosts = "http://localhost:9200")
converter = TextFileToDocument()
splitter = DocumentSplitter()
doc_embedder = SentenceTransformersDocumentEmbedder(model_name_or_path="sentence-transformers/multi-qa-mpnet-base-dot-v1")
writer = DocumentWriter(document_store)

# Download example files from web
files = download_files(sources=[
    #"https://www.eak.admin.ch/eak/de/home/dokumentation/pensionierung/altersrente.html",
    #"https://www.eak.admin.ch/eak/de/home/reform-ahv21/ueberblick/ausgleichsmassnahmen.html",
    "https://bee-gu.ch/geschichte.html",])

# Pipelines are our main abstratcion.
# Here we create a pipeline that can index TXT and HTML. You can also use your own private files.
indexing_pipeline = build_indexing_pipeline(
    document_store=document_store,
    embedding_model="intfloat/e5-base-v2",
    supported_mime_types=["text/plain", "text/html"],  # "application/pdf"
)
indexing_pipeline.run(files=files)  # you can also supply files=[path_to_directory], which is searched recursively