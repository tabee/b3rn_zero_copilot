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

def _get_hugging_face_embeddings():
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
def _ignite_vectorstore(database_handler, embeddings, path_to_vetorestore, selected_languages=None):
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
    _ignite_vectorstore(database_handler=DatabaseHandler(DB_PATH__BSV_ADMIN_CH),
         embeddings=_get_hugging_face_embeddings(),
         path_to_vetorestore=DB_PATH__BSV_ADMIN_CH_VECTORSTORE_LOCAL,
         selected_languages=['de'])
def init_bsv_admin_ch_vectorstore_openai():
    '''Init vectorstore (bsv-faq) with openai embeddings.'''
    _ignite_vectorstore(database_handler=DatabaseHandler(DB_PATH__BSV_ADMIN_CH),
         embeddings=OpenAIEmbeddings(),
         path_to_vetorestore=DB_PATH__BSV_ADMIN_CH_VECTORSTORE_OPENAI,
         selected_languages=["de", "fr"])


def _get_suggestions_questions(input_text, languages=None, categories=None, embeddings=None, k=5, path_to_vetorestore=None, filter_typ='question'):
    '''Get suggestions based on input text. '''
    faiss_db = FAISS.load_local(path_to_vetorestore, embeddings)
    categories = None
    if categories is None:
        results_with_scores_filtered = faiss_db.similarity_search(
            input_text,
            k=k,
            filter={'type': filter_typ},
            fetch_k=10)
        list_from_vectorstor = [result.page_content for result in results_with_scores_filtered]
        print(f"list_from_vectorstor: {list_from_vectorstor}")
        return list_from_vectorstor
    else:
        # @todo: implement category filter
        return None
def get_suggestions_questions_openai(input_text, languages=None, categories=None, embeddings=None, k=5):
    '''Get suggestions based on input text. '''
    return _get_suggestions_questions(input_text, languages, categories, OpenAIEmbeddings(), k, DB_PATH__BSV_ADMIN_CH_VECTORSTORE_OPENAI)
def get_suggestions_answers_questions_openai(input_text, languages=None, categories=None, embeddings=None, k=5, filter_typ='question-answer'):
    '''Get suggestions based on input text. '''
    return _get_suggestions_questions(input_text, languages, categories, OpenAIEmbeddings(), k, DB_PATH__BSV_ADMIN_CH_VECTORSTORE_OPENAI, filter_typ=filter_typ)
def get_suggestions_questions_local(input_text, languages=None, categories=None, embeddings=None, k=5):
    '''Get suggestions based on input text. '''
    return _get_suggestions_questions(input_text, languages, categories, _get_hugging_face_embeddings(), k, DB_PATH__BSV_ADMIN_CH_VECTORSTORE_LOCAL)


if __name__ == '__main__':
    # init vectorstores
    # init_bsv_admin_ch_vectorstore_local()
   # init_bsv_admin_ch_vectorstore_openai()

    user_input = """ AHV21 """
    print(f"\ninput: {user_input}\n")

    print("********** local **********")
    start_time = time.time()
    res = get_suggestions_questions_local(input_text=user_input)
    end_time = time.time()
    print(f"{len(res)}, {end_time-start_time} sec.")
    for r in res:
        print(r)

    print("\n********** openai **********")
    start_time = time.time()
    res = get_suggestions_questions_openai(input_text=user_input)
    end_time = time.time()
    print(f"{len(res)}, {end_time-start_time} sec.")
    for r in res:
        print(r)
