import streamlit as st
from langgraph_backend_with_database import chatbot,retreave_all_threads
from langchain_core.messages import HumanMessage
import uuid

#................... Utility Functions ...................#

def get_thread_id():
    return str(uuid.uuid4())

def reset_chat():
    new_thread_id = get_thread_id()
    add_thread_ids(new_thread_id)
    st.session_state['message_history'] = []
    st.session_state['thread_id'] = new_thread_id

def add_thread_ids(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def load_particular_conversation(thread_id):
    return chatbot.get_state(config={'configurable': {'thread_id' : thread_id}}).values['messages']

#................... Session Setup ...................#
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = get_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] =retreave_all_threads()

add_thread_ids(st.session_state['thread_id'])

#................... Sidebar UI ...................#
st.sidebar.title("LangGraph Chatbot")

if st.sidebar.button("New Chat"):
    reset_chat()

st.sidebar.header("My Chats")

for thread_id in st.session_state['chat_threads'][::-1]:
    if st.sidebar.button(thread_id):
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

    
    CONFIG = {
        "configurable": {"thread_id": st.session_state['thread_id']},
        "metadata":{
            "thread_id": st.session_state['thread_id']
        },
        "run_name": "chat_turn",
    }
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
            