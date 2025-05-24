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

app_mode = st.sidebar.selectbox(
    "Choose Application Mode",
    ["Home", "Riemann Sums", "Definite Integrals", "Area Between Curves", "Engineering Applications"]
)

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
        function_input = create_math_input("Function f(x)", "x^2", key="home_function")
        lower_bound = st.text_input("Lower Bound (a)", "0", key="home_lower")
        upper_bound = st.text_input("Upper Bound (b)", "1", key="home_upper")
        
        if st.button("Calculate Integral"):
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

# Footer
st.markdown("---")
st.markdown("© 2024 CalcuMaster - Integral Calculus Solver")
