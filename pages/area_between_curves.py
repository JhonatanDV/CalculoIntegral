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
        function1_input = create_math_input("First Function f₁(x)", "x^2", key="function1")
        function2_input = create_math_input("Second Function f₂(x)", "x", key="function2")
        
        col1a, col1b = st.columns(2)
        with col1a:
            lower_bound = st.text_input("Lower Bound (a)", "0", key="abc_lower")
        with col1b:
            upper_bound = st.text_input("Upper Bound (b)", "1", key="abc_upper")
        
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
            st.session_state.function1 = example["function1"]
            st.session_state.function2 = example["function2"]
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
