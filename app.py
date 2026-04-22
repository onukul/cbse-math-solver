import streamlit as st
from sympy import symbols, sympify, diff, integrate, Matrix, latex, Limit, S
# Updated import for 2026 standards
import google.genai as genai 
from PIL import Image

# ... (keep your existing config and secrets code) ...

# --- NEW IMPROVED MATH KEYBOARD ---
def math_keyboard(layout_type):
    st.write(f"### ⌨️ {layout_type} Keyboard")
    
    # Comprehensive symbol sets for CBSE 12
    keyboards = {
        "General": ["^2", "^3", "sqrt(", "pi", "(", ")", "e", "+", "-", "*", "/", "="],
        "Calculus": ["d/dx", "∫", "limit(", "∞", "log(", "exp(", "sin(", "cos(", "tan("],
        "Matrices": ["det(", "inv(", "adj(", "T", "[", "]", ";", "0", "1", "I"],
        "Relations": ["∈", "⊂", "∀", "∃", "≤", "≥", "≠", "→", "R", "N", "Z"],
        "Vectors": ["î", "ĵ", "k̂", "·", "×", "| |", "θ", "λ", "μ"]
    }
    
    symbols_to_show = keyboards.get(layout_type, keyboards["General"])
    
    # Display buttons in a grid of 4 columns
    cols = st.columns(4) 
    for i, symbol in enumerate(symbols_to_show):
        with cols[i % 4]:
            if st.button(symbol, key=f"btn_{layout_type}_{symbol}_{i}"):
                # This creates a code block you can easily double-tap to copy
                st.code(symbol) 

# --- UPDATED CHAPTER SELECTION ---
# Ensure each chapter calls the correct keyboard
if chapter == "AI Chat: Proofs & Image Solver":
    math_keyboard("General")
    # ... rest of your code ...
elif chapter == "Relations & Functions":
    math_keyboard("Relations")
    # ... rest of your code ...
elif chapter == "Matrices & Determinants":
    math_keyboard("Matrices")
    # ... rest of your code ...
elif chapter == "Calculus (Integrals & Diff)":
    math_keyboard("Calculus")
    # ... rest of your code ...
elif chapter == "Vector & 3D Geometry":
    math_keyboard("Vectors")
    # ... rest of your code ...
