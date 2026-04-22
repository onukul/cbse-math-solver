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
# This keeps your chat active for follow-up questions
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- GLOBAL MATH TOOLBAR ---
# This stays at the top of the app at all times
st.markdown("### ⌨️ Universal Math Toolbar")
def global_toolbar():
    math_keys = ["^2", "^3", "sqrt(", "pi", "∫", "d/dx", "det(", "limit(", "log(", "sin(", "cos(", "tan(", "∈", "≤", "≥", "≠"]
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

# --- CHAT INTERFACE LOGIC ---
st.header(f"📍 {chapter}")

# Display existing chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Image Uploader (only for Chat chapter)
uploaded_file = None
if chapter == "AI Chat: Proofs & Image Solver":
    uploaded_file = st.file_uploader("➕ Upload Image for solving", type=["jpg", "png", "jpeg"])

# Chat Input Box (stays active for follow-ups)
if prompt := st.chat_input("Ask a question or explain your doubt..."):
    # Add user message to state
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("AI is analyzing..."):
            try:
                # Combine context if there's an image
                if uploaded_file and len(st.session_state.messages) == 1:
                    img = Image.open(uploaded_file)
                    response = model.generate_content(["Solve this CBSE 12 problem:", img, prompt])
                else:
                    # Regular text conversation
                    # We pass the full history for continuity
                    chat = model.start_chat(history=[])
                    response = chat.send_message(f"As a CBSE Math Expert, help with this: {prompt}")
                
                full_response = response.text
                st.markdown(full_response)
                # Save assistant message to state
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"Error: {e}")

# --- SPECIFIC TOOLS (Below Chat) ---
if chapter == "Matrices & Determinants":
    with st.expander("Use Calculator Tool"):
        m_input = st.text_area("Matrix (1 2; 3 4)", "1 2; 3 4")
        if st.button("Calculate"):
            mat = Matrix([list(map(float, row.split())) for row in m_input.split(';')])
            st.latex(rf"|A| = {mat.det()}")

elif chapter == "Calculus (Integrals & Diff)":
    with st.expander("Use Calculus Engine"):
        func = st.text_input("Enter Function", "x**2")
        if st.button("Integrate"):
            res = integrate(sympify(func), symbols('x'))
            st.latex(latex(res))

# Button to clear conversation
if st.sidebar.button("Clear Conversation"):
    st.session_state.messages = []
    st.rerun()
