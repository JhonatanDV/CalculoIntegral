import streamlit as st
import sympy as sp

def display_solution(func_str, lower_bound, upper_bound, result, steps):
    """
    Display the solution to an integral calculation with step-by-step workings.
    
    Args:
        func_str (str): String representation of the function
        lower_bound (str): Lower bound of integration
        upper_bound (str): Upper bound of integration
        result: Result of the integration
        steps (list): List of solution steps
    
    Returns:
        None
    """
    st.markdown("## Solution")
    
    # Display the problem statement
    st.markdown(f"### Evaluating $\\int_{{{lower_bound}}}^{{{upper_bound}}} {func_str} \\, dx$")
    
    # Display the result
    st.markdown(f"### Result: {result}")
    
    # Display step-by-step solution
    st.markdown("### Step-by-Step Solution")
    
    with st.expander("Show Solution Steps", expanded=True):
        for step in steps:
            st.markdown(step)
    
    # Add a download button for the solution
    solution_text = f"""
# Integral Calculation: ∫_{lower_bound}^{upper_bound} {func_str} dx

## Result: {result}

## Step-by-Step Solution:
"""
    for step in steps:
        solution_text += f"\n{step}"
    
    st.download_button(
        label="Download Solution",
        data=solution_text,
        file_name="integral_solution.txt",
        mime="text/plain"
    )

def display_riemann_sum_solution(func_str, lower_bound, upper_bound, n, method, result, steps, diagram_provided=True):
    """
    Display the solution to a Riemann sum calculation with step-by-step workings.
    
    Args:
        func_str (str): String representation of the function
        lower_bound (float): Lower bound of the interval
        upper_bound (float): Upper bound of the interval
        n (int): Number of subdivisions
        method (str): Method for selecting sample points ('left', 'right', 'midpoint')
        result (float): Result of the Riemann sum calculation
        steps (list): List of solution steps
        diagram_provided (bool): Whether a diagram has been provided separately
    
    Returns:
        None
    """
    st.markdown("## Riemann Sum Solution")
    
    # Display the problem statement
    st.markdown(f"### Calculating the {method} Riemann sum for $f(x) = {func_str}$ on $[{lower_bound}, {upper_bound}]$ with $n = {n}$")
    
    # Display the result
    st.markdown(f"### Result: {result}")
    
    # Display step-by-step solution
    st.markdown("### Step-by-Step Solution")
    
    with st.expander("Show Solution Steps", expanded=True):
        for step in steps:
            st.markdown(step)
    
    # Explanation of what the Riemann sum represents
    st.markdown("### What does the Riemann sum represent?")
    
    explanation = f"""
    The Riemann sum approximates the area under the curve $f(x) = {func_str}$ from $x = {lower_bound}$ to $x = {upper_bound}$
    by dividing the interval into {n} equal subintervals and calculating the sum of the areas of {n} rectangles.
    
    In this calculation, we used the **{method} endpoint method**, which means:
    """
    
    if method == 'left':
        explanation += "- The height of each rectangle is determined by the function value at the **left endpoint** of each subinterval."
    elif method == 'right':
        explanation += "- The height of each rectangle is determined by the function value at the **right endpoint** of each subinterval."
    elif method == 'midpoint':
        explanation += "- The height of each rectangle is determined by the function value at the **midpoint** of each subinterval."
    
    explanation += f"""
    
    As the number of subintervals ($n$) increases, the Riemann sum approaches the exact value of the definite integral:
    
    $\\lim_{{n \\to \\infty}} \\sum_{{i=1}}^{{n}} f(x_i^*) \\Delta x = \\int_{{{lower_bound}}}^{{{upper_bound}}} f(x) \\, dx$
    """
    
    st.markdown(explanation)
    
    if not diagram_provided:
        st.markdown("### Diagram")
        st.markdown("A visual representation helps to understand what the Riemann sum calculates. "
                   "The diagram would show the function curve and the rectangles used in the approximation.")
    
    # Add a download button for the solution
    solution_text = f"""
# Riemann Sum Calculation for f(x) = {func_str} on [{lower_bound}, {upper_bound}] with n = {n}

## Method: {method} endpoint
## Result: {result}

## Step-by-Step Solution:
"""
    for step in steps:
        solution_text += f"\n{step.replace('$', '')}"
    
    solution_text += f"""
\n## What does the Riemann sum represent?
The Riemann sum approximates the area under the curve f(x) = {func_str} from x = {lower_bound} to x = {upper_bound}
by dividing the interval into {n} equal subintervals and calculating the sum of the areas of {n} rectangles.
"""
    
    st.download_button(
        label="Download Solution",
        data=solution_text,
        file_name="riemann_sum_solution.txt",
        mime="text/plain"
    )

def display_area_between_curves_solution(func1_str, func2_str, lower_bound, upper_bound, result, steps, diagram_provided=True):
    """
    Display the solution to an area between curves calculation with step-by-step workings.
    
    Args:
        func1_str (str): String representation of the first function
        func2_str (str): String representation of the second function
        lower_bound (float): Lower bound of the interval
        upper_bound (float): Upper bound of the interval
        result (float): Result of the area calculation
        steps (list): List of solution steps
        diagram_provided (bool): Whether a diagram has been provided separately
    
    Returns:
        None
    """
    st.markdown("## Area Between Curves Solution")
    
    # Display the problem statement
    st.markdown(f"### Calculating the area between $y = {func1_str}$ and $y = {func2_str}$ from $x = {lower_bound}$ to $x = {upper_bound}$")
    
    # Display the result
    st.markdown(f"### Result: {result}")
    
    # Display step-by-step solution
    st.markdown("### Step-by-Step Solution")
    
    with st.expander("Show Solution Steps", expanded=True):
        for step in steps:
            st.markdown(step)
    
    # Explanation of what the area represents
    st.markdown("### What does the area between curves represent?")
    
    explanation = f"""
    The area between curves calculates the region enclosed by two functions $y = {func1_str}$ and $y = {func2_str}$
    from $x = {lower_bound}$ to $x = {upper_bound}$.
    
    This area can be calculated using the definite integral:
    
    $\\text{{Area}} = \\int_{{{lower_bound}}}^{{{upper_bound}}} |f_1(x) - f_2(x)| \\, dx$
    
    In practice, we determine which function has greater values in the interval and subtract the lower function from the upper one:
    
    $\\text{{Area}} = \\int_{{{lower_bound}}}^{{{upper_bound}}} [\\text{{upper function}} - \\text{{lower function}}] \\, dx$
    """
    
    st.markdown(explanation)
    
    if not diagram_provided:
        st.markdown("### Diagram")
        st.markdown("A visual representation helps to understand what the area between curves represents. "
                   "The diagram would show both function curves and the enclosed area.")
    
    # Add a download button for the solution
    solution_text = f"""
# Area Between Curves Calculation for y = {func1_str} and y = {func2_str} on [{lower_bound}, {upper_bound}]

## Result: {result}

## Step-by-Step Solution:
"""
    for step in steps:
        solution_text += f"\n{step.replace('$', '')}"
    
    solution_text += f"""
\n## What does the area between curves represent?
The area between curves calculates the region enclosed by two functions y = {func1_str} and y = {func2_str}
from x = {lower_bound} to x = {upper_bound}.
"""
    
    st.download_button(
        label="Download Solution",
        data=solution_text,
        file_name="area_between_curves_solution.txt",
        mime="text/plain"
    )
