import streamlit as st

def math_keyboard():
    """
    Crea un teclado matemático visual similar al de Math Solver de Microsoft.
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
    if "math_keyboard_category" not in st.session_state:
        st.session_state.math_keyboard_category = "Básica"
    if "math_expression" not in st.session_state:
        st.session_state.math_expression = ""
    
    st.markdown("<div class='math-keyboard-container'>", unsafe_allow_html=True)
    
    # Categorías del teclado
    st.markdown("<div style='display: flex; overflow-x: auto; padding-bottom: 10px;'>", unsafe_allow_html=True)
    categories = ["Básica", "Álgebra", "Trigonometría", "Cálculo", "Estadísticas", "Matrices"]
    for category in categories:
        active = "active" if st.session_state.math_keyboard_category == category else ""
        if st.button(category, key=f"category_{category}", 
                     help=f"Cambiar a categoría {category}"):
            st.session_state.math_keyboard_category = category
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Subcategorías y botones basados en la categoría seleccionada
    if st.session_state.math_keyboard_category == "Básica":
        cols = st.columns(6)
        # Primera fila
        if cols[0].button("7", key="btn_7"):
            st.session_state.math_expression += "7"
        if cols[1].button("8", key="btn_8"):
            st.session_state.math_expression += "8"
        if cols[2].button("9", key="btn_9"):
            st.session_state.math_expression += "9"
        if cols[3].button("÷", key="btn_div"):
            st.session_state.math_expression += "/"
        if cols[4].button("(", key="btn_open"):
            st.session_state.math_expression += "("
        if cols[5].button(")", key="btn_close"):
            st.session_state.math_expression += ")"
            
        # Segunda fila
        if cols[0].button("4", key="btn_4"):
            st.session_state.math_expression += "4"
        if cols[1].button("5", key="btn_5"):
            st.session_state.math_expression += "5"
        if cols[2].button("6", key="btn_6"):
            st.session_state.math_expression += "6"
        if cols[3].button("×", key="btn_mult"):
            st.session_state.math_expression += "*"
        if cols[4].button("^", key="btn_pow"):
            st.session_state.math_expression += "^"
        if cols[5].button("√", key="btn_sqrt"):
            st.session_state.math_expression += "sqrt("
            
        # Tercera fila
        if cols[0].button("1", key="btn_1"):
            st.session_state.math_expression += "1"
        if cols[1].button("2", key="btn_2"):
            st.session_state.math_expression += "2"
        if cols[2].button("3", key="btn_3"):
            st.session_state.math_expression += "3"
        if cols[3].button("-", key="btn_minus"):
            st.session_state.math_expression += "-"
        if cols[4].button("π", key="btn_pi"):
            st.session_state.math_expression += "pi"
        if cols[5].button("e", key="btn_e"):
            st.session_state.math_expression += "e"
            
        # Cuarta fila
        if cols[0].button("0", key="btn_0"):
            st.session_state.math_expression += "0"
        if cols[1].button(".", key="btn_dot"):
            st.session_state.math_expression += "."
        if cols[2].button("x", key="btn_x"):
            st.session_state.math_expression += "x"
        if cols[3].button("+", key="btn_plus"):
            st.session_state.math_expression += "+"
        if cols[4].button("=", key="btn_equals"):
            st.session_state.math_expression += "="
        if cols[5].button("C", key="btn_clear"):
            st.session_state.math_expression = ""
    
    elif st.session_state.math_keyboard_category == "Trigonometría":
        cols = st.columns(6)
        # Primera fila
        if cols[0].button("sin", key="btn_sin"):
            st.session_state.math_expression += "sin("
        if cols[1].button("cos", key="btn_cos"):
            st.session_state.math_expression += "cos("
        if cols[2].button("tan", key="btn_tan"):
            st.session_state.math_expression += "tan("
        if cols[3].button("csc", key="btn_csc"):
            st.session_state.math_expression += "csc("
        if cols[4].button("sec", key="btn_sec"):
            st.session_state.math_expression += "sec("
        if cols[5].button("cot", key="btn_cot"):
            st.session_state.math_expression += "cot("
            
        # Segunda fila
        if cols[0].button("arcsin", key="btn_arcsin"):
            st.session_state.math_expression += "asin("
        if cols[1].button("arccos", key="btn_arccos"):
            st.session_state.math_expression += "acos("
        if cols[2].button("arctan", key="btn_arctan"):
            st.session_state.math_expression += "atan("
        if cols[3].button("sinh", key="btn_sinh"):
            st.session_state.math_expression += "sinh("
        if cols[4].button("cosh", key="btn_cosh"):
            st.session_state.math_expression += "cosh("
        if cols[5].button("tanh", key="btn_tanh"):
            st.session_state.math_expression += "tanh("
    
    elif st.session_state.math_keyboard_category == "Cálculo":
        st.markdown("#### Diferenciales")
        cols1 = st.columns(2)
        if cols1[0].button("d/dx", key="btn_diff"):
            st.session_state.math_expression += "diff("
        if cols1[1].button("d²/dx²", key="btn_diff2"):
            st.session_state.math_expression += "diff(,2)"
        
        st.markdown("#### Integrales")
        cols2 = st.columns(2)
        if cols2[0].button("∫", key="btn_int"):
            st.session_state.math_expression += "integrate("
        if cols2[1].button("∫ₐᵇ", key="btn_defint"):
            st.session_state.math_expression += "integrate(,,a,b)"
        
        st.markdown("#### Límites")
        cols3 = st.columns(3)
        if cols3[0].button("lim x→a", key="btn_lim"):
            st.session_state.math_expression += "limit(,x,a)"
        if cols3[1].button("lim x→∞", key="btn_liminf"):
            st.session_state.math_expression += "limit(,x,oo)"
        if cols3[2].button("lim x→-∞", key="btn_limninf"):
            st.session_state.math_expression += "limit(,x,-oo)"
    
    elif st.session_state.math_keyboard_category == "Álgebra":
        cols = st.columns(3)
        # Primera fila
        if cols[0].button("x²", key="btn_x2"):
            st.session_state.math_expression += "^2"
        if cols[1].button("x³", key="btn_x3"):
            st.session_state.math_expression += "^3"
        if cols[2].button("xⁿ", key="btn_xn"):
            st.session_state.math_expression += "^"
            
        # Segunda fila
        if cols[0].button("log", key="btn_log"):
            st.session_state.math_expression += "log("
        if cols[1].button("ln", key="btn_ln"):
            st.session_state.math_expression += "log("
        if cols[2].button("log₁₀", key="btn_log10"):
            st.session_state.math_expression += "log10("
            
        # Tercera fila
        if cols[0].button("|x|", key="btn_abs"):
            st.session_state.math_expression += "abs("
        if cols[1].button("⌊x⌋", key="btn_floor"):
            st.session_state.math_expression += "floor("
        if cols[2].button("⌈x⌉", key="btn_ceil"):
            st.session_state.math_expression += "ceiling("
    
    # Controles generales
    col1, col2, col3 = st.columns(3)
    if col1.button("Borrar Todo", key="btn_clear_all"):
        st.session_state.math_expression = ""
    if col2.button("Borrar Último", key="btn_backspace"):
        st.session_state.math_expression = st.session_state.math_expression[:-1]
    if col3.button("Cerrar Teclado", key="btn_close"):
        return False
    
    st.markdown("</div>", unsafe_allow_html=True)
    return True