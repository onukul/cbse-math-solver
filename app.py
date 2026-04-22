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
    st.error("API Key not found in Secrets. Please add GEMINI_API_KEY to your Streamlit dashboard.")
    st.stop()

genai.configure(api_key=GEMINI_API_KEY)
# Using Gemini 3 Flash for speed and higher free-tier limits
model = genai.GenerativeModel('gemini-3-flash-preview')

# --- NOTEBOOK THEME & PDF PRINT LOGIC (HTML/CSS/JS) ---
st.markdown("""
    <script>
    function printPage() {
        window.print();
    }
    </script>
    <style>
    /* Main Background: Paper Texture */
    .stApp {
        background-color: #fdfdfd;
        background-image: radial-gradient(#e5e5f7 0.5px, transparent 0.5px);
        background-size: 10px 10px;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #2c3e50 !important;
        border-right: 5px solid #c0392b; /* Notebook spine look */
    }
    section[data-testid="stSidebar"] .stMarkdown, section[data-testid="stSidebar"] label {
        color: white !important;
    }

    /* Custom Header Box */
    .header-box {
        background-color: #ffffff;
        border-bottom: 3px solid #3498db;
        padding: 20px;
        border-radius: 0px 0px 15px 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 25px;
    }

    /* Button Styling (Calculator Look) */
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        border: 1px solid #bdc3c7;
        background-color: #ffffff;
        color: #2c3e50;
        font-weight: bold;
        box-shadow: 2px 2px 0px #bdc3c7;
    }
    .stButton>button:hover {
        background-color: #3498db;
        color: white;
        border: 1px solid #3498db;
    }

    /* Exam Tip Styling */
    .exam-tip {
        border-left: 10px solid #c0392b;
        background-color: #fff5f5;
        padding: 15px;
        margin: 10px 0px;
        font-family: 'Courier New', Courier, monospace;
        border-radius: 5px;
    }

    /* PDF PRINT STYLING */
    @media print {
        section[data-testid="stSidebar"], .stButton, .header-box, .toolbar-container, button {
            display: none !important;
        }
        .stApp {
            background: white !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE (Chat Memory) ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_session" not in st.session_state:
    # This keeps the AI context alive for follow-up questions
    st.session_state.chat_session = model.start_chat(history=[])

# --- GLOBAL MATH TOOLBAR ---
st.markdown('<div class="header-box"><h1>📚 CBSE Math Master</h1></div>', unsafe_allow_html=True)
st.markdown('<div class="toolbar-container"><h3>⌨️ Universal Math Toolbar</h3>', unsafe_allow_html=True)

def global_toolbar():
    # Includes subscript (_) and superscript (^) helpers
    math_keys = ["^2", "^3", "sqrt(", "pi", "∫", "d/dx", "det(", "limit(", "_", "^{}", "∈", "≤", "≥", "≠", "sin(", "cos("]
    cols = st.columns(8)
    for i, symbol in enumerate(math_keys):
        with cols[i % 8]:
            if st.button(symbol, key=f"global_{symbol}_{i}"):
                st.code(symbol)

global_toolbar()
st.write("---")

# --- SIDEBAR ---
st.sidebar.title("📖 Chapter Index")
chapter = st.sidebar.selectbox("Go to:", [
    "AI Chat: Proofs & Image Solver",
    "Relations & Functions",
    "Matrices & Determinants",
    "Calculus (Integrals & Diff)",
    "Vector & 3D Geometry"
])

# Sidebar Controls
st.sidebar.write("---")
if st.sidebar.button("🗑️ Clear Conversation"):
    st.session_state.messages = []
    st.session_state.chat_session = model.start_chat(history=[])
    st.rerun()

if st.sidebar.button("💾 Save Solution as PDF"):
    st.markdown('<script>window.print();</script>', unsafe_allow_html=True)
    st.sidebar.info("Select 'Save as PDF' from your phone's print menu.")

# --- CHAT INTERFACE ---
st.subheader(f"📍 {chapter}")

# Display persistent message history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Image Uploader (only for Chat chapter)
uploaded_file = st.sidebar.file_uploader("➕ Upload Question Image", type=["jpg", "png", "jpeg"])

# Active Chat Input
if prompt := st.chat_input("Ask a math question or follow-up doubt..."):
    # Store and display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing context and writing response..."):
            try:
                # Handle images for the first turn or text for follow-ups
                if uploaded_file and len(st.session_state.messages) <= 1:
                    img = Image.open(uploaded_file)
                    response = model.generate_content(["Solve this CBSE 12 problem step-by-step:", img, prompt])
                    # Sync initial image context to history manually
                    st.session_state.chat_session.history.append({"role": "user", "parts": [prompt]})
                    st.session_state.chat_session.history.append({"role": "model", "parts": [response.text]})
                else:
                    # Continuous conversation using the stored chat session
                    response = st.session_state.chat_session.send_message(prompt)
                
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            
            except Exception as e:
                st.error(f"API Error: {e}. Try clearing conversation if it persists.")

# --- CHAPTER TOOLS ---
if chapter == "Matrices & Determinants":
    with st.expander("🧮 Matrix Calculator Tool"):
        m_input = st.text_area("Matrix (e.g., 1 2; 3 4)", "1 0; 0 1")
        if st.button("Solve Matrix"):
            mat = Matrix([list(map(float, row.split())) for row in m_input.split(';')])
            st.latex(rf"|A| = {mat.det()}")
