import streamlit as st  
from langchain_core.prompts import ChatPromptTemplate  
from langchain_core.output_parsers import StrOutputParser  
from langchain_community.llms import Ollama  
import os   

# --- Streamlit App Configuration ---  
st.set_page_config(page_title="KAIRO-AI", layout="wide")  
st.title("🤖 KAIRO-AI: Your Personal Assistant")  

# --- Sidebar Instructions and Personality Selection ---  
with st.sidebar:  
    st.header("Instructions")  
    st.write("1️⃣ Type your question in the input box.")  
    st.write("2️⃣ Click 'Send' to get a response.")  
    st.write("3️⃣ Adjust KAIRO's personality!")  

    personality = st.selectbox(  
        "Choose KAIRO's Personality:",  
        ["Professional", "Friendly", "Funny", "Technical"],  
    )  

# --- Personality-Based System Prompts ---  
personality_prompts = {  
    "Professional": "You are KAIRO, a professional, polite, and formal assistant.",  
    "Friendly": "You are KAIRO, a friendly, casual, and warm assistant.",  
    "Funny": "You are KAIRO, a humorous assistant, always adding light jokes.",  
    "Technical": "You are KAIRO, a highly technical, precise, and detailed assistant.",  
}  

# --- Initialize LangChain Components ---  
prompt = ChatPromptTemplate.from_messages([  
    ("system", personality_prompts[personality]),  
    ("user", "{query}")  
])  
llm = Ollama(model="llama2")  
output_parser = StrOutputParser()  
chain = prompt | llm | output_parser  

# --- Session State for Chat History ---  
if "chat_history" not in st.session_state:  
    st.session_state.chat_history = []  

# --- Input and Output ---  
input_txt = st.text_input("💬 What’s on your mind? Type it here!")  

if st.button("Send"):  
    if input_txt:  
        response = chain.invoke({"query": input_txt})  

        st.session_state.chat_history.append(("You", input_txt))  
        st.session_state.chat_history.append(("KAIRO", response))  
    else:  
        st.warning("⚠️ Please enter a question before clicking 'Send'.")  

# --- Display Chat History ---  
for speaker, message in st.session_state.chat_history:  
    role_indicator = "🧑" if speaker == "You" else "🤖"  
    st.markdown(f"{role_indicator} **{speaker}:** {message}")  

# --- Footer ---  
st.markdown("---")  
st.text("© 2025 KAIRO-AI. All rights reserved.")  
st.text("🚀 Powered by KAIRO-AI Team | Made with ❤️")  