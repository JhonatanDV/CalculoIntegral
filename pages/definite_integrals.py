import streamlit as st
import sympy as sp
import numpy as np
from utils.calculator import evaluate_expression, solve_integral
from utils.plotting import plot_integral
from components.math_input import create_math_input
from components.solution_display import display_solution
from assets.examples import definite_integral_examples

def show():
    st.title("📐 Definite Integrals Calculator")
    
    st.markdown("""
    Definite integrals calculate the accumulated value of a function over an interval, often representing area under a curve.
    
    This calculator allows you to:
    - Evaluate definite integrals and see step-by-step solutions
    - Visualize the area under the curve
    - Explore different types of functions and intervals
    """)
    
    # Main input section
    st.header("Function and Interval")
    
    col1, col2 = st.columns(2)
    
    with col1:
        function_input = create_math_input("Function f(x)", st.session_state.function_str, key="integral_function")
        st.session_state.function_str = function_input
        
        col1a, col1b = st.columns(2)
        with col1a:
            lower_bound = st.text_input("Lower Bound (a)", st.session_state.lower_bound, key="integral_lower")
            st.session_state.lower_bound = lower_bound
        with col1b:
            upper_bound = st.text_input("Upper Bound (b)", st.session_state.upper_bound, key="integral_upper")
            st.session_state.upper_bound = upper_bound
        
        variable = st.text_input("Variable", st.session_state.variable, key="integral_variable")
        st.session_state.variable = variable
    
    with col2:
        st.markdown("### Example Problems")
        selected_example = st.selectbox(
            "Select an example from the course materials:",
            list(definite_integral_examples.keys()),
            key="integral_example"
        )
        
        if st.button("Load Example", key="load_integral_example"):
            example = definite_integral_examples[selected_example]
            st.session_state.function_str = example["function"]
            st.session_state.lower_bound = str(example["lower_bound"])
            st.session_state.upper_bound = str(example["upper_bound"])
            st.session_state.variable = example["variable"]
            st.rerun()
    
    # Calculate button
    if st.button("Calculate Integral", key="calculate_integral"):
        try:
            # Parse inputs
            func_str = function_input
            a = lower_bound
            b = upper_bound
            var = variable if variable else "x"
            
            # Calculate integral
            result, steps = solve_integral(func_str, a, b, var)
            
            # Display the plot
            plot_integral(func_str, a, b, var)
            
            # Display the solution
            display_solution(func_str, a, b, result, steps)
            
        except Exception as e:
            st.error(f"Error calculating integral: {str(e)}")
    
    # Theory section
    with st.expander("Learn about Definite Integrals"):
        st.markdown("""
        ### What is a Definite Integral?
        
        A definite integral calculates the signed area between a function and the x-axis over a specified interval.
        
        The definite integral of a function $f(x)$ from $a$ to $b$ is written as:
        
        $\int_{a}^{b} f(x) \, dx$
        
        ### The Fundamental Theorem of Calculus
        
        The definite integral can be calculated using antiderivatives:
        
        $\int_{a}^{b} f(x) \, dx = F(b) - F(a)$
        
        where $F(x)$ is an antiderivative of $f(x)$, meaning $F'(x) = f(x)$.
        
        ### Properties of Definite Integrals
        
        1. $\int_{a}^{b} [f(x) \pm g(x)] \, dx = \int_{a}^{b} f(x) \, dx \pm \int_{a}^{b} g(x) \, dx$
        
        2. $\int_{a}^{b} c \cdot f(x) \, dx = c \cdot \int_{a}^{b} f(x) \, dx$ (where $c$ is a constant)
        
        3. $\int_{a}^{b} f(x) \, dx = -\int_{b}^{a} f(x) \, dx$
        
        4. $\int_{a}^{b} f(x) \, dx = \int_{a}^{c} f(x) \, dx + \int_{c}^{b} f(x) \, dx$ (for any $c$ between $a$ and $b$)
        
        ### Applications
        
        Definite integrals have numerous applications, including:
        - Area under a curve
        - Volume of solids
        - Length of curves
        - Work done by a force
        - Probability distributions
        - Center of mass
        """)
