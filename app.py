import streamlit as st
from panchakarma_chatbot import get_gemini_response

# --------------------------
# Streamlit Page Config
# --------------------------
st.set_page_config(page_title="Panchakarma Chatbot", page_icon="🧘", layout="wide")

st.title("🧘 Panchakarma Chatbot")
st.markdown("Ask any question about Panchakarma or Ayurvedic practices. Powered by **Google Gemini**.")

# --------------------------
# Sidebar for Therapy Type
# --------------------------
with st.sidebar:
    st.header("Settings")
    therapy_type_input = st.text_input("Therapy Type (optional):", placeholder="Virechana, Basti, etc.")
    if st.button("Set Therapy Type"):
        st.session_state.therapy_type = therapy_type_input

# --------------------------
# Initialize Chat History
# --------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --------------------------
# Chat Input
# --------------------------
if prompt := st.chat_input("Ask your question:"):
    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Gemini AI response
    with st.chat_message("assistant"):
        with st.spinner("Generating response..."):
            response = get_gemini_response(prompt, st.session_state.get("therapy_type"))
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

# --------------------------
# Clear Chat History Button
# --------------------------
if st.button("Clear Chat History"):
    st.session_state.messages = []

st.markdown("---")
st.caption("*Disclaimer: This chatbot provides general Ayurvedic guidance—consult a certified practitioner for personalized advice.*")
