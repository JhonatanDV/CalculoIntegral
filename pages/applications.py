import streamlit as st
import sympy as sp
import numpy as np
from utils.calculator import evaluate_expression, solve_integral
from utils.plotting import plot_function, plot_integral, plot_area_between_curves
from components.math_input import create_math_input
from components.solution_display import display_solution, display_area_between_curves_solution
from assets.examples import engineering_applications_examples

def show():
    st.title("🔧 Engineering Applications of Integrals")
    
    st.markdown("""
    This section demonstrates how integral calculus is applied to solve engineering problems,
    particularly in software engineering contexts.
    
    Examples include:
    - Server resource consumption over time
    - User interaction patterns
    - Optimization in database queries
    - Algorithm complexity analysis
    """)
    
    # Application selection
    application_type = st.selectbox(
        "Select Application Type",
        ["Server Resource Consumption", "User Load Analysis", "Database Optimization", "Algorithm Complexity"],
        key="application_type"
    )
    
    # Load examples based on application type
    if application_type in engineering_applications_examples:
        examples = engineering_applications_examples[application_type]
    else:
        examples = {}
    
    # Example selection
    selected_example = st.selectbox(
        "Select an example problem:",
        list(examples.keys()) if examples else ["No examples available"],
        key="selected_application_example"
    )
    
    if st.button("Load Example", key="load_application_example") and examples:
        example = examples[selected_example]
        st.session_state.application_description = example.get("description", "")
        st.session_state.application_function1 = example.get("function1", "")
        st.session_state.application_function2 = example.get("function2", "")
        st.session_state.application_lower_bound = str(example.get("lower_bound", "0"))
        st.session_state.application_upper_bound = str(example.get("upper_bound", "1"))
        st.session_state.application_calculation_type = example.get("calculation_type", "definite_integral")
        st.rerun()
    
    # Problem description
    st.header("Problem Description")
    problem_description = st.text_area(
        "Problem Description",
        value=st.session_state.get("application_description", ""),
        height=100,
        key="application_description"
    )
    
    # Calculation type
    calculation_type = st.selectbox(
        "Calculation Type",
        ["Definite Integral", "Area Between Curves"],
        index=0 if st.session_state.get("application_calculation_type", "") == "definite_integral" else 1,
        key="application_calculation_type"
    )
    
    # Main input section
    st.header("Mathematical Model")
    
    col1, col2 = st.columns(2)
    
    with col1:
        function1_input = create_math_input(
            "First Function f₁(t)" if calculation_type == "Area Between Curves" else "Function f(t)",
            st.session_state.get("application_function1", "t^2 + 2*t + 1"),
            key="application_function1"
        )
        
        if calculation_type == "Area Between Curves":
            function2_input = create_math_input(
                "Second Function f₂(t)",
                st.session_state.get("application_function2", "2*t + 5"),
                key="application_function2"
            )
        
        col1a, col1b = st.columns(2)
        with col1a:
            lower_bound = st.text_input(
                "Lower Bound (a)",
                st.session_state.get("application_lower_bound", "0"),
                key="application_lower_bound"
            )
        with col1b:
            upper_bound = st.text_input(
                "Upper Bound (b)",
                st.session_state.get("application_upper_bound", "5"),
                key="application_upper_bound"
            )
    
    with col2:
        st.markdown("### Model Visualization")
        
        try:
            if calculation_type == "Definite Integral":
                fig = plot_function(function1_input, x_range=(float(lower_bound)-1, float(upper_bound)+1), var_str="t")
                st.plotly_chart(fig, use_container_width=True)
            else:
                fig = plot_function(function1_input, x_range=(float(lower_bound)-1, float(upper_bound)+1), var_str="t", color='blue')
                fig.add_trace(plot_function(function2_input, x_range=(float(lower_bound)-1, float(upper_bound)+1), var_str="t", color='green').data[0])
                st.plotly_chart(fig, use_container_width=True)
        except:
            st.info("Enter valid functions and bounds to see visualization")
    
    # Calculate button
    if st.button("Solve Problem", key="calculate_application"):
        try:
            # Parse inputs
            a = float(lower_bound)
            b = float(upper_bound)
            
            if calculation_type == "Definite Integral":
                # Calculate integral
                result, steps = solve_integral(function1_input, lower_bound, upper_bound, "t")
                
                # Display the plot
                plot_integral(function1_input, lower_bound, upper_bound, "t")
                
                # Display the solution
                display_solution(function1_input, lower_bound, upper_bound, result, steps)
                
                # Interpretation
                st.header("Engineering Interpretation")
                st.markdown(f"""
                The calculated value of {result:.6f} represents the total accumulated quantity over the interval [{lower_bound}, {upper_bound}].
                
                In the context of the problem:
                """)
                
                if "server" in problem_description.lower() and "resource" in problem_description.lower():
                    st.markdown(f"- This represents the **total resource consumption** of the server over the given time period.")
                elif "user" in problem_description.lower() and "load" in problem_description.lower():
                    st.markdown(f"- This represents the **total user load** on the system over the given time period.")
                elif "algorithm" in problem_description.lower() and "complex" in problem_description.lower():
                    st.markdown(f"- This represents the **cumulative processing time** of the algorithm across all inputs in the range.")
                else:
                    st.markdown(f"- This value represents the total accumulated quantity described in the problem.")
                
            else:  # Area Between Curves
                # Calculate area
                area, steps = calculate_area_between_curves(function1_input, function2_input, a, b, "t")
                
                # Display the plot
                plot_area_between_curves(function1_input, function2_input, a, b, "t")
                
                # Display the solution
                display_area_between_curves_solution(function1_input, function2_input, a, b, area, steps)
                
                # Interpretation
                st.header("Engineering Interpretation")
                st.markdown(f"""
                The calculated area of {area:.6f} represents the total difference between the two functions over the interval [{lower_bound}, {upper_bound}].
                
                In the context of the problem:
                """)
                
                if "database" in problem_description.lower() and "optim" in problem_description.lower():
                    st.markdown(f"- This represents the **optimization potential** in the database operations.")
                elif "server" in problem_description.lower() and ("memory" in problem_description.lower() or "cpu" in problem_description.lower()):
                    st.markdown(f"- This represents the **difference between resource types** consumed by the server.")
                else:
                    st.markdown(f"- This value represents the total difference between the two quantities described in the problem.")
            
        except Exception as e:
            st.error(f"Error solving problem: {str(e)}")
    
    # Theory section
    with st.expander("Applications of Integrals in Software Engineering"):
        st.markdown("""
        ### Integral Calculus in Software Engineering
        
        Integral calculus has several important applications in software engineering:
        
        #### 1. Performance Analysis
        
        - **Resource Consumption**: Calculating total memory, CPU, or bandwidth usage over time
        - **Throughput Measurement**: Analyzing the total number of transactions processed over a period
        
        #### 2. Load Testing and Capacity Planning
        
        - **User Load Modeling**: Predicting peak loads and resource requirements
        - **Server Scaling**: Determining when to scale resources based on integrated load metrics
        
        #### 3. Algorithm Analysis
        
        - **Time Complexity**: Analyzing the average or expected performance of algorithms
        - **Space-Time Tradeoffs**: Optimizing algorithms based on integrated performance metrics
        
        #### 4. Data Analysis and Machine Learning
        
        - **Probability Distributions**: Working with continuous probability distributions
        - **Error Minimization**: Minimizing error functions in machine learning models
        
        #### 5. Graphics and Simulation
        
        - **Physics Engines**: Calculating trajectories, velocities, and other physical properties
        - **Computer Graphics**: Path tracing, illumination models, and rendering equations
        
        By understanding and applying integral calculus, software engineers can build more efficient, 
        scalable, and mathematically sound systems.
        """)
