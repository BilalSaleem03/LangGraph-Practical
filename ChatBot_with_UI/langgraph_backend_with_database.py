from langgraph.graph import StateGraph, START, END
from typing import TypedDict , Annotated
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, HumanMessage
import os
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
import sqlite3


load_dotenv(override=True)

llm_model = ChatOpenAI(
    model="gpt-4o", 
    api_key=os.getenv("github_OPENAI_KEY"), 
    base_url="https://models.inference.ai.azure.com" 
)


class ChatbotState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def chat_node(state: ChatbotState) -> ChatbotState:
    #take user query from state
    messages = state['messages']
    #send to llm
    response = llm_model.invoke(messages)
    #store repsonse in state
    return {"messages": [response]}

conn = sqlite3.connect(database='chatbot.db' ,check_same_thread=False)

checkpointer = SqliteSaver(conn=conn)   

graph = StateGraph(ChatbotState)

graph.add_node('chat_node' , chat_node)
graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)

chatbot = graph.compile(checkpointer=checkpointer)

def retreave_all_threads():
    all_threads = set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])

    return list(all_threads)