import os
from haystack import Pipeline, Document
from haystack.document_stores import InMemoryDocumentStore
from haystack.components.retrievers import InMemoryBM25Retriever
from haystack.components.generators import GPTGenerator
from haystack.components.builders.answer_builder import AnswerBuilder
from haystack.components.builders.prompt_builder import PromptBuilder


prompt_template = """
Given these documents, answer the question.
Documents:
{% for doc in documents %}
    {{ doc.content }}
{% endfor %}
Question: {{question}}
Answer:
"""

document_store = InMemoryDocumentStore()
retriever = InMemoryBM25Retriever(document_store=document_store)
prompt_builder = PromptBuilder(template=prompt_template)
llm = GPTGenerator(api_key=os.environ.get("OPENAI_API_KEY"))
answer_builder = AnswerBuilder()

rag_pipeline = Pipeline()
rag_pipeline.add_component("retriever", retriever)
rag_pipeline.add_component("prompt_builder", prompt_builder)
rag_pipeline.add_component("llm", llm)
rag_pipeline.add_component("answer_builder", answer_builder)
rag_pipeline.connect("retriever", "prompt_builder.documents")
rag_pipeline.connect("prompt_builder", "llm")
rag_pipeline.connect("llm.replies", "answer_builder.replies")

document_store.write_documents([
    Document(content="My name is Jean and I live in Paris."), 
    Document(content="My name is Mark and I live in Berlin."), 
    Document(content="My name is Giorgio and I live in Rome.")
])

rag_pipeline.draw("rag_pipeline.png")

question = "Who lives in Paris?"
results = rag_pipeline.run(
    {
        "retriever": {"query": question},
        "prompt_builder": {"question": question},
        "answer_builder": {"query": question},
    }
)

for answer in results["answer_builder"]["answers"]:
    print(answer.data)