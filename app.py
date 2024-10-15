from dotenv import load_dotenv
import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage

# Load environment variables
load_dotenv()

st.title("💬 Maverick minds")
st.caption("🚀 your app to generate Arabic Poem")

# Initialize chat history if not already in session state
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

# Display the conversation
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Function to call Google Generative AI (Gemini Pro)
def get_google_ai_response(messages):
    llm = ChatGoogleGenerativeAI(
        model='gemini-pro', 
        google_api_key=os.getenv("GOOGLE_API_KEY"), 
        temperature=0.7,
        max_output_tokens=100, 
        convert_system_message_to_human=True
    )

    # Convert the chat history into a list of Human and AI messages
    chat_history = [HumanMessage(content=msg["content"]) if msg["role"] == "user" else AIMessage(content=msg["content"]) for msg in messages]

    # Send the request and get the response
    response = llm.invoke(chat_history)

    return response.content

# Handle user input
if prompt := st.chat_input():
    # if not google_api_key:
    #     st.info("Please add your Google API key to continue.")
    #     st.stop()

    # Add user message to session state and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Get the AI response from Google Gemini Pro model
    response = get_google_ai_response(st.session_state["messages"])

    # Append AI response to session state and display it
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)
