import streamlit as st
from sympy import symbols, sympify, diff, integrate, Matrix, solve, expand, simplify, latex

# Set up the page
st.set_page_config(page_title="CBSE Class 12 Math AI", layout="wide")
st.title("📘 CBSE Class 12 Math Solver")
st.markdown("Select a chapter from the sidebar to solve NCERT-level problems.")

# Sidebar Navigation
chapter = st.sidebar.selectbox(
    "Choose Chapter",
    ["Relations & Functions", "Algebra (Matrices & Det)", "Calculus (Diff & Int)", "Vectors & 3D Geometry"]
)

x, y, z = symbols('x y z')

# --- CHAPTER 1: RELATIONS & FUNCTIONS ---
if chapter == "Relations & Functions":
    st.header("Relations and Functions")
    st.write("Determine the nature of a Relation R on Set A = {1, 2, 3...}")
    
    set_input = st.text_input("Enter Set A (comma separated)", "1, 2, 3")
    rel_input = st.text_input("Enter Relation R as pairs (e.g., (1,1), (2,2))", "(1,1), (2,2), (3,3)")
    
    if st.button("Analyze Relation"):
        A = set(set_input.split(","))
        # Simple parser for pairs
        try:
            pairs = eval(f"[{rel_input}]")
            is_reflexive = all((i, i) in pairs for i in A)
            is_symmetric = all((b, a) in pairs for (a, b) in pairs)
            is_transitive = True
            for (a, b) in pairs:
                for (c, d) in pairs:
                    if b == c and (a, d) not in pairs:
                        is_transitive = False
            
            st.write(f"**Reflexive:** {is_reflexive}")
            st.write(f"**Symmetric:** {is_symmetric}")
            st.write(f"**Transitive:** {is_transitive}")
            
            if is_reflexive and is_symmetric and is_transitive:
                st.success("This is an Equivalence Relation!")
        except:
            st.error("Check your pair formatting.")

# --- CHAPTER 2: MATRICES & DETERMINANTS ---
elif chapter == "Algebra (Matrices & Det)":
    st.header("Matrices and Determinants")
    matrix_input = st.text_area("Enter Matrix (Rows separated by semicolons, elements by spaces)", "1 2; 3 4")
    
    if st.button("Calculate"):
        try:
            mat = Matrix([list(map(float, row.split())) for row in matrix_input.split(';')])
            st.write("**Original Matrix:**")
            st.latex(latex(mat))
            
            st.write(f"**Determinant:** {mat.det()}")
            
            if mat.is_square and mat.det() != 0:
                st.write("**Inverse Matrix:**")
                st.latex(latex(mat.inv()))
            else:
                st.warning("Matrix is singular or not square; Inverse doesn't exist.")
        except:
            st.error("Invalid Matrix format.")

# --- CHAPTER 3: CALCULUS ---
elif chapter == "Calculus (Diff & Int)":
    st.header("Differential & Integral Calculus")
    calc_type = st.radio("Operation", ["Differentiation", "Integration", "Limit"])
    expr_input = st.text_input("Enter Expression (use * for mult, ** for power)", "x**2 + sin(x)")
    
    if st.button("Solve Step"):
        try:
            expr = sympify(expr_input)
            if calc_type == "Differentiation":
                result = diff(expr, x)
                st.latex(rf"\frac{{d}}{{dx}}({latex(expr)}) = {latex(result)}")
            elif calc_type == "Integration":
                result = integrate(expr, x)
                st.latex(rf"\int {latex(expr)} \, dx = {latex(result)} + C")
        except:
            st.error("Please check your math syntax.")

# --- CHAPTER 4: VECTORS ---
elif chapter == "Vectors & 3D Geometry":
    st.header("Vector Algebra")
    st.write("Define Vectors as [x, y, z]")
    v1_raw = st.text_input("Vector A", "1, 2, 3")
    v2_raw = st.text_input("Vector B", "4, 5, 6")
    
    if st.button("Compute Vectors"):
        a = Matrix(list(map(float, v1_raw.split(','))))
        b = Matrix(list(map(float, v2_raw.split(','))))
        
        dot_product = a.dot(b)
        cross_product = a.cross(b)
        
        st.write(f"**Dot Product (A.B):** {dot_product}")
        st.write("**Cross Product (AxB):**")
        st.latex(latex(cross_product))