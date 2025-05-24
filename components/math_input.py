import streamlit as st
import sympy as sp

def create_math_input(label, default="", key=None):
    """
    Create a math input field with LaTeX preview.
    
    Args:
        label (str): Label for the input field
        default (str): Default value for the input field
        key (str): Unique key for the input field
    
    Returns:
        str: The input value
    """
    # Set up session state for the input value
    input_key = f"input_value_{key}"
    if input_key not in st.session_state:
        st.session_state[input_key] = default
    
    # Create a unique text input key
    text_input_key = f"textinput_{key}"
    
    # Text input field
    input_value = st.text_input(label, value=st.session_state[input_key], key=text_input_key)
    
    # Update session state after user input
    st.session_state[input_key] = input_value
    
    # Display the rendered LaTeX for preview
    try:
        if input_value:
            expr = sp.sympify(input_value.replace("^", "**"))
            st.latex(expr)
    except:
        pass
    
    return input_value