import streamlit as st

def math_keyboard(prefix=""):
    """
    Crea un teclado matemático visual similar al de Math Solver de Microsoft.
    
    Args:
        prefix (str): Prefijo para crear claves únicas
    
    Returns:
        bool: True si el teclado sigue abierto, False si debe cerrarse
    """
    # Estilos CSS
    st.markdown("""
    <style>
    .math-button {
        background-color: #f8f9fa;
        border: 1px solid #d1d5db;
        border-radius: 4px;
        padding: 8px 12px;
        margin: 4px;
        cursor: pointer;
        font-size: 16px;
        text-align: center;
        min-width: 40px;
    }
    .math-button:hover {
        background-color: #e9ecef;
    }
    .math-category.active {
        background-color: #4fc3f7 !important;
        color: white !important;
    }
    .math-keyboard-container {
        border-radius: 8px;
        padding: 10px;
        background-color: #f8f9fa;
        border: 1px solid #d1d5db;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Inicializar estado
    category_key = f"math_keyboard_category_{prefix}"
    expr_key = f"math_expression_{prefix}"
    st.session_state.setdefault(category_key, "Básica")
    st.session_state.setdefault(expr_key, "")

    # Contenedor del teclado
    st.markdown("<div class='math-keyboard-container'>", unsafe_allow_html=True)

    # Menú de categorías
    st.markdown("<div style='display: flex; gap: 5px; overflow-x: auto;'>", unsafe_allow_html=True)
    categories = ["Básica", "Álgebra", "Trigonometría", "Cálculo"]
    for category in categories:
        if st.button(category, key=f"{prefix}_category_{category}"):
            st.session_state[category_key] = category
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # Teclado por categoría
    if st.session_state[category_key] == "Básica":
        cols = st.columns(6)
        rows = [
            ["7", "8", "9", "÷", "(", ")"],
            ["4", "5", "6", "×", "^", "√"],
            ["1", "2", "3", "-", "π", "e"],
            ["0", ".", "x", "+", "=", "C"]
        ]
        values = {
            "÷": "/", "×": "*", "^": "^", "√": "sqrt(",
            "π": "pi", "e": "e", "C": "", "=": "="
        }
        for i, row in enumerate(rows):
            for j, label in enumerate(row):
                if cols[j].button(label, key=f"{prefix}_btn_{label}_{i}"):
                    if label == "C":
                        st.session_state[expr_key] = ""
                    else:
                        st.session_state[expr_key] += values.get(label, label)

    elif st.session_state[category_key] == "Álgebra":
        cols = st.columns(3)
        rows = [
            [("x²", "^2"), ("x³", "^3"), ("xⁿ", "^")],
            [("log", "log("), ("ln", "ln("), ("abs", "abs(")]
        ]
        for row in rows:
            for i, (label, val) in enumerate(row):
                if cols[i].button(label, key=f"{prefix}_btn_{label}"):
                    st.session_state[expr_key] += val

    elif st.session_state[category_key] == "Trigonometría":
        cols = st.columns(3)
        rows = [
            [("sin", "sin("), ("cos", "cos("), ("tan", "tan(")],
            [("csc", "csc("), ("sec", "sec("), ("cot", "cot(")],
            [("arcsin", "asin("), ("arccos", "acos("), ("arctan", "atan(")],
            [("sinh", "sinh("), ("cosh", "cosh("), ("tanh", "tanh(")]
        ]
        for row in rows:
            for i, (label, val) in enumerate(row):
                if cols[i].button(label, key=f"{prefix}_btn_{label}"):
                    st.session_state[expr_key] += val

    elif st.session_state[category_key] == "Cálculo":
        st.markdown("**Diferenciales**")
        cols1 = st.columns(2)
        if cols1[0].button("d/dx", key=f"{prefix}_btn_diff"):
            st.session_state[expr_key] += "diff("
        if cols1[1].button("d²/dx²", key=f"{prefix}_btn_diff2"):
            st.session_state[expr_key] += "diff(,2)"

        st.markdown("**Integrales**")
        cols2 = st.columns(2)
        if cols2[0].button("∫", key=f"{prefix}_btn_int"):
            st.session_state[expr_key] += "integrate("
        if cols2[1].button("∫ₐᵇ", key=f"{prefix}_btn_defint"):
            st.session_state[expr_key] += "integrate(,,a,b)"

        st.markdown("**Límites**")
        cols3 = st.columns(3)
        if cols3[0].button("lim x→a", key=f"{prefix}_btn_lim"):
            st.session_state[expr_key] += "limit(,x,a)"
        if cols3[1].button("lim x→∞", key=f"{prefix}_btn_liminf"):
            st.session_state[expr_key] += "limit(,x,oo)"
        if cols3[2].button("lim x→-∞", key=f"{prefix}_btn_limninf"):
            st.session_state[expr_key] += "limit(,x,-oo)"

    # Mostrar expresión actual
    st.markdown("</div>", unsafe_allow_html=True)
    st.text_input("Expresión:", st.session_state[expr_key], key=f"{prefix}_display", disabled=True)

    return True
