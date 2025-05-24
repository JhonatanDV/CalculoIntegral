import streamlit as st
import sympy as sp
import numpy as np
from utils.riemann_sum import calculate_riemann_sum, get_riemann_sum_steps
from utils.plotting import plot_riemann_sum
from components.math_input import create_math_input
from components.solution_display import display_riemann_sum_solution
from assets.examples import riemann_sum_examples

def show():
    st.title("📊 Riemann Sums Calculator")
    
    # Initialize page-specific session state
    if "input_value_riemann_function" not in st.session_state:
        st.session_state["input_value_riemann_function"] = st.session_state.function_str
    
    st.markdown("""
    Riemann sums are used to approximate the definite integral (area under a curve) by dividing the area into rectangles.
    
    This calculator allows you to:
    - Calculate Riemann sums using left, right, or midpoint methods
    - Visualize the rectangles used in the approximation
    - See step-by-step solutions
    """)
    
    # Main input section
    st.header("Function and Interval")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Input Method Selection
        input_method = st.radio("Input Method", ["Keyboard", "Upload Image"], horizontal=True, key="riemann_input_method")
        
        if input_method == "Keyboard":
            function_input = create_math_input("Function f(x)", st.session_state.function_str, key="riemann_function")
        else:
            uploaded_file = st.file_uploader("Upload an image of a mathematical equation", type=["jpg", "jpeg", "png"], key="riemann_file_uploader")
            if uploaded_file is not None:
                st.image(uploaded_file, caption="Uploaded Math Expression", width=300)
                st.info("La funcionalidad de procesamiento de imágenes matemáticas estará disponible próximamente.")
                function_input = st.session_state.get("input_value_riemann_function", st.session_state.function_str)
            else:
                function_input = st.session_state.function_str
                
        # Save the function input to session state
        st.session_state.function_str = function_input
        
        col1a, col1b = st.columns(2)
        with col1a:
            lower_bound = st.text_input("Lower Bound (a)", st.session_state.lower_bound, key="riemann_lower")
            st.session_state.lower_bound = lower_bound
        with col1b:
            upper_bound = st.text_input("Upper Bound (b)", st.session_state.upper_bound, key="riemann_upper")
            st.session_state.upper_bound = upper_bound
        
        n_subdivisions = st.number_input("Number of Subdivisions (n)", min_value=1, max_value=100, value=st.session_state.n_subdivisions, key="riemann_n")
        st.session_state.n_subdivisions = n_subdivisions
        
        method = st.selectbox(
            "Sampling Method",
            ["left", "right", "midpoint"],
            index=0,
            key="riemann_method"
        )
    
    with col2:
        st.markdown("### Example Problems")
        selected_example = st.selectbox(
            "Select an example from the course materials:",
            list(riemann_sum_examples.keys()),
            key="riemann_example"
        )
        
        if st.button("Load Example", key="load_riemann_example"):
            example = riemann_sum_examples[selected_example]
            # Update the input value first
            st.session_state["input_value_riemann_function"] = example["function"]
            # Then update the other session variables
            st.session_state.function_str = example["function"]
            st.session_state.lower_bound = str(example["lower_bound"])
            st.session_state.upper_bound = str(example["upper_bound"])
            st.session_state.n_subdivisions = example["subdivisions"]
            if "method" in example:
                st.session_state.riemann_method = example["method"]
            st.rerun()
    
    # Calculate button
    if st.button("Calculate Riemann Sum", key="calculate_riemann"):
        try:
            # Parse inputs
            func_str = function_input
            a = float(lower_bound)
            b = float(upper_bound)
            n = int(n_subdivisions)
            
            # Calculate Riemann sum
            riemann_sum, _ = calculate_riemann_sum(func_str, a, b, n, method, "x")
            
            # Get step-by-step solution
            steps = get_riemann_sum_steps(func_str, a, b, n, method, "x")
            
            # Display the plot
            plot_riemann_sum(func_str, a, b, n, method, "x")
            
            # Display the solution
            display_riemann_sum_solution(func_str, a, b, n, method, riemann_sum, steps, diagram_provided=True)
            
        except Exception as e:
            st.error(f"Error calculating Riemann sum: {str(e)}")
    
    # Theory section
    with st.expander("Learn about Riemann Sums"):
        st.markdown("""
        ### What is a Riemann Sum?
        
        A Riemann sum is a method for approximating the definite integral (or area under a curve) by dividing it into simpler shapes (rectangles) whose areas are easy to calculate.
        
        ### Types of Riemann Sums
        
        1. **Left Riemann Sum**: Uses the function value at the left endpoint of each subinterval.
        2. **Right Riemann Sum**: Uses the function value at the right endpoint of each subinterval.
        3. **Midpoint Riemann Sum**: Uses the function value at the midpoint of each subinterval.
        
        ### The Formula
        
        For a function $f(x)$ on an interval $[a, b]$ divided into $n$ equal subintervals, the Riemann sum is:
        
        $R_n = \Delta x \sum_{i=1}^{n} f(x_i^*)$
        
        where:
        - $\Delta x = \frac{b-a}{n}$ is the width of each subinterval
        - $x_i^*$ is the sample point in the $i$-th subinterval
        
        ### Connection to Definite Integrals
        
        As the number of subintervals increases, the Riemann sum approaches the definite integral:
        
        $\lim_{n \to \infty} \sum_{i=1}^{n} f(x_i^*) \Delta x = \int_{a}^{b} f(x) \, dx$
        
        This is the fundamental connection between Riemann sums and definite integrals.
        """)
