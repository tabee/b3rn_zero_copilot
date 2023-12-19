import os
import asyncio
from database import DatabaseHandler
from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores.faiss import FAISS
from langchain.schema import Document

DB_PATH = os.getenv('DATA_PATH', default=os.path.join(os.path.dirname(__file__), 'data'))
DB_PATH__BSV_ADMIN_CH = DB_PATH + '/bsv_faq.db'
DB_PATH__BSV_ADMIN_CH_VECTORESTORE = DB_PATH + '/bsv_faq_demo_vectorestore'


def init():
    db = DatabaseHandler(DB_PATH__BSV_ADMIN_CH)

    bsv_faq_demo = db.get_questions_answers_by_category("alters-und-hinterlassenenversicherung-ahv")
    embeddings = OpenAIEmbeddings()

    list_of_documents = []
    for q,a in bsv_faq_demo:
        content = f"question: {q}\n answer: {a}\n\n"
        print(f"add: {content}...")
        list_of_documents.append(Document(page_content=content, metadata=dict(category="alters-und-hinterlassenenversicherung-ahv")))
    
    faiss_db = FAISS.from_documents(list_of_documents, embeddings)
    faiss_db.save_local(DB_PATH__BSV_ADMIN_CH_VECTORESTORE)



async def test(query):
    embeddings = OpenAIEmbeddings()
    faiss_db = FAISS.load_local(DB_PATH__BSV_ADMIN_CH_VECTORESTORE, embeddings)
    results_with_scores_filtered = await faiss_db.asimilarity_search_with_score(query, k=1, fetch_k=10)
    for doc, score in results_with_scores_filtered:
        print(f"Content: {doc.page_content}, Metadata: {doc.metadata}, Score: {score}")

if __name__ == '__main__':
    init()
    asyncio.run(test("Lohnabrechnungen"))
