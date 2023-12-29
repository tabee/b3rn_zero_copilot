''' https://haystack.deepset.ai/tutorials/24_building_chat_app'''
import os
from getpass import getpass
from haystack.nodes import PromptNode
from haystack.agents.memory import ConversationSummaryMemory
from haystack.agents.conversational import ConversationalAgent

#######################
# we need to set the HF_API_KEY environment variable to access the model !!!!!!!!!!!!!!!!
HF_API_KEY="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"
os.environ["HF_API_KEY"] = HF_API_KEY   # needed for the Hub model to be accessible
#######################
model_api_key = os.getenv("HF_API_KEY", None) or getpass("Enter HF API key:")

prompt_node = PromptNode(
    model_name_or_path="HuggingFaceH4/zephyr-7b-beta",
    api_key=model_api_key,
    debug=True,
    max_length=256,
    stop_words=["Human"],
)
summary_memory = ConversationSummaryMemory(prompt_node)
conversational_agent = ConversationalAgent(
   prompt_node=prompt_node,
   memory=summary_memory,
   #tools=[search_tool]
)
conversational_agent.run("Tell me three most interesting things about Istanbul, Turkey")
conversational_agent.run("Can you elaborate on the second item?")
