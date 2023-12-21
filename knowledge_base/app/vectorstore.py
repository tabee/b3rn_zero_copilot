import os
import time
import asyncio
from database import DatabaseHandler
from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores.faiss import FAISS
from langchain.schema import Document
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings



DB_PATH = os.getenv('DATA_PATH', default=os.path.join(os.path.dirname(__file__), 'data'))
DB_PATH__BSV_ADMIN_CH = DB_PATH + '/bsv_faq.db'
DB_PATH__BSV_ADMIN_CH_VECTORESTORE = DB_PATH + '/bsv_faq_demo_vectorestore'
DB_PATH__BSV_ADMIN_CH_VECTORESTORE_LOCAL_EMBEDDINGS = DB_PATH + '/bsv_faq_demo_vectorestore_local_embeddings'

def get_embedding_model():
    model_name = "sentence-transformers/all-mpnet-base-v2"
    model_kwargs = {'device': 'cpu'}
    encode_kwargs = {'normalize_embeddings': False}
    return HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )

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

def init_local(languages=["de"]):
    db_sqlite = DatabaseHandler(DB_PATH__BSV_ADMIN_CH)

    list_of_documents = []
    categories = db_sqlite.get_unique_categories(selected_languages=languages)

    for category in categories:
        bsv_faq_by_category = db_sqlite.get_questions_answers_by_category(category)
        
        for q,a in bsv_faq_by_category[0:2]:
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
    
    embeddings = get_embedding_model()
    faiss_db = FAISS.from_documents(list_of_documents, embeddings)
    faiss_db.save_local(DB_PATH__BSV_ADMIN_CH_VECTORESTORE_LOCAL_EMBEDDINGS)

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

def get_suggestions_questions_local(input_text, languages=None, categories=None, k=5):
    '''Get suggestions based on input text. '''
    embeddings = HuggingFaceEmbeddings()
    faiss_db = FAISS.load_local(DB_PATH__BSV_ADMIN_CH_VECTORESTORE_LOCAL_EMBEDDINGS, embeddings)

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

if __name__ == '__main__':

    user_input = "KJFG"  

    #init_local()
    start_time = time.time()
    res = get_suggestions_questions_local(user_input, k=5)
    end_time = time.time()
    print(f"{len(res)}, {end_time-start_time}ms, local:")
    for r in res:
        print(r)
    
    print("***************************")

    #init()
    start_time = time.time()
    res = get_suggestions_questions(user_input, k=5)
    end_time = time.time()
    print(f"{len(res)}, {end_time-start_time}ms, openai:")
    for r in res:
        print(r)
