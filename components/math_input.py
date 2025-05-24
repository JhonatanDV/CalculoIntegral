import streamlit as st
import sympy as sp

def create_math_input(label, default="", key=None):
    """
    Create a math input field with an optional virtual keyboard.
    
    Args:
        label (str): Label for the input field
        default (str): Default value for the input field
        key (str): Unique key for the input field
    
    Returns:
        str: The input value
    """
    # Set up session state for this input if it doesn't exist
    keyboard_key = f"show_keyboard_{key}"
    if keyboard_key not in st.session_state:
        st.session_state[keyboard_key] = False
    
    # Set up session state for the input value
    input_key = f"input_value_{key}"
    if input_key not in st.session_state:
        st.session_state[input_key] = default
    
    col1, col2 = st.columns([5, 1])
    
    with col1:
        input_value = st.text_input(label, value=st.session_state[input_key], key=key)
        # Update session state after user input
        st.session_state[input_key] = input_value
    
    with col2:
        if st.button("📝", key=f"keyboard_{key}"):
            st.session_state[keyboard_key] = not st.session_state[keyboard_key]
            st.rerun()
    
    if st.session_state[keyboard_key]:
        enhanced_math_keyboard(key)
    
    # Display the rendered LaTeX for preview
    try:
        if input_value:
            expr = sp.sympify(input_value.replace("^", "**"))
            st.latex(expr)
    except:
        pass
    
    return input_value

def enhanced_math_keyboard(parent_key):
    """
    Enhanced mathematical keyboard based on the reference images.
    
    Args:
        parent_key (str): Key of the parent input field
    """
    input_key = f"input_value_{parent_key}"
    
    st.markdown("### Calculadora Matemática")
    
    # Create tabs for different categories
    tabs = st.tabs([
        "Básica", "Trigonométrica", "Cálculo", "Algebraica", "Números"
    ])
    
    # Basic Tab
    with tabs[0]:
        st.markdown("#### Operaciones Básicas")
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        
        # Row 1
        if col1.button("DEG", key=f"deg_btn_{parent_key}"):
            st.session_state[input_key] += "deg"
            st.rerun()
        if col2.button("x", key=f"varx_btn_{parent_key}"):
            st.session_state[input_key] += "x"
            st.rerun()
        if col3.button("y", key=f"vary_btn_{parent_key}"):
            st.session_state[input_key] += "y"
            st.rerun()
        if col4.button("(", key=f"open_btn_{parent_key}"):
            st.session_state[input_key] += "("
            st.rerun()
        if col5.button(")", key=f"close_btn_{parent_key}"):
            st.session_state[input_key] += ")"
            st.rerun()
        if col6.button("%", key=f"percent_btn_{parent_key}"):
            st.session_state[input_key] += "%"
            st.rerun()
        
        # Row 2
        if col1.button("π", key=f"pi_btn_{parent_key}"):
            st.session_state[input_key] += "pi"
            st.rerun()
        if col2.button("7", key=f"7_btn_{parent_key}"):
            st.session_state[input_key] += "7"
            st.rerun()
        if col3.button("8", key=f"8_btn_{parent_key}"):
            st.session_state[input_key] += "8"
            st.rerun()
        if col4.button("9", key=f"9_btn_{parent_key}"):
            st.session_state[input_key] += "9"
            st.rerun()
        if col5.button("÷", key=f"div_btn_{parent_key}"):
            st.session_state[input_key] += "/"
            st.rerun()
        
        # Row 3
        if col1.button("log", key=f"log_btn_{parent_key}"):
            st.session_state[input_key] += "log("
            st.rerun()
        if col2.button("4", key=f"4_btn_{parent_key}"):
            st.session_state[input_key] += "4"
            st.rerun()
        if col3.button("5", key=f"5_btn_{parent_key}"):
            st.session_state[input_key] += "5"
            st.rerun()
        if col4.button("6", key=f"6_btn_{parent_key}"):
            st.session_state[input_key] += "6"
            st.rerun()
        if col5.button("×", key=f"mult_btn_{parent_key}"):
            st.session_state[input_key] += "*"
            st.rerun()
        
        # Row 4
        if col1.button("√", key=f"sqrt_btn_{parent_key}"):
            st.session_state[input_key] += "sqrt("
            st.rerun()
        if col2.button("1", key=f"1_btn_{parent_key}"):
            st.session_state[input_key] += "1"
            st.rerun()
        if col3.button("2", key=f"2_btn_{parent_key}"):
            st.session_state[input_key] += "2"
            st.rerun()
        if col4.button("3", key=f"3_btn_{parent_key}"):
            st.session_state[input_key] += "3"
            st.rerun()
        if col5.button("−", key=f"minus_btn_{parent_key}"):
            st.session_state[input_key] += "-"
            st.rerun()
        
        # Row 5
        if col1.button("exp", key=f"exp_btn_{parent_key}"):
            st.session_state[input_key] += "exp("
            st.rerun()
        if col2.button("0", key=f"0_btn_{parent_key}"):
            st.session_state[input_key] += "0"
            st.rerun()
        if col3.button(".", key=f"dot_btn_{parent_key}"):
            st.session_state[input_key] += "."
            st.rerun()
        if col4.button("=", key=f"eq_btn_{parent_key}"):
            st.session_state[input_key] += "="
            st.rerun()
        if col5.button("+", key=f"plus_btn_{parent_key}"):
            st.session_state[input_key] += "+"
            st.rerun()
    
    # Trigonometric Tab
    with tabs[1]:
        st.markdown("#### Funciones Trigonométricas")
        
        st.markdown("##### Básica")
        col1, col2, col3 = st.columns(3)
        if col1.button("sin", key=f"sin_btn_{parent_key}"):
            st.session_state[input_key] += "sin("
            st.rerun()
        if col2.button("cos", key=f"cos_btn_{parent_key}"):
            st.session_state[input_key] += "cos("
            st.rerun()
        if col3.button("tan", key=f"tan_btn_{parent_key}"):
            st.session_state[input_key] += "tan("
            st.rerun()
        
        st.markdown("##### Recíprocos")
        col1, col2, col3 = st.columns(3)
        if col1.button("csc", key=f"csc_btn_{parent_key}"):
            st.session_state[input_key] += "csc("
            st.rerun()
        if col2.button("sec", key=f"sec_btn_{parent_key}"):
            st.session_state[input_key] += "sec("
            st.rerun()
        if col3.button("cot", key=f"cot_btn_{parent_key}"):
            st.session_state[input_key] += "cot("
            st.rerun()
        
        st.markdown("##### Hiperbólico")
        col1, col2, col3 = st.columns(3)
        if col1.button("sinh", key=f"sinh_btn_{parent_key}"):
            st.session_state[input_key] += "sinh("
            st.rerun()
        if col2.button("cosh", key=f"cosh_btn_{parent_key}"):
            st.session_state[input_key] += "cosh("
            st.rerun()
        if col3.button("tanh", key=f"tanh_btn_{parent_key}"):
            st.session_state[input_key] += "tanh("
            st.rerun()
    
    # Calculus Tab
    with tabs[2]:
        st.markdown("#### Cálculo")
        
        st.markdown("##### Diferenciales")
        col1, col2 = st.columns(2)
        if col1.button("d/dx", key=f"ddx_btn_{parent_key}"):
            st.session_state[input_key] += "diff("
            st.rerun()
        if col2.button("d²/dx²", key=f"d2dx2_btn_{parent_key}"):
            st.session_state[input_key] += "diff(,2)"
            st.rerun()
        
        st.markdown("##### Integrales")
        col1, col2 = st.columns(2)
        if col1.button("∫", key=f"int_btn_{parent_key}"):
            st.session_state[input_key] += "∫("
            st.rerun()
        if col2.button("∫ₐᵇ", key=f"defint_btn_{parent_key}"):
            st.session_state[input_key] += "∫("
            st.rerun()
        
        st.markdown("##### Límites")
        col1, col2, col3 = st.columns(3)
        if col1.button("lim x→a", key=f"lim_btn_{parent_key}"):
            st.session_state[input_key] += "limit(,x,a)"
            st.rerun()
        if col2.button("lim x→∞", key=f"liminf_btn_{parent_key}"):
            st.session_state[input_key] += "limit(,x,oo)"
            st.rerun()
        if col3.button("lim x→-∞", key=f"limneginf_btn_{parent_key}"):
            st.session_state[input_key] += "limit(,x,-oo)"
            st.rerun()
    
    # Algebraic Tab
    with tabs[3]:
        st.markdown("#### Álgebra")
        
        st.markdown("##### Desigualdades")
        col1, col2, col3, col4 = st.columns(4)
        if col1.button("<", key=f"lt_btn_{parent_key}"):
            st.session_state[input_key] += "<"
            st.rerun()
        if col2.button("≤", key=f"leq_btn_{parent_key}"):
            st.session_state[input_key] += "<="
            st.rerun()
        if col3.button(">", key=f"gt_btn_{parent_key}"):
            st.session_state[input_key] += ">"
            st.rerun()
        if col4.button("≥", key=f"geq_btn_{parent_key}"):
            st.session_state[input_key] += ">="
            st.rerun()
        
        st.markdown("##### Valor absoluto y redondeo")
        col1, col2, col3 = st.columns(3)
        if col1.button("|x|", key=f"abs_btn_{parent_key}"):
            st.session_state[input_key] += "abs("
            st.rerun()
        if col2.button("⌊x⌋", key=f"floor_btn_{parent_key}"):
            st.session_state[input_key] += "floor("
            st.rerun()
        if col3.button("⌈x⌉", key=f"ceil_btn_{parent_key}"):
            st.session_state[input_key] += "ceiling("
            st.rerun()
        
        st.markdown("##### Exponentes")
        col1, col2, col3 = st.columns(3)
        if col1.button("xⁿ", key=f"xn_btn_{parent_key}"):
            st.session_state[input_key] += "^"
            st.rerun()
        if col2.button("x²", key=f"x2_btn_{parent_key}"):
            st.session_state[input_key] += "^2"
            st.rerun()
        if col3.button("x³", key=f"x3_btn_{parent_key}"):
            st.session_state[input_key] += "^3"
            st.rerun()
    
    # Numbers Tab
    with tabs[4]:
        st.markdown("#### Números y Constantes")
        col1, col2 = st.columns(2)
        if col1.button("e (Euler)", key=f"euler_btn_{parent_key}"):
            st.session_state[input_key] += "e"
            st.rerun()
        if col2.button("i (imaginario)", key=f"i_btn_{parent_key}"):
            st.session_state[input_key] += "I"
            st.rerun()
        if col1.button("∞ (infinito)", key=f"inf_btn_{parent_key}"):
            st.session_state[input_key] += "oo"
            st.rerun()
        if col2.button("φ (proporción áurea)", key=f"golden_btn_{parent_key}"):
            st.session_state[input_key] += "GoldenRatio"
            st.rerun()
    
    # Control buttons
    col1, col2, col3 = st.columns(3)
    if col1.button("Borrar Todo", key=f"clear_btn_{parent_key}", use_container_width=True):
        st.session_state[input_key] = ""
        st.rerun()
    if col2.button("Borrar Último", key=f"backspace_btn_{parent_key}", use_container_width=True):
        if st.session_state[input_key]:
            st.session_state[input_key] = st.session_state[input_key][:-1]
            st.rerun()
    if col3.button("Cerrar Teclado", key=f"close_btn_{parent_key}", use_container_width=True):
        st.session_state[f"show_keyboard_{parent_key}"] = False
        st.rerun()

def create_math_keyboard():
    """
    Create a virtual math keyboard component.
    
    Returns:
        tuple: (is_used, expression) where is_used indicates if the keyboard was used
               and expression is the resulting expression
    """
    st.markdown("### Calculadora Matemática")
    
    # Initialize session state for the expression
    if "math_expression" not in st.session_state:
        st.session_state.math_expression = ""
    
    # Display current expression
    st.text_input("Expresión Actual", value=st.session_state.math_expression, key="expr_display", disabled=True)
    
    # Create tabs for different categories
    tabs = st.tabs([
        "Básica", "Trigonométrica", "Cálculo", "Algebraica", "Números"
    ])
    
    # Basic Tab
    with tabs[0]:
        st.markdown("#### Operaciones Básicas")
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        
        # Row 1
        if col1.button("DEG"):
            st.session_state.math_expression += "deg"
            return True, st.session_state.math_expression
        if col2.button("x"):
            st.session_state.math_expression += "x"
            return True, st.session_state.math_expression
        if col3.button("y"):
            st.session_state.math_expression += "y"
            return True, st.session_state.math_expression
        if col4.button("("):
            st.session_state.math_expression += "("
            return True, st.session_state.math_expression
        if col5.button(")"):
            st.session_state.math_expression += ")"
            return True, st.session_state.math_expression
        if col6.button("%"):
            st.session_state.math_expression += "%"
            return True, st.session_state.math_expression
        
        # Row 2
        if col1.button("π"):
            st.session_state.math_expression += "pi"
            return True, st.session_state.math_expression
        if col2.button("7"):
            st.session_state.math_expression += "7"
            return True, st.session_state.math_expression
        if col3.button("8"):
            st.session_state.math_expression += "8"
            return True, st.session_state.math_expression
        if col4.button("9"):
            st.session_state.math_expression += "9"
            return True, st.session_state.math_expression
        if col5.button("÷"):
            st.session_state.math_expression += "/"
            return True, st.session_state.math_expression
        
        # Similar implementation for other rows and tabs...
    
    # Control buttons
    col1, col2, col3 = st.columns(3)
    if col1.button("Borrar Todo", use_container_width=True):
        st.session_state.math_expression = ""
        return True, st.session_state.math_expression
    if col2.button("Borrar Último", use_container_width=True):
        if st.session_state.math_expression:
            st.session_state.math_expression = st.session_state.math_expression[:-1]
            return True, st.session_state.math_expression
    if col3.button("Usar Expresión", use_container_width=True):
        return True, st.session_state.math_expression
    
    return False, st.session_state.math_expression
