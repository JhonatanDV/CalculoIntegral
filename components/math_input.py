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
    col1, col2 = st.columns([5, 1])
    
    with col1:
        input_value = st.text_input(label, value=default, key=key)
    
    with col2:
        if st.button("📝", key=f"keyboard_{key}"):
            show_keyboard = True
            st.session_state[f"show_keyboard_{key}"] = True
        else:
            show_keyboard = st.session_state.get(f"show_keyboard_{key}", False)
    
    if show_keyboard:
        st.markdown("### Mathematical Symbols")
        cols = st.columns(4)
        
        # Common symbols
        symbols = [
            "+", "-", "*", "/", "^", "sqrt", 
            "sin", "cos", "tan", "exp", "log", 
            "pi", "e", "(", ")", "x", "y"
        ]
        
        for i, symbol in enumerate(symbols):
            col_idx = i % 4
            if cols[col_idx].button(symbol, key=f"{symbol}_{key}"):
                if symbol in ["sin", "cos", "tan", "exp", "log", "sqrt"]:
                    input_value += f"{symbol}("
                else:
                    input_value += symbol
                st.session_state[key] = input_value
                st.rerun()
        
        if st.button("Close Keyboard", key=f"close_keyboard_{key}"):
            st.session_state[f"show_keyboard_{key}"] = False
            st.rerun()
    
    # Display the rendered LaTeX for preview
    try:
        if input_value:
            expr = sp.sympify(input_value.replace("^", "**"))
            st.latex(expr)
    except:
        pass
    
    return input_value

def create_math_keyboard():
    """
    Create a virtual math keyboard component.
    
    Returns:
        tuple: (is_used, expression) where is_used indicates if the keyboard was used
               and expression is the resulting expression
    """
    st.markdown("### Mathematical Keyboard")
    
    # Initialize session state for the expression
    if "math_expression" not in st.session_state:
        st.session_state.math_expression = ""
    
    # Display current expression
    st.text_input("Current Expression", value=st.session_state.math_expression, key="expr_display", disabled=True)
    
    # Create keyboard layout
    col1, col2, col3, col4 = st.columns(4)
    
    # Numbers
    with col1:
        st.markdown("#### Numbers")
        num_cols = st.columns(3)
        for i in range(1, 10):
            col_idx = (i - 1) % 3
            if num_cols[col_idx].button(str(i), key=f"num_{i}"):
                st.session_state.math_expression += str(i)
                return True, st.session_state.math_expression
        
        if num_cols[0].button("0", key="num_0"):
            st.session_state.math_expression += "0"
            return True, st.session_state.math_expression
        
        if num_cols[1].button(".", key="decimal"):
            st.session_state.math_expression += "."
            return True, st.session_state.math_expression
        
        if num_cols[2].button("π", key="pi"):
            st.session_state.math_expression += "pi"
            return True, st.session_state.math_expression
    
    # Basic operations
    with col2:
        st.markdown("#### Operations")
        if st.button("+", key="add"):
            st.session_state.math_expression += "+"
            return True, st.session_state.math_expression
        
        if st.button("-", key="subtract"):
            st.session_state.math_expression += "-"
            return True, st.session_state.math_expression
        
        if st.button("×", key="multiply"):
            st.session_state.math_expression += "*"
            return True, st.session_state.math_expression
        
        if st.button("÷", key="divide"):
            st.session_state.math_expression += "/"
            return True, st.session_state.math_expression
        
        if st.button("^", key="power"):
            st.session_state.math_expression += "^"
            return True, st.session_state.math_expression
        
        if st.button("√", key="sqrt"):
            st.session_state.math_expression += "sqrt("
            return True, st.session_state.math_expression
    
    # Functions
    with col3:
        st.markdown("#### Functions")
        if st.button("sin", key="sin"):
            st.session_state.math_expression += "sin("
            return True, st.session_state.math_expression
        
        if st.button("cos", key="cos"):
            st.session_state.math_expression += "cos("
            return True, st.session_state.math_expression
        
        if st.button("tan", key="tan"):
            st.session_state.math_expression += "tan("
            return True, st.session_state.math_expression
        
        if st.button("exp", key="exp"):
            st.session_state.math_expression += "exp("
            return True, st.session_state.math_expression
        
        if st.button("log", key="log"):
            st.session_state.math_expression += "log("
            return True, st.session_state.math_expression
        
        if st.button("ln", key="ln"):
            st.session_state.math_expression += "log("
            return True, st.session_state.math_expression
    
    # Brackets and variables
    with col4:
        st.markdown("#### Other")
        if st.button("(", key="open_bracket"):
            st.session_state.math_expression += "("
            return True, st.session_state.math_expression
        
        if st.button(")", key="close_bracket"):
            st.session_state.math_expression += ")"
            return True, st.session_state.math_expression
        
        if st.button("x", key="var_x"):
            st.session_state.math_expression += "x"
            return True, st.session_state.math_expression
        
        if st.button("y", key="var_y"):
            st.session_state.math_expression += "y"
            return True, st.session_state.math_expression
        
        if st.button("e", key="const_e"):
            st.session_state.math_expression += "e"
            return True, st.session_state.math_expression
        
        if st.button("Clear", key="clear"):
            st.session_state.math_expression = ""
            return True, st.session_state.math_expression
    
    # Handle submission
    if st.button("Use Expression", key="use_expr"):
        return True, st.session_state.math_expression
    
    return False, st.session_state.math_expression
