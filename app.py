import streamlit as st
from sympy import symbols, sympify, diff, integrate, Matrix, latex, Limit, S
import google.generativeai as genai
from PIL import Image

# --- CONFIGURATION ---
st.set_page_config(page_title="CBSE Class 12 Math Master", layout="wide")

# Setup Gemini using Streamlit Secrets
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
except KeyError:
    st.error("API Key not found. Please set 'GEMINI_API_KEY' in Streamlit Secrets.")
    st.stop()

genai.configure(api_key=GEMINI_API_KEY)

# Using Gemini 3 Flash for high speed and better free-tier limits
model = genai.GenerativeModel('gemini-3-flash-preview')

# --- MATH KEYBOARD FUNCTION ---
def math_keyboard(layout_type):
    st.markdown(f"#### ⌨️ {layout_type} Toolbar")
    
    # Comprehensive symbol sets for CBSE 12
    keyboards = {
        "General": ["^2", "^3", "sqrt(", "pi", "(", ")", "e", "+", "-", "*", "/", "="],
        "Calculus": ["d/dx", "∫", "limit(", "∞", "log(", "exp(", "sin(", "cos(", "tan("],
        "Matrices": ["det(", "inv(", "adj(", "T", "[", "]", ";", "0", "1", "I"],
        "Relations": ["∈", "⊂", "∀", "∃", "≤", "≥", "≠", "→", "R", "N", "Z"],
        "Vectors": ["î", "ĵ", "k̂", "·", "×", "| |", "θ", "λ", "μ"]
    }
    
    symbols_to_show = keyboards.get(layout_type, keyboards["General"])
    
    # Display buttons in a neat grid
    cols = st.columns(6) 
    for i, symbol in enumerate(symbols_to_show):
        with cols[i % 6]:
            if st.button(symbol, key=f"btn_{layout_type}_{symbol}_{i}"):
                st.code(symbol) # Provides an easy-to-copy snippet

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("📚 CBSE Syllabus")
chapter = st.sidebar.selectbox("Select Chapter", [
    "AI Chat: Proofs & Image Solver",
    "Relations & Functions",
    "Matrices & Determinants",
    "Calculus (Integrals & Diff)",
    "Vector & 3D Geometry"
])

x, y, z, t = symbols('x y z t')

# --- CHAPTER LOGIC ---

if chapter == "AI Chat: Proofs & Image Solver":
    st.header("💬 AI Tutor: Proofs & Problem Solving")
    math_keyboard("General")
    
    uploaded_file = st.file_uploader("➕ Upload Image", type=["jpg", "png", "jpeg"])
    prompt = st.text_area("Type your question here (or copy symbols from above):")
    
    if st.button("Solve", type="primary"):
        with st.spinner("AI is thinking..."):
            if uploaded_file:
                img = Image.open(uploaded_file)
                response = model.generate_content(["Solve this CBSE 12 problem step-by-step:", img, prompt])
            else:
                response = model.generate_content(f"Act as a CBSE Math Expert. Solve/Prove: {prompt}")
            st.markdown(response.text)

elif chapter == "Relations & Functions":
    st.header("Relations & Functions")
    math_keyboard("Relations")
    rel_type = st.text_input("Enter Relation pairs (e.g. (1,1),(2,2))")
    if st.button("Check Equivalence"):
        res = model.generate_content(f"Check if relation {rel_type} on set {{1,2,3}} is reflexive, symmetric, and transitive.")
        st.write(res.text)

elif chapter == "Matrices & Determinants":
    st.header("Matrices & Determinants")
    math_keyboard("Matrices")
    m_input = st.text_area("Matrix (rows by ';', elements by space)", "1 2; 3 4")
    if st.button("Calculate Matrix"):
        mat = Matrix([list(map(float, row.split())) for row in m_input.split(';')])
        st.latex(rf"|A| = {mat.det()}")
        if mat.det() != 0: st.latex(rf"A^{{-1}} = {latex(mat.inv())}")

elif chapter == "Calculus (Integrals & Diff)":
    st.header("Calculus Engine")
    math_keyboard("Calculus")
    func = st.text_input("Enter Function f(x)", "sin(x) + x**2")
    action = st.selectbox("Action", ["Differentiate", "Integrate", "Limit at x=0"])
    
    if st.button("Run Calculus"):
        expr = sympify(func)
        if action == "Differentiate": res = diff(expr, x)
        elif action == "Integrate": res = integrate(expr, x)
        else: res = Limit(expr, x, 0).doit()
        st.latex(latex(res))

elif chapter == "Vector & 3D Geometry":
    st.header("Vector & 3D Geometry")
    math_keyboard("Vectors")
    v1 = st.text_input("Vector A (e.g., 1, 0, 2)", "1, 0, 2")
    v2 = st.text_input("Vector B (e.g., 3, 1, 1)", "3, 1, 1")
    if st.button("Find Cross Product"):
        a = Matrix(list(map(float, v1.split(','))))
        b = Matrix(list(map(float, v2.split(','))))
        st.latex(latex(a.cross(b)))
