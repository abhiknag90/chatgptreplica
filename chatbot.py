import streamlit as st
from streamlit_chat import message
# from langchain.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
# from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import SystemMessage

system_message = """You are MasterBot. You are an airline/aviation maintenance engineer expert. You answer in a formal and very informative way.
You don't answer any questions not related to aircraft maintenance. Please respond with 'I cannot answer the question' for non-aircraft maintenance questions.
 """

import os

# os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# Initialize session state variables
if 'buffer_memory' not in st.session_state:
    st.session_state.buffer_memory = ConversationBufferMemory(k=3, return_messages=True)

if "messages" not in st.session_state.keys(): # Initialize the chat message history
    st.session_state.messages = [
        {"role": "assistant", "content": "How can I help you today?"}
    ]

# Initialize ChatOpenAI and ConversationChain
# llm = ChatOpenAI(model_name="gpt-4o-mini")
# llm = ChatGoogleGenerativeAI(model = "gemini-pro")
llm = ChatOpenAI(model = "meta-llama/Llama-3.2-90B-Vision-Instruct-Turbo",
                      openai_api_key = st.secrets["OPENAI_API_KEY"] , ## use your key
                      openai_api_base = "https://api.together.xyz/v1"

)

conversation = ConversationChain(memory=st.session_state.buffer_memory, llm=llm)

memory = ConversationBufferMemory(k = 3)

conversation = ConversationChain(
    llm=llm,
    memory = memory
)

# Create user interface
st.title("🗣️ Conversational Chatbot")
st.subheader("㈻ Your personal chatbot")


if prompt := st.chat_input("Your question"): # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages: # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = conversation.predict(input = prompt)
            st.write(response)
            message = {"role": "assistant", "content": response}
            st.session_state.messages.append(message) # Add response to message history
