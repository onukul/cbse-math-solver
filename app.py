import streamlit as st
from sympy import symbols, sympify, diff, integrate, Matrix, latex, Limit, S
import google.generativeai as genai
from PIL import Image

# --- CONFIGURATION ---
st.set_page_config(page_title="CBSE Class 12 Math Master", layout="wide")

# Setup Gemini
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
except KeyError:
    st.error("API Key not found in Secrets.")
    st.stop()

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-3-flash-preview')

# --- SESSION STATE INITIALIZATION ---
# 'messages' stores the UI display, 'chat_session' stores the AI's memory
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# --- GLOBAL MATH TOOLBAR ---
st.markdown("### ⌨️ Universal Math Toolbar")
def global_toolbar():
    # Added subscript/superscript helpers here as requested
    math_keys = ["^2", "^3", "sqrt(", "pi", "∫", "d/dx", "det(", "limit(", "_", "^{}", "∈", "≤", "≥", "≠"]
    cols = st.columns(8)
    for i, symbol in enumerate(math_keys):
        with cols[i % 8]:
            if st.button(symbol, key=f"global_{symbol}_{i}"):
                st.code(symbol)
st.write("---")
global_toolbar()

# --- SIDEBAR ---
st.sidebar.title("📚 CBSE Syllabus")
chapter = st.sidebar.selectbox("Select Chapter", [
    "AI Chat: Proofs & Image Solver",
    "Relations & Functions",
    "Matrices & Determinants",
    "Calculus (Integrals & Diff)",
    "Vector & 3D Geometry"
])

# Button to clear conversation
if st.sidebar.button("Clear Conversation"):
    st.session_state.messages = []
    st.session_state.chat_session = model.start_chat(history=[])
    st.rerun()

# --- CHAT INTERFACE ---
st.header(f"📍 {chapter}")

# Display existing chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Image Uploader (only for Chat chapter)
uploaded_file = st.sidebar.file_uploader("➕ Upload Image", type=["jpg", "png", "jpeg"])

# Chat Input Box
if prompt := st.chat_input("Ask a question or explain your doubt..."):
    # 1. Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Generate AI response with MEMORY
    with st.chat_message("assistant"):
        with st.spinner("AI is thinking..."):
            try:
                # If first message has an image, use generate_content
                if uploaded_file and len(st.session_state.messages) <= 1:
                    img = Image.open(uploaded_file)
                    response = model.generate_content(["Solve this CBSE 12 problem:", img, prompt])
                    # Sync the image response into chat history
                    st.session_state.chat_session.history.append({"role": "user", "parts": [prompt]})
                    st.session_state.chat_session.history.append({"role": "model", "parts": [response.text]})
                else:
                    # Continuous conversation
                    response = st.session_state.chat_session.send_message(prompt)
                
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Context Error: {e}")
