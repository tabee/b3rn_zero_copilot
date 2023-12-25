from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import asyncio

model = ChatOpenAI(verbose=False)
template = """Answer the question based only on the following context:
{context}

Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)

vectorstore = FAISS.from_texts(
    ["harrison worked at kensho"], embedding=OpenAIEmbeddings()
)
retriever = vectorstore.as_retriever()

retrieval_chain = (
    {
        "context": retriever.with_config(run_name="Docs"),
        "question": RunnablePassthrough(),
    }
    | prompt
    | model
    | StrOutputParser()
)

def agent_for(user_input):
    for s in retrieval_chain.stream(user_input):
        yield s


if __name__ == "__main__":
    for chunk in agent_for(user_input="where did harrison work?"):
        print(chunk, end="", flush=True)