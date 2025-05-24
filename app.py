import streamlit as st
import sympy as sp
from sympy import symbols, sympify, solve, diff, integrate, Rational
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from components.math_input import create_math_input
from components.solution_display import display_solution
from utils.calculator import evaluate_expression, solve_integral
from utils.plotting import plot_function, plot_integral
import streamlit.components.v1 as components

# Page configuration
st.set_page_config(
    page_title="CalcuMaster - Integral Calculus Solver",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Sidebar
st.sidebar.title("CalcuMaster")
st.sidebar.subheader("Integral Calculus Solver")

# Initialize session state variables if they don't exist
if 'function_str' not in st.session_state:
    st.session_state.function_str = "x^2"
if 'lower_bound' not in st.session_state:
    st.session_state.lower_bound = "0"
if 'upper_bound' not in st.session_state:
    st.session_state.upper_bound = "1"
if 'variable' not in st.session_state:
    st.session_state.variable = "x"
if 'n_subdivisions' not in st.session_state:
    st.session_state.n_subdivisions = 6
if 'input_value_home_function' not in st.session_state:
    st.session_state.input_value_home_function = "x^2"

# Setup for file upload (for image based math input)
def process_uploaded_math_image():
    # This function would be implemented with OCR capabilities 
    # to extract math equations from images
    st.info("La funcionalidad de procesamiento de imágenes matemáticas estará disponible próximamente.")

app_mode = st.sidebar.selectbox(
    "Selecciona un Modo",
    ["Home", "Riemann Sums", "Definite Integrals", "Area Between Curves", "Engineering Applications", "Software Engineering Scenarios"]
)

# Home page
if app_mode == "Home":
    st.title("🧮 CalcuMaster: Integral Calculus Solver")
    
    st.markdown("""
    ## Welcome to CalcuMaster!
    
    This application helps you solve and visualize integral calculus problems, with a focus on:
    
    - **Riemann Sums**: Calculate and visualize Riemann sums for definite integrals
    - **Definite Integrals**: Evaluate definite integrals and visualize the area under curves
    - **Area Between Curves**: Calculate and visualize the area between two curves
    - **Engineering Applications**: Solve engineering problems using integral calculus
    
    ### Getting Started
    
    1. Select an application mode from the sidebar
    2. Enter your mathematical expressions and parameters
    3. View the step-by-step solutions and visualizations
    
    ### About Integral Calculus
    
    Integral calculus is a powerful mathematical tool used to solve problems involving accumulation, area, volume, and more. 
    It is widely applied in engineering, physics, economics, and computer science.
    
    #### Key Concepts:
    
    - **Definite Integral**: $\\int_{a}^{b} f(x) dx$ represents the area under the curve $f(x)$ from $x=a$ to $x=b$
    - **Riemann Sum**: An approximation of the definite integral using a finite sum of areas of rectangles
    - **Fundamental Theorem of Calculus**: Connects differentiation and integration
    """)
    
    st.markdown("---")
    
    st.header("Quick Calculator")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Input Method Selection
        input_method = st.radio("Input Method", ["Keyboard", "Upload Image"], horizontal=True)
        
        if input_method == "Keyboard":
            function_input = create_math_input("Function f(x)", st.session_state.get("input_value_home_function", "x^2"), key="home_function")
        else:
            uploaded_file = st.file_uploader("Upload an image of a mathematical equation", type=["jpg", "jpeg", "png"], key="home_image_uploader")
            if uploaded_file is not None:
                st.image(uploaded_file, caption="Uploaded Math Expression", width=300)
                process_uploaded_math_image()
                st.error("Procesamiento de imágenes no disponible. Por favor ingresa la función manualmente.")
                function_input = st.text_input("Función reconocida", st.session_state.get("input_value_home_function", "x^2"), key="recognized_function")
            else:
                function_input = st.session_state.get("input_value_home_function", "x^2")
        
        # Save function to session state
        st.session_state.input_value_home_function = function_input
        
        # Get bounds from session state if available
        lower_bound = st.text_input("Lower Bound (a)", st.session_state.get("lower_bound", "0"), key="home_lower")
        upper_bound = st.text_input("Upper Bound (b)", st.session_state.get("upper_bound", "1"), key="home_upper")
        
        # Update session state
        st.session_state.lower_bound = lower_bound
        st.session_state.upper_bound = upper_bound
        
        if st.button("Calculate Integral", key="calculate_home_integral"):
            try:
                result, steps = solve_integral(function_input, lower_bound, upper_bound, "x")
                display_solution(function_input, lower_bound, upper_bound, result, steps)
                
                # Plot the function and its integral
                plot_integral(function_input, lower_bound, upper_bound, "x")
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    with col2:
        st.markdown("""
        ### How to use:
        
        1. Enter a function in terms of x
        2. Specify the lower and upper bounds
        3. Click "Calculate Integral"
        
        ### Example inputs:
        
        - Function: `x^2 + 3*x + 2`
        - Lower bound: `2`
        - Upper bound: `4`
        
        Try these examples from the course materials!
        """)

# Other pages are imported from the pages directory
elif app_mode == "Riemann Sums":
    import pages.riemann_sums
    pages.riemann_sums.show()
    
elif app_mode == "Definite Integrals":
    import pages.definite_integrals
    pages.definite_integrals.show()
    
elif app_mode == "Area Between Curves":
    import pages.area_between_curves
    pages.area_between_curves.show()
    
elif app_mode == "Engineering Applications":
    import pages.applications
    pages.applications.show()
    
elif app_mode == "Software Engineering Scenarios":
    import pages.software_engineering_scenarios
    pages.software_engineering_scenarios.show()

# Footer
st.markdown("---")
st.markdown("© 2024 CalcuMaster - Integral Calculus Solver")
