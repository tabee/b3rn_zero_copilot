''' This is the main file for the chatbot agent. It is called by the main.py file in the same directory. '''
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough

def run_agent(user_input="Tell me something about the next open ai model!"):
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are a helpfull assistant 
                for this prompt: {user_input}:\n\n 
                Your answer is as short as possible.
                And long answer is not needed.""",
            ),
            ("human", "{user_input}"),
            ]
        )
    model = ChatOpenAI(temperature=0.05)
    runnable = (
        {"user_input": RunnablePassthrough()} | prompt | model | StrOutputParser()
    )

    result = runnable.invoke(user_input)
    print(result)
    return result

if __name__ == "__main__":
    run_agent()
