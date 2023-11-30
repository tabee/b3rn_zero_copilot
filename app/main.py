''' Main file to run the app. '''
import os
import time
import redis
from config import set_enviroment_variables
from langchain.cache import RedisCache
from langchain.chat_models import ChatOpenAI
from langchain.globals import set_llm_cache
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough


def main():
    '''Main function to run the app. '''

    set_enviroment_variables()

    # Redis Cache
    redis_client = redis.Redis.from_url(os.environ.get("REDIS_URL"))
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
