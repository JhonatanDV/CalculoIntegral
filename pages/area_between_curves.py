import streamlit as st
import sympy as sp
import numpy as np
from utils.area_calculator import calculate_area_between_curves, find_intersection_points
from utils.plotting import plot_area_between_curves
from components.math_input import create_math_input
from components.solution_display import display_area_between_curves_solution
from assets.examples import area_between_curves_examples

def show():
    st.title("📏 Area Between Curves Calculator")
    
    # Initialize page-specific session state for functions
    if "input_value_function1" not in st.session_state:
        st.session_state["input_value_function1"] = "x^2"
    if "input_value_function2" not in st.session_state:
        st.session_state["input_value_function2"] = "x"
    if "abc_lower" not in st.session_state:
        st.session_state.abc_lower = "0"
    if "abc_upper" not in st.session_state:
        st.session_state.abc_upper = "1"
    
    st.markdown("""
    This calculator finds the area enclosed between two curves over a specified interval.
    
    You can:
    - Calculate the area between any two functions
    - Visualize the enclosed region
    - See step-by-step solutions
    - Find intersection points automatically
    """)
    
    # Main input section
    st.header("Functions and Interval")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Input Method Selection
        input_method = st.radio("Input Method", ["Keyboard", "Upload Image"], horizontal=True, key="abc_input_method")
        
        if input_method == "Keyboard":
            function1_input = create_math_input("First Function f₁(x)", st.session_state.get("input_value_function1", "x^2"), key="function1")
            function2_input = create_math_input("Second Function f₂(x)", st.session_state.get("input_value_function2", "x"), key="function2")
        else:
            st.markdown("#### First Function")
            uploaded_file1 = st.file_uploader("Upload an image for first function", type=["jpg", "jpeg", "png"], key="abc_file_uploader1")
            if uploaded_file1 is not None:
                st.image(uploaded_file1, caption="Uploaded First Function", width=300)
                st.info("La funcionalidad de procesamiento de imágenes matemáticas estará disponible próximamente.")
            function1_input = st.session_state.get("input_value_function1", "x^2")
            
            st.markdown("#### Second Function")
            uploaded_file2 = st.file_uploader("Upload an image for second function", type=["jpg", "jpeg", "png"], key="abc_file_uploader2")
            if uploaded_file2 is not None:
                st.image(uploaded_file2, caption="Uploaded Second Function", width=300)
                st.info("La funcionalidad de procesamiento de imágenes matemáticas estará disponible próximamente.")
            function2_input = st.session_state.get("input_value_function2", "x")
        
        # Save functions to session state
        st.session_state["input_value_function1"] = function1_input
        st.session_state["input_value_function2"] = function2_input
        
        col1a, col1b = st.columns(2)
        with col1a:
            lower_bound = st.text_input("Lower Bound (a)", st.session_state.abc_lower, key="abc_lower_input")
            st.session_state.abc_lower = lower_bound
        with col1b:
            upper_bound = st.text_input("Upper Bound (b)", st.session_state.abc_upper, key="abc_upper_input")
            st.session_state.abc_upper = upper_bound
        
        find_intersections = st.checkbox("Find intersection points automatically", value=True)
    
    with col2:
        st.markdown("### Example Problems")
        selected_example = st.selectbox(
            "Select an example from the course materials:",
            list(area_between_curves_examples.keys()),
            key="abc_example"
        )
        
        if st.button("Load Example", key="load_abc_example"):
            example = area_between_curves_examples[selected_example]
            st.session_state["input_value_function1"] = example["function1"]
            st.session_state["input_value_function2"] = example["function2"]
            st.session_state.abc_lower = str(example["lower_bound"])
            st.session_state.abc_upper = str(example["upper_bound"])
            st.rerun()
    
    # Find intersections if requested
    if find_intersections and st.button("Find Intersection Points", key="find_intersections"):
        try:
            intersections = find_intersection_points(function1_input, function2_input, "x")
            
            if intersections:
                st.success(f"Found {len(intersections)} intersection point(s)")
                
                intersection_text = ", ".join([f"x = {x:.6f}" for x in intersections])
                st.markdown(f"Intersection points: {intersection_text}")
                
                # Suggest bounds
                if len(intersections) >= 2:
                    st.markdown("Suggested bounds for area calculation:")
                    for i in range(len(intersections) - 1):
                        st.markdown(f"From x = {intersections[i]:.6f} to x = {intersections[i+1]:.6f}")
            else:
                st.warning("No intersection points found in the domain")
        
        except Exception as e:
            st.error(f"Error finding intersections: {str(e)}")
    
    # Calculate button
    if st.button("Calculate Area", key="calculate_area"):
        try:
            # Parse inputs
            func1_str = function1_input
            func2_str = function2_input
            a = float(lower_bound)
            b = float(upper_bound)
            
            # Calculate area
            area, steps = calculate_area_between_curves(func1_str, func2_str, a, b, "x")
            
            # Display the plot
            plot_area_between_curves(func1_str, func2_str, a, b, "x")
            
            # Display the solution
            display_area_between_curves_solution(func1_str, func2_str, a, b, area, steps)
            
        except Exception as e:
            st.error(f"Error calculating area: {str(e)}")
    
    # Theory section
    with st.expander("Learn about Area Between Curves"):
        st.markdown("""
        ### Area Between Curves Calculation
        
        To find the area between two curves $y = f(x)$ and $y = g(x)$ from $x = a$ to $x = b$, we use the formula:
        
        $\text{Area} = \int_{a}^{b} |f(x) - g(x)| \, dx$
        
        In practice, we need to determine which function has greater values in the given interval. If $f(x) \geq g(x)$ for all $x$ in $[a, b]$, then:
        
        $\text{Area} = \int_{a}^{b} [f(x) - g(x)] \, dx$
        
        ### When Curves Intersect
        
        If the curves intersect within the interval $[a, b]$, we need to:
        
        1. Find the intersection points
        2. Split the integral at these points
        3. Ensure we're always subtracting the lower curve from the upper curve
        
        ### Important Considerations
        
        - The area between curves is always positive
        - When finding the area with respect to the y-axis, use $\int_{c}^{d} |f^{-1}(y) - g^{-1}(y)| \, dy$
        - For complex regions, break the problem into simpler parts
        """)
