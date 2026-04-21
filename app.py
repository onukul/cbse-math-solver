import streamlit as st
from sympy import symbols, sympify, diff, integrate, Matrix, latex, Limit, S
import google.generativeai as genai
from PIL import Image

# --- CONFIGURATION ---
st.set_page_config(page_title="CBSE Class 12 Math Master", layout="wide")

# Setup Gemini for Proofs, Modelling, and Image Solving
# Instead of pasting the key here, we tell Streamlit to find it in "Secrets"
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
except KeyError:
    st.error("API Key not found. Please set 'GEMINI_API_KEY' in Streamlit Secrets.")
    st.stop()

genai.configure(api_key=GEMINI_API_KEY)

#model = genai.GenerativeModel('gemini-1.5-pro-latest')
model = genai.GenerativeModel('gemini-3-flash-preview')

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("📚 CBSE Syllabus")
chapter = st.sidebar.selectbox("Select Chapter", [
    "AI Chat: Proofs & Image Solver",
    "Relations & Functions",
    "Inverse Trig Functions",
    "Matrices & Determinants",
    "Continuity & Differentiability",
    "Calculus (Integrals & Diff)",
    "Application of Derivatives",
    "Vector & 3D Geometry",
    "Linear Programming",
    "Probability",
    "Mathematical Modelling"
])

x, y, z, t = symbols('x y z t')

# --- 1. AI CHAT: PROOFS, MODELLING, & IMAGES ---
if chapter == "AI Chat: Proofs & Image Solver":
    st.header("💬 AI Tutor: Proofs & Problem Solving")
    st.info("Use this for: Proofs, Mathematical Modelling, and Image Solving.")
    
    uploaded_file = st.file_uploader("➕ Upload Image", type=["jpg", "png", "jpeg"])
    if prompt := st.chat_input("Ask a question or type a theorem to prove..."):
        with st.chat_message("user"): st.markdown(prompt)
        with st.chat_message("assistant"):
            if uploaded_file:
                img = Image.open(uploaded_file)
                response = model.generate_content(["Solve this CBSE 12 problem step-by-step:", img, prompt])
            else:
                response = model.generate_content(f"Act as a CBSE Math Expert. Solve/Prove: {prompt}")
            st.markdown(response.text)

# --- 2. RELATIONS & FUNCTIONS ---
elif chapter == "Relations & Functions":
    st.header("Relations & Functions")
    rel_type = st.text_input("Enter Relation pairs for Set {1,2,3} (e.g. (1,1),(2,2),(3,3))")
    if st.button("Check Equivalence"):
        # The AI handles logic checks best for set-theory
        res = model.generate_content(f"Check if relation {rel_type} on set {{1,2,3}} is reflexive, symmetric, and transitive.")
        st.write(res.text)

# --- 3. MATRICES & DETERMINANTS ---
elif chapter == "Matrices & Determinants":
    st.header("Matrices & Determinants")
    m_input = st.text_area("Matrix (rows separated by ';', elements by space)", "1 2; 3 4")
    if st.button("Solve"):
        mat = Matrix([list(map(float, row.split())) for row in m_input.split(';')])
        st.latex(rf"|A| = {mat.det()}")
        if mat.det() != 0: st.latex(rf"A^{{-1}} = {latex(mat.inv())}")

# --- 4. CONTINUITY & CALCULUS ---
elif chapter in ["Continuity & Differentiability", "Calculus (Integrals & Diff)", "Application of Derivatives"]:
    st.header(f"Calculus Engine: {chapter}")
    func = st.text_input("Enter Function f(x)", "sin(x) + x**2")
    action = st.selectbox("Action", ["Differentiate", "Integrate", "Limit at x=0"])
    
    if st.button("Calculate"):
        expr = sympify(func)
        if action == "Differentiate": res = diff(expr, x)
        elif action == "Integrate": res = integrate(expr, x)
        else: res = Limit(expr, x, 0).doit()
        st.latex(latex(res))

# --- 5. VECTOR & 3D GEOMETRY ---
elif chapter == "Vector & 3D Geometry":
    st.header("Vector & 3D Geometry")
    v1 = st.text_input("Vector A (i, j, k)", "1, 0, 2")
    v2 = st.text_input("Vector B (i, j, k)", "3, 1, 1")
    if st.button("Find Cross Product"):
        a = Matrix(list(map(float, v1.split(','))))
        b = Matrix(list(map(float, v2.split(','))))
        st.latex(latex(a.cross(b)))

# --- 6. PROBABILITY & LPP ---
elif chapter in ["Linear Programming", "Probability", "Mathematical Modelling"]:
    st.header(chapter)
    st.write(f"Send your {chapter} question to the AI Expert for logical breakdown.")
    if st.button(f"Go to AI Chat"):
        st.info("Switch to the first tab in the sidebar to solve these complex topics!")
