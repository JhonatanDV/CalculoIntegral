import streamlit as st

def math_keyboard(prefix=""):
    """
    Crea un teclado matemático visual similar al de Math Solver de Microsoft.
    
    Args:
        prefix (str): Prefijo para crear claves únicas
    
    Returns:
        bool: True si el teclado sigue abierto, False si debe cerrarse
    """
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
    .math-category {
        background-color: #e0f7fa;
        border-radius: 4px;
        padding: 4px 12px;
        margin: 4px;
        cursor: pointer;
        font-weight: bold;
    }
    .math-category.active {
        background-color: #4fc3f7;
        color: white;
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
    
    # Inicializar el estado de la sesión para el teclado
    category_key = f"math_keyboard_category_{prefix}"
    if category_key not in st.session_state:
        st.session_state[category_key] = "Básica"
    
    expr_key = f"math_expression_{prefix}"
    if expr_key not in st.session_state:
        st.session_state[expr_key] = ""
    
    st.markdown("<div class='math-keyboard-container'>", unsafe_allow_html=True)
    
    # Categorías del teclado
    st.markdown("<div style='display: flex; overflow-x: auto; padding-bottom: 10px;'>", unsafe_allow_html=True)
    categories = ["Básica", "Álgebra", "Trigonometría", "Cálculo"]
    for category in categories:
        active = "active" if st.session_state[category_key] == category else ""
        if st.button(category, key=f"{prefix}_category_{category}", 
                     help=f"Cambiar a categoría {category}"):
            st.session_state[category_key] = category
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Subcategorías y botones basados en la categoría seleccionada
    if st.session_state[category_key] == "Básica":
        cols = st.columns(6)
        # Primera fila
        if cols[0].button("7", key=f"{prefix}_btn_7"):
            st.session_state[expr_key] += "7"
        if cols[1].button("8", key=f"{prefix}_btn_8"):
            st.session_state[expr_key] += "8"
        if cols[2].button("9", key=f"{prefix}_btn_9"):
            st.session_state[expr_key] += "9"
        if cols[3].button("÷", key=f"{prefix}_btn_div"):
            st.session_state[expr_key] += "/"
        if cols[4].button("(", key=f"{prefix}_btn_open"):
            st.session_state[expr_key] += "("
        if cols[5].button(")", key=f"{prefix}_btn_close"):
            st.session_state[expr_key] += ")"
            
        # Segunda fila
        if cols[0].button("4", key=f"{prefix}_btn_4"):
            st.session_state[expr_key] += "4"
        if cols[1].button("5", key=f"{prefix}_btn_5"):
            st.session_state[expr_key] += "5"
        if cols[2].button("6", key=f"{prefix}_btn_6"):
            st.session_state[expr_key] += "6"
        if cols[3].button("×", key=f"{prefix}_btn_mult"):
            st.session_state[expr_key] += "*"
        if cols[4].button("^", key=f"{prefix}_btn_pow"):
            st.session_state[expr_key] += "^"
        if cols[5].button("√", key=f"{prefix}_btn_sqrt"):
            st.session_state[expr_key] += "sqrt("
            
        # Tercera fila
        if cols[0].button("1", key=f"{prefix}_btn_1"):
            st.session_state[expr_key] += "1"
        if cols[1].button("2", key=f"{prefix}_btn_2"):
            st.session_state[expr_key] += "2"
        if cols[2].button("3", key=f"{prefix}_btn_3"):
            st.session_state[expr_key] += "3"
        if cols[3].button("-", key=f"{prefix}_btn_minus"):
            st.session_state[expr_key] += "-"
        if cols[4].button("π", key=f"{prefix}_btn_pi"):
            st.session_state[expr_key] += "pi"
        if cols[5].button("e", key=f"{prefix}_btn_e"):
            st.session_state[expr_key] += "e"
            
        # Cuarta fila
        if cols[0].button("0", key=f"{prefix}_btn_0"):
            st.session_state[expr_key] += "0"
        if cols[1].button(".", key=f"{prefix}_btn_dot"):
            st.session_state[expr_key] += "."
        if cols[2].button("x", key=f"{prefix}_btn_x"):
            st.session_state[expr_key] += "x"
        if cols[3].button("+", key=f"{prefix}_btn_plus"):
            st.session_state[expr_key] += "+"
        if cols[4].button("=", key=f"{prefix}_btn_equals"):
            st.session_state[expr_key] += "="
        if cols[5].button("C", key=f"{prefix}_btn_clear"):
            st.session_state[expr_key] = ""
    
    elif st.session_state[category_key] == "Trigonometría":
        cols = st.columns(3)
        # Primera fila
        if cols[0].button("sin", key=f"{prefix}_btn_sin"):
            st.session_state[expr_key] += "sin("
        if cols[1].button("cos", key=f"{prefix}_btn_cos"):
            st.session_state[expr_key] += "cos("
        if cols[2].button("tan", key=f"{prefix}_btn_tan"):
            st.session_state[expr_key] += "tan("
            
        # Segunda fila
        if cols[0].button("csc", key=f"{prefix}_btn_csc"):
            st.session_state[expr_key] += "csc("
        if cols[1].button("sec", key=f"{prefix}_btn_sec"):
            st.session_state[expr_key] += "sec("
        if cols[2].button("cot", key=f"{prefix}_btn_cot"):
            st.session_state[expr_key] += "cot("
            
        # Tercera fila
        if cols[0].button("arcsin", key=f"{prefix}_btn_arcsin"):
            st.session_state[expr_key] += "asin("
        if cols[1].button("arccos", key=f"{prefix}_btn_arccos"):
            st.session_state[expr_key] += "acos("
        if cols[2].button("arctan", key=f"{prefix}_btn_arctan"):
            st.session_state[expr_key] += "atan("
            
        # Cuarta fila
        if cols[0].button("sinh", key=f"{prefix}_btn_sinh"):
            st.session_state[expr_key] += "sinh("
        if cols[1].button("cosh", key=f"{prefix}_btn_cosh"):
            st.session_state[expr_key] += "cosh("
        if cols[2].button("tanh", key=f"{prefix}_btn_tanh"):
            st.session_state[expr_key] += "tanh("
    
    elif st.session_state[category_key] == "Cálculo":
        st.markdown("#### Diferenciales")
        cols1 = st.columns(2)
        if cols1[0].button("d/dx", key=f"{prefix}_btn_diff"):
            st.session_state[expr_key] += "diff("
        if cols1[1].button("d²/dx²", key=f"{prefix}_btn_diff2"):
            st.session_state[expr_key] += "diff(,2)"
        
        st.markdown("#### Integrales")
        cols2 = st.columns(2)
        if cols2[0].button("∫", key=f"{prefix}_btn_int"):
            st.session_state[expr_key] += "integrate("
        if cols2[1].button("∫ₐᵇ", key=f"{prefix}_btn_defint"):
            st.session_state[expr_key] += "integrate(,,a,b)"
        
        st.markdown("#### Límites")
        cols3 = st.columns(3)
        if cols3[0].button("lim x→a", key=f"{prefix}_btn_lim"):
            st.session_state[expr_key] += "limit(,x,a)"
        if cols3[1].button("lim x→∞", key=f"{prefix}_btn_liminf"):
            st.session_state[expr_key] += "limit(,x,oo)"
        if cols3[2].button("lim x→-∞", key=f"{prefix}_btn_limninf"):
            st.session_state[expr_key] += "limit(,x,-oo)"
    
    elif st.session_state[category_key] == "Álgebra":
        cols = st.columns(3)
        # Primera fila
        if cols[0].button("x²", key=f"{prefix}_btn_x2"):
            st.session_state[expr_key] += "^2"
        if cols[1].button("x³", key=f"{prefix}_btn_x3"):
            st.session_state[expr_key] += "^3"
        if cols[2].button("xⁿ", key=f"{prefix}_btn_xn"):
            st.session_state[expr_key] += "^"
            
        # Segunda fila
        if cols[0].button("log", key=f"{prefix}_btn_log"):
            st.session_state[expr_key] += "log("
        if cols[1].button("ln", key=f"{prefix}_btn_ln"):
            st.session_state[expr_key] += "log("
        if cols[2].button("log₁₀", key=f"{prefix}_btn_log10"):
            st.session_state[expr_key] += "log10("
            
        # Tercera fila
        if cols[0].button("|x|", key=f"{prefix}_btn_abs"):
            st.session_state[expr_key] += "abs("
        if cols[1].button("⌊x⌋", key=f"{prefix}_btn_floor"):
            st.session_state[expr_key] += "floor("
        if cols[2].button("⌈x⌉", key=f"{prefix}_btn_ceil"):
            st.session_state[expr_key] += "ceiling("
    
    # Muestra la expresión actual
    st.text_area("Expresión Actual:", value=st.session_state[expr_key], height=70, key=f"{prefix}_current_expr")
    
    # Controles generales
    col1, col2, col3 = st.columns(3)
    if col1.button("Borrar Todo", key=f"{prefix}_btn_clear_all"):
        st.session_state[expr_key] = ""
    if col2.button("Borrar Último", key=f"{prefix}_btn_backspace"):
        if st.session_state[expr_key]:
            st.session_state[expr_key] = st.session_state[expr_key][:-1]
    if col3.button("Cerrar Teclado", key=f"{prefix}_btn_close"):
        return False
    
    st.markdown("</div>", unsafe_allow_html=True)
    return True