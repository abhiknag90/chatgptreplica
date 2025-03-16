import streamlit as st
from streamlit_chat import message
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import SystemMessage
import os

# Define system message for the chatbot
system_message = """You are MasterBot. You are an airline/aviation maintenance engineer expert. You answer in a formal and very informative way.
You don't answer any questions not related to aircraft maintenance. Please respond with 'I cannot answer the question' for non-aircraft maintenance questions.
 """

# Initialize session state variables
if 'buffer_memory' not in st.session_state:
    st.session_state.buffer_memory = ConversationBufferMemory(k=3, return_messages=True)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "How can I help you today?"}
    ]

# Initialize the language model and conversation chain only once
if 'conversation' not in st.session_state:
    llm = ChatOpenAI(
        model="meta-llama/Llama-3.2-90B-Vision-Instruct-Turbo",
        openai_api_key=st.secrets["OPENAI_API_KEY"],
        openai_api_base="https://api.together.xyz/v1"
    )
    
    st.session_state.conversation = ConversationChain(
        llm=llm,
        memory=st.session_state.buffer_memory
    )
    
    # Add the system message to the conversation
    st.session_state.conversation.memory.chat_memory.add_message(SystemMessage(content=system_message))

# Create user interface
st.title("🗣️ Conversational Chatbot")
st.subheader("㈻ Your aviation maintenance expert")

# Get user input
if prompt := st.chat_input("Your question"):
    st.session_state.messages.append({"role": "user", "content": prompt})

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Generate response if the last message is from the user
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = st.session_state.conversation.predict(input=prompt)
                st.write(response)
                message = {"role": "assistant", "content": response}
                st.session_state.messages.append(message)
            except Exception as e:
                error_message = f"Sorry, I encountered an error: {str(e)}"
                st.write(error_message)
                st.session_state.messages.append({"role": "assistant", "content": error_message})
