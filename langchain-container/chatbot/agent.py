from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.schema.messages import AIMessage, HumanMessage
from langchain.agents import AgentExecutor
from langchain.tools.render import format_tool_to_openai_function
from langchain.cache import SQLiteCache
from langchain.globals import set_llm_cache
from agent_tools import tools
import os
def agent_for_here_weare(topic="Elefanten"):
    
    chat_history = []

    llm = ChatOpenAI(
        api_key=os.environ["OPENAI_API_KEY"],
        temperature=0,
        model="gpt-4-1106-preview",
        n=3)
    #set_llm_cache(SQLiteCache(database_path=LLM_CACHE_PATH))


    MEMORY_KEY = "chat_history"
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """Du bist ein KI-Experte für das schweizer Sozialversicherungssystem der 1. Säule.
                Ich bin ein Mitarbeiter einer Ausgleichskasse in der CH.
                Nutze deine Tools um Fragen zu beantworten. Erfinde keine Antworten.
                Deine bevorzugte Quellen ist das Tool sozialversicherungssystem_faq_retriever.
                Beantworte Fragen IMMER mit einer Qullenangabe:""",
            ),
            MessagesPlaceholder(variable_name=MEMORY_KEY),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    llm_with_tools = llm.bind(functions=[format_tool_to_openai_function(t) for t in tools])

    agent = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_to_openai_function_messages(
                x["intermediate_steps"]
                ),
            "chat_history": lambda x: x["chat_history"],
        }
        | prompt
        | llm_with_tools
        | OpenAIFunctionsAgentOutputParser()
    )
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        return_intermediate_steps=False,
        verbose=False)

    for chunks in agent_executor.stream({"input": topic, "chat_history": chat_history}):
            yield chunks

def agent_for(topic="Elefanten"):
    '''Agent, der eine Geschichte über ein Thema erzählt'''

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """bisherige Konversation {topic}\n\n 
                Versuche die letzte Anfrage des humans zu beantworten.
                Du bist schweizer sozialversucherungsexperte:\n\n""",
            ),
            ("human", "{topic}"),
            ]
        )
    
    model = ChatOpenAI(temperature=0, model="gpt-3.5-turbo",n=1)
    runnable = (
        {"topic": RunnablePassthrough()} | prompt | model | StrOutputParser()
    )

    for chunks in runnable.stream(topic):
        yield chunks

if __name__ == "__main__":
    for chunk in agent_for(topic="was ist EV"):
        print(chunk, end="", flush=True)