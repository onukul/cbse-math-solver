import streamlit as st
from sympy import symbols, sympify, diff, integrate, Matrix, latex, Limit, S
import google.generativeai as genai
from PIL import Image

# --- CONFIGURATION ---
st.set_page_config(page_title="CBSE Class 12 Math Master", layout="wide")

# Fetch Key from Secrets
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
except KeyError:
    st.error("API Key not found in Streamlit Secrets.")
    st.stop()

genai.configure(api_key=GEMINI_API_KEY)
# Using Flash for speed and higher free-tier quota
model = genai.GenerativeModel('gemini-3-flash-preview')

# --- MATH KEYBOARD HELPER ---
def math_keyboard(layout_type):
    st.write("---")
    st.subheader("⌨️ Math Toolbar")
    
    # Define toolbars for different chapters
    keyboards = {
        "General": ["^2", "^3", "sqrt()", "pi", "( )", "e"],
        "Calculus": ["d/dx", "∫", "limit(", "∞", "exp(", "log("],
        "Matrices": ["[ ]", "det()", "inv()", "T", "I"],
        "Relations": ["∈", "⊂", "∀", "∃", "≤", "≥", "≠"]
    }
    
    selected_keys = keyboards.get(layout_type, keyboards["General"])
    
    # Create columns for buttons
    cols = st.columns(len(selected_keys))
    for i, symbol in enumerate(selected_keys):
        if cols[i].button(symbol):
            st.info(f"Copy-paste this: `{symbol}`") 
            # Note: Streamlit doesn't allow direct text injection into an active input,
            # so we show it as a helper for the user to copy/paste.

# --- SIDEBAR ---
st.sidebar.title("📚 CBSE Syllabus")
chapter = st.sidebar.selectbox("Select Chapter", [
    "AI Chat: Proofs & Image Solver",
    "Relations & Functions",
    "Matrices & Determinants",
    "Calculus (Integrals & Diff)",
    "Vector & 3D Geometry"
])

# --- CHAPTER LOGIC ---

if chapter == "AI Chat: Proofs & Image Solver":
    st.header("💬 AI Tutor: Proofs & Problem Solving")
    math_keyboard("General") # Show general math symbols
    
    uploaded_file = st.file_uploader("➕ Upload Image", type=["jpg", "png", "jpeg"])
    prompt = st.text_area("Type your question here (or use the toolbar above):")
    
    if st.button("Solve"):
        with st.spinner("Analyzing..."):
            if uploaded_file:
                img = Image.open(uploaded_file)
                response = model.generate_content(["Solve this CBSE 12 problem step-by-step:", img, prompt])
            else:
                response = model.generate_content(f"Act as a CBSE Math Expert. Solve/Prove: {prompt}")
            st.markdown(response.text)

elif chapter == "Matrices & Determinants":
    st.header("Matrices & Determinants")
    math_keyboard("Matrices")
    m_input = st.text_area("Matrix (rows separated by ';', elements by space)", "1 2; 3 4")
    # ... (rest of your matrix code)
