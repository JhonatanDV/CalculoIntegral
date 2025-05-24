import sympy as sp
import numpy as np
from sympy import symbols, sympify, integrate, solve
from utils.calculator import parse_expression

def find_intersection_points(func1_str, func2_str, var_str="x", domain=None):
    """
    Find the intersection points of two functions.
    
    Args:
        func1_str (str): String representation of the first function
        func2_str (str): String representation of the second function
        var_str (str): Variable name
        domain (tuple): Optional domain limits as (lower, upper)
    
    Returns:
        list: List of x-coordinates of intersection points
    """
    try:
        # Parse the functions
        expr1 = parse_expression(func1_str, var_str)
        expr2 = parse_expression(func2_str, var_str)
        var = symbols(var_str)
        
        # Find where the functions are equal
        equation = sp.Eq(expr1, expr2)
        intersection_points = solve(equation, var)
        
        # Convert complex solutions to real if imaginary part is close to zero
        real_solutions = []
        for point in intersection_points:
            if isinstance(point, sp.Float) or point.is_real:
                real_solutions.append(float(point))
            elif hasattr(point, 'as_real_imag'):
                re, im = point.as_real_imag()
                if abs(float(im)) < 1e-10:  # Small imaginary part, treat as real
                    real_solutions.append(float(re))
        
        # Filter by domain if provided
        if domain:
            lower, upper = domain
            real_solutions = [p for p in real_solutions if lower <= p <= upper]
        
        # Sort the solutions
        real_solutions.sort()
        
        return real_solutions
    
    except Exception as e:
        raise ValueError(f"Error finding intersection points: {str(e)}")

def calculate_area_between_curves(func1_str, func2_str, lower_bound, upper_bound, var_str="x"):
    """
    Calculate the area between two curves.
    
    Args:
        func1_str (str): String representation of the first function
        func2_str (str): String representation of the second function
        lower_bound (float): Lower bound of the interval
        upper_bound (float): Upper bound of the interval
        var_str (str): Variable name
    
    Returns:
        tuple: (area, steps) where area is the calculated area and steps is a list of solution steps
    """
    try:
        # Parse the functions
        expr1 = parse_expression(func1_str, var_str)
        expr2 = parse_expression(func2_str, var_str)
        var = symbols(var_str)
        
        # Determine which function is on top (greater y-value)
        # We'll check at the midpoint of the interval
        midpoint = (lower_bound + upper_bound) / 2
        val1 = expr1.subs(var, midpoint)
        val2 = expr2.subs(var, midpoint)
        
        if val1 > val2:
            top_expr = expr1
            bottom_expr = expr2
            top_func_str = func1_str
            bottom_func_str = func2_str
        else:
            top_expr = expr2
            bottom_expr = expr1
            top_func_str = func2_str
            bottom_func_str = func1_str
        
        # Compute the integral of the difference
        diff_expr = top_expr - bottom_expr
        integral = integrate(diff_expr, (var, lower_bound, upper_bound))
        
        # Format the steps
        steps = []
        
        # Step 1: Identify the functions
        steps.append(f"Step 1: Identify the two functions")
        steps.append(f"f₁({var_str}) = {func1_str}")
        steps.append(f"f₂({var_str}) = {func2_str}")
        
        # Step 2: Determine which function is on top
        steps.append(f"Step 2: Determine which function has greater values in the interval [{lower_bound}, {upper_bound}]")
        steps.append(f"At {var_str} = {midpoint}:")
        steps.append(f"f₁({midpoint}) = {float(val1)}")
        steps.append(f"f₂({midpoint}) = {float(val2)}")
        
        if val1 > val2:
            steps.append(f"Since f₁({midpoint}) > f₂({midpoint}), f₁ is the top function.")
        else:
            steps.append(f"Since f₂({midpoint}) > f₁({midpoint}), f₂ is the top function.")
        
        # Step 3: Set up the integral
        steps.append(f"Step 3: Set up the integral for the area between curves")
        steps.append(f"Area = ∫_{{{lower_bound}}}^{{{upper_bound}}} [top_function - bottom_function] d{var_str}")
        steps.append(f"Area = ∫_{{{lower_bound}}}^{{{upper_bound}}} [{top_func_str} - ({bottom_func_str})] d{var_str}")
        
        # Step 4: Simplify the integrand
        steps.append(f"Step 4: Simplify the integrand")
        steps.append(f"Area = ∫_{{{lower_bound}}}^{{{upper_bound}}} [{sp.latex(diff_expr)}] d{var_str}")
        
        # Step 5: Compute the integral
        steps.append(f"Step 5: Compute the integral")
        steps.append(f"Area = [{sp.latex(integrate(diff_expr, var))}]_{{{lower_bound}}}^{{{upper_bound}}}")
        
        # Step 6: Evaluate at the bounds
        upper_result = integrate(diff_expr, var).subs(var, upper_bound)
        lower_result = integrate(diff_expr, var).subs(var, lower_bound)
        steps.append(f"Area = {sp.latex(upper_result)} - ({sp.latex(lower_result)})")
        
        # Step 7: Calculate the final result
        steps.append(f"Step 7: Calculate the final result")
        steps.append(f"Area = {sp.latex(integral)} = {float(integral)}")
        
        return float(integral), steps
    
    except Exception as e:
        raise ValueError(f"Error calculating area between curves: {str(e)}")
