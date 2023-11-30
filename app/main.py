''' Main file to run the app. '''
import time
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from config import set_enviroment_variables
from langchain.cache import RedisCache
from langchain.globals import set_llm_cache
import redis

def main():
    '''Main function to run the app. '''

    set_enviroment_variables()


    # Set the cache to use Redis
    # redis_url = "redis+sentinel://:secret-pass@sentinel-host:26379/mymaster/0"
    redis_url = "redis://localhost:6379"
    redis_client = redis.Redis.from_url(redis_url)
    set_llm_cache(RedisCache(redis_client))


    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """Write out the following equation 
                using algebraic symbols then solve it. 
                Use the format\n\nEQUATION:...\nSOLUTION:...\n\n""",
            ),
            ("human", "{equation_statement}"),
        ]
    )
    model = ChatOpenAI(temperature=0)
    runnable = (
        {"equation_statement": RunnablePassthrough()} | prompt | model | StrOutputParser()
    )

    print(runnable.invoke("x raised to the third plus seven equals 13"))



# Rest Ihres Codes ...

if __name__ == "__main__":
    start_time = time.time()  # Startzeit erfassen

    main()

    end_time = time.time()  # Endzeit erfassen
    total_time = end_time - start_time  # Dauer berechnen
    print(f"Die Ausführung der LLM-Aufgabe dauerte {total_time} Sekunden.")
