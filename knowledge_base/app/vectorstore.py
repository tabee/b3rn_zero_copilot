import os
import time
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.faiss import FAISS
from langchain.schema import Document
from langchain.embeddings import HuggingFaceEmbeddings
from database import DatabaseHandler

# path to data folder on server
DB_PATH = os.getenv('DATA_PATH', default=os.path.join(os.path.dirname(__file__), 'data'))
# sqlite database
DB_PATH__BSV_ADMIN_CH = DB_PATH + '/bsv_faq.db'
# FAISS vectorstores
DB_PATH__BSV_ADMIN_CH_VECTORSTORE_OPENAI = DB_PATH + '/bsv_faq_demo_vectorestore__openai'
DB_PATH__BSV_ADMIN_CH_VECTORSTORE_LOCAL = DB_PATH + '/bsv_faq_demo_vectorestore_all-mpnet-base-v2'

#@todo: class VectorStore:

def get_hugging_face_embeddings():
    '''Get HuggingFaceEmbeddings.'''
    model_name = "sentence-transformers/all-mpnet-base-v2"
    # model_name = "SentenceTransformer('sentence-transformers/multi-qa-MiniLM-L6-cos-v1')
    model_kwargs = {'device': 'cpu'}
    encode_kwargs = {'normalize_embeddings': False}
    return HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )

def ignite_vectorstore(database_handler, embeddings, path_to_vetorestore, selected_languages=None):
    print(f"ignite vectorstore {path_to_vetorestore}")
    list_of_documents = []
    categories = database_handler.get_unique_categories(selected_languages)
    for category in categories:
        print(f"process category: {category}")
        category_dataset = database_handler.get_questions_answers_by_category(category)
        for q,a in category_dataset:
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
    faiss_db.save_local(path_to_vetorestore)

def init_bsv_admin_ch_vectorstore_local():
    '''Init vectorstore (bsv-faq) with local embeddings.'''
    ignite_vectorstore(database_handler=DatabaseHandler(DB_PATH__BSV_ADMIN_CH),
         embeddings=get_hugging_face_embeddings(),
         path_to_vetorestore=DB_PATH__BSV_ADMIN_CH_VECTORSTORE_LOCAL,
         selected_languages=['de'])

def init_bsv_admin_ch_vectorstore_openai():
    '''Init vectorstore (bsv-faq) with openai embeddings.'''
    ignite_vectorstore(database_handler=DatabaseHandler(DB_PATH__BSV_ADMIN_CH),
         embeddings=OpenAIEmbeddings(),
         path_to_vetorestore=DB_PATH__BSV_ADMIN_CH_VECTORSTORE_OPENAI,
         selected_languages=['de'])

def get_suggestions_questions(input_text, embeddings, languages=None, categories=None, k=5, path_to_vetorestore=DB_PATH__BSV_ADMIN_CH_VECTORSTORE_OPENAI):
    '''Get suggestions based on input text. '''
    faiss_db = FAISS.load_local(path_to_vetorestore, embeddings)
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
    init_bsv_admin_ch_vectorstore_local()
    init_bsv_admin_ch_vectorstore_openai()

    user_input = """ Mutterschaftsentschädigung """
    print(f"\ninput: {user_input}\n")


    print("********** local **********")
    start_time = time.time()
    res = get_suggestions_questions(input_text=user_input, k=5, path_to_vetorestore=DB_PATH__BSV_ADMIN_CH_VECTORSTORE_LOCAL, embeddings=get_hugging_face_embeddings(), languages=['de'])
    end_time = time.time()
    print(f"{len(res)}, {end_time-start_time}sec:")
    for r in res:
        print(r)

    print("********** openai **********")
    start_time = time.time()
    res = get_suggestions_questions(input_text=user_input, k=5, path_to_vetorestore=DB_PATH__BSV_ADMIN_CH_VECTORSTORE_OPENAI, embeddings=OpenAIEmbeddings(), languages=['de'])
    end_time = time.time()
    print(f"{len(res)}, {end_time-start_time}sec:")
    for r in res:
        print(r)
