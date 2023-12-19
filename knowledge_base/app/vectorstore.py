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
    db_sqlite = DatabaseHandler(DB_PATH__BSV_ADMIN_CH)

    embeddings = OpenAIEmbeddings()
    list_of_documents = []
    categories = db_sqlite.get_unique_categories()

    for category in categories:
        bsv_faq_by_category = db_sqlite.get_questions_answers_by_category(category)
        
        for q,a in bsv_faq_by_category:
            content = f"question: {q}\n answer: {a}\n\n"
            list_of_documents.append(
                Document( page_content=content, metadata=dict(category=category, type="question-answer") )
                )
            list_of_documents.append(
                Document( page_content=q, metadata=dict(category=category, type="question") )
                )
            list_of_documents.append(
                Document( page_content=a, metadata=dict(category=category, type="answer") )
                )
        
    faiss_db = FAISS.from_documents(list_of_documents, embeddings)
    faiss_db.save_local(DB_PATH__BSV_ADMIN_CH_VECTORESTORE)

def get_suggestions_questions(input_text, languages=None, categories=None, k=5):
    '''Get suggestions based on input text. '''
    embeddings = OpenAIEmbeddings()
    faiss_db = FAISS.load_local(DB_PATH__BSV_ADMIN_CH_VECTORESTORE, embeddings)

    categories = None
    if categories is None:
        results_with_scores_filtered = faiss_db.similarity_search(
            input_text, 
            k=k, 
            filter={'type': 'question'},
            fetch_k=10)
        list_of_questions = [result.page_content for result in results_with_scores_filtered]
        return list_of_questions
    else:
        # @todo: implement category filter
        return None
    
async def aget_suggestions_questions(input_text, languages=None, categories=None, k=5):
    '''Get suggestions based on input text. '''
    embeddings = OpenAIEmbeddings()
    faiss_db = FAISS.load_local(DB_PATH__BSV_ADMIN_CH_VECTORESTORE, embeddings)

    categories = None
    if categories is None:
        results_with_scores_filtered = await faiss_db.asimilarity_search(
            input_text, 
            k=k, 
            filter={'type': 'question'},
            fetch_k=10)
        list_of_questions = [result.page_content for result in results_with_scores_filtered]
        return list_of_questions
    else:
        # @todo: implement category filter
        return None
    
if __name__ == '__main__':
    #init()
    #res = asyncio.run(aget_suggestions_questions("KJFG", k=5))
    res = get_suggestions_questions("KJFG", k=5)
    print(len(res))
    for r in res:
        print(r)
