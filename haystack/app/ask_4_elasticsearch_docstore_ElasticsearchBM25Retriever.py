''' https://docs.haystack.deepset.ai/v2.0/docs/elasticsearchbm25retriever'''
import os
from pathlib import Path
from elasticsearch_haystack.bm25_retriever import ElasticsearchBM25Retriever
from elasticsearch_haystack.document_store import ElasticsearchDocumentStore
from haystack import Pipeline
from haystack.components.builders.answer_builder import AnswerBuilder
from haystack.components.builders.prompt_builder import PromptBuilder
from haystack.components.generators import GPTGenerator

# Get API key from environment variable
api_key = os.environ['OPENAI_API_KEY']

# Create a RAG query pipeline
prompt_template = """
    Given these documents, answer the question.\n 
    Aanswer always in german!\n
    Cite always 'file_path' in your answer.\n
    Documents:
    {% for doc in documents %}
        {{ doc.content }}
        {{ doc.meta }}
    {% endfor %}

    \nQuestion: {{question}}
    \nAnswer:
    """

document_store = ElasticsearchDocumentStore(hosts= "http://localhost:9200/")
retriever = ElasticsearchBM25Retriever(document_store=document_store)
rag_pipeline = Pipeline()
rag_pipeline.add_component(name="retriever", instance=retriever)
rag_pipeline.add_component(instance=PromptBuilder(template=prompt_template), name="prompt_builder")
rag_pipeline.add_component(instance=GPTGenerator(api_key=api_key), name="llm")
rag_pipeline.add_component(instance=AnswerBuilder(), name="answer_builder")
rag_pipeline.connect("retriever", "prompt_builder.documents")
rag_pipeline.connect("prompt_builder", "llm")
rag_pipeline.connect("llm.replies", "answer_builder.replies")
rag_pipeline.connect("llm.metadata", "answer_builder.metadata")
rag_pipeline.connect("retriever", "answer_builder.documents")

# Draw the pipeline
rag_pipeline.draw(Path("./rag_pipeline_ask_4_elasticsearch_docstore_ElasticsearchBM25Retriever.png"))

question = "Wie hoch ist das Rentenalter für Frauen?"
result = rag_pipeline.run(
            {
                "retriever": {"query": question},
                "prompt_builder": {"question": question},
                "answer_builder": {"query": question},
            }
        )
print(result['answer_builder']['answers'][0].data)
