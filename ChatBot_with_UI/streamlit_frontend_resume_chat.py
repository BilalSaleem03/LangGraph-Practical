import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage
import uuid

#................... Utility Functions ...................#

def get_thread_id():
    return str(uuid.uuid4())

def reset_chat(thread_name):
    
    new_thread_id = get_thread_id()
    add_thread_ids(new_thread_id,thread_name)
    st.session_state['message_history'] = []
    st.session_state['thread_id'] = new_thread_id
    st.session_state['thread_name'] = thread_name


def add_thread_ids(thread_id,thread_name):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)
        st.session_state['chat_threads_names'].append(thread_name)

def load_particular_conversation(thread_id):
    return chatbot.get_state(config={'configurable': {'thread_id' : thread_id}}).values['messages']

#................... Session Setup ...................#
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = get_thread_id()

if 'chat_threads_names' not in st.session_state:
    st.session_state['chat_threads_names'] =[]

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] =[]


add_thread_ids(st.session_state['thread_id'] , "First Chat")

#................... Sidebar UI ...................#
st.sidebar.title("LangGraph Chatbot")

thread_name = st.sidebar.text_input("Chat name" , "New Chat")
if st.sidebar.button("New Chat"):
    reset_chat(thread_name)

st.sidebar.header("My Chats")

for thread_id , thread_name in zip(st.session_state['chat_threads'][::-1],st.session_state['chat_threads_names'][::-1]):
    if st.sidebar.button(thread_name,key=thread_id):
        st.session_state['thread_id'] = thread_id
        messages = load_particular_conversation(thread_id)

        temp_messages = []
        for msg in messages:
            if isinstance(msg , HumanMessage):
                role='user'
            else:
                role='assistant'
            temp_messages.append({'role':role , 'content':msg.content})
        
        st.session_state['message_history'] = temp_messages

#................... Display Message History ...................#
for message in st.session_state['message_history']:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.write(message["content"])
    else:
        with st.chat_message("assistant"):
            st.write(message["content"])

user_input = st.chat_input("Type your message here...")

#................... Handle User Input and Chatbot Response ...................#
if user_input:

    st.session_state.message_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    
    CONFIG = {"configurable": {"thread_id": st.session_state['thread_id']}}
    #here we implement streaming response from the chatbot
    with st.chat_message("assistant"):
        ai_message = st.write_stream(
            message_chunk.content for message_chunk , metadata in chatbot.stream(
                {"messages": [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode="messages"
            )
        )
    st.session_state.message_history.append({"role": "assistant", "content": ai_message})
            