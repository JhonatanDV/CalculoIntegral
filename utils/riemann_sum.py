import numpy as np
import sympy as sp
from sympy import symbols, sympify, lambdify
from utils.calculator import parse_expression

def calculate_riemann_sum(func_str, lower_bound, upper_bound, n, method='left', var_str="x"):
    """
    Calculate the Riemann sum for a function.
    
    Args:
        func_str (str): String representation of the function
        lower_bound (float): Lower bound of the interval
        upper_bound (float): Upper bound of the interval
        n (int): Number of subdivisions
        method (str): Method for selecting sample points ('left', 'right', 'midpoint')
        var_str (str): Variable name
    
    Returns:
        tuple: (riemann_sum, step_details) where riemann_sum is the calculated sum and 
               step_details is a list of dictionaries with information about each subinterval
    """
    try:
        # Parse the function
        expr = parse_expression(func_str, var_str)
        var = symbols(var_str)
        
        # Create a numeric function using lambdify
        f = lambdify(var, expr, "numpy")
        
        # Calculate width of each subinterval
        delta_x = (upper_bound - lower_bound) / n
        
        # Initialize sum and step details
        riemann_sum = 0
        step_details = []
        
        for i in range(n):
            x_left = lower_bound + i * delta_x
            x_right = lower_bound + (i + 1) * delta_x
            
            if method == 'left':
                sample_point = x_left
            elif method == 'right':
                sample_point = x_right
            elif method == 'midpoint':
                sample_point = (x_left + x_right) / 2
            else:
                raise ValueError(f"Unknown method: {method}")
            
            # Calculate function value at sample point
            function_value = f(sample_point)
            
            # Calculate area of the rectangle
            rectangle_area = function_value * delta_x
            
            # Add to the sum
            riemann_sum += rectangle_area
            
            # Store details for this step
            step_details.append({
                'subinterval_index': i + 1,
                'x_left': x_left,
                'x_right': x_right,
                'sample_point': sample_point,
                'function_value': function_value,
                'rectangle_area': rectangle_area,
                'running_sum': riemann_sum
            })
        
        return riemann_sum, step_details
    
    except Exception as e:
        raise ValueError(f"Error calculating Riemann sum: {str(e)}")

def get_riemann_sum_steps(func_str, lower_bound, upper_bound, n, method='left', var_str="x"):
    """
    Generate formatted steps for Riemann sum calculation.
    
    Args:
        func_str (str): String representation of the function
        lower_bound (float): Lower bound of the interval
        upper_bound (float): Upper bound of the interval
        n (int): Number of subdivisions
        method (str): Method for selecting sample points ('left', 'right', 'midpoint')
        var_str (str): Variable name
    
    Returns:
        list: List of formatted solution steps
    """
    try:
        # Calculate Riemann sum and get step details
        riemann_sum, step_details = calculate_riemann_sum(
            func_str, lower_bound, upper_bound, n, method, var_str
        )
        
        # Format the steps
        steps = []
        
        # Step 1: Setup
        steps.append(f"Step 1: Set up the Riemann sum for f({var_str}) = {func_str}")
        
        # Step 2: Calculate delta_x
        delta_x = (upper_bound - lower_bound) / n
        steps.append(f"Step 2: Calculate the width of each subinterval (Δ{var_str})")
        steps.append(f"Δ{var_str} = (b - a) / n = ({upper_bound} - {lower_bound}) / {n} = {delta_x}")
        
        # Step 3: Determine the sample points
        steps.append(f"Step 3: Using the {method} endpoint method, calculate the sample points")
        
        # Step 4: Calculate the sum
        steps.append(f"Step 4: Calculate the Riemann sum")
        
        sum_formula = "R_n = "
        if method == 'left':
            sum_formula += f"Δ{var_str} × [f({var_str}_0) + f({var_str}_1) + ... + f({var_str}_{n-1})]"
        elif method == 'right':
            sum_formula += f"Δ{var_str} × [f({var_str}_1) + f({var_str}_2) + ... + f({var_str}_{n})]"
        elif method == 'midpoint':
            sum_formula += f"Δ{var_str} × [f(m_1) + f(m_2) + ... + f(m_{n})]"
            
        steps.append(sum_formula)
        
        # Step 5: Detailed calculations
        steps.append(f"Step 5: Calculate each term in the sum")
        
        for i, detail in enumerate(step_details):
            if method == 'left':
                steps.append(f"Rectangle {i+1}: {var_str} = {detail['sample_point']:.6f}, "
                           f"f({var_str}) = {detail['function_value']:.6f}, "
                           f"Area = {detail['function_value']:.6f} × {delta_x:.6f} = {detail['rectangle_area']:.6f}")
            elif method == 'right':
                steps.append(f"Rectangle {i+1}: {var_str} = {detail['sample_point']:.6f}, "
                           f"f({var_str}) = {detail['function_value']:.6f}, "
                           f"Area = {detail['function_value']:.6f} × {delta_x:.6f} = {detail['rectangle_area']:.6f}")
            elif method == 'midpoint':
                steps.append(f"Rectangle {i+1}: midpoint = {detail['sample_point']:.6f}, "
                           f"f(midpoint) = {detail['function_value']:.6f}, "
                           f"Area = {detail['function_value']:.6f} × {delta_x:.6f} = {detail['rectangle_area']:.6f}")
        
        # Step 6: Final result
        steps.append(f"Step 6: Sum all rectangle areas")
        
        sum_expression = " + ".join([f"{detail['rectangle_area']:.6f}" for detail in step_details])
        steps.append(f"Riemann Sum = {sum_expression} = {riemann_sum:.6f}")
        
        return steps
    
    except Exception as e:
        raise ValueError(f"Error generating Riemann sum steps: {str(e)}")
