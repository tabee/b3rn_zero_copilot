from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain.cache import RedisCache
from langchain.globals import set_llm_cache
import redis

REDIS_URL = "redis://langchain-redis:6379"

def agent_for(topic="Elefanten", redis_url=REDIS_URL):
    '''Agent, der eine Geschichte über ein Thema erzählt'''
    
    # Erstellen Sie eine Redis-Client-Instanz
    redis_client = redis.Redis.from_url(redis_url)
    set_llm_cache(RedisCache(redis_client))
    print(f"Redis-Client: {redis_client}")

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """Erzähl ein Witz, der ca. 300 zeichen lang ist 
                wie Chuck Norris über {topic} denken 
                könnte. Begründe ausführlich:\n\n""",
            ),
            ("human", "{topic}"),
            ]
        )
    model = ChatOpenAI(temperature=0.4, model="gpt-3.5-turbo-0301")
    runnable = (
        {"topic": RunnablePassthrough()} | prompt | model | StrOutputParser()
    )

    for chunks in runnable.stream(topic):
        yield chunks

if __name__ == "__main__":
    print("Finaly... ggg Go go:\n")
    for chunk in agent_for(topic="Elefanten"):
        print(chunk, end="", flush=True)
