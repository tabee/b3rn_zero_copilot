from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough

def agent_for(topic="Elefanten"):
    '''Agent, der eine Geschichte über ein Thema erzählt'''
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
    for chunk in agent_for(topic="Elefanten"):
        print(chunk, end="", flush=True)
