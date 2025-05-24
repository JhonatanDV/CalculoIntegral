import sympy as sp
import numpy as np
from sympy import symbols, sympify, integrate, diff, N, Rational

def parse_expression(expr_str, var_str="x"):
    """
    Parse a string expression into a SymPy expression.
    
    Args:
        expr_str (str): String representation of the mathematical expression
        var_str (str): The variable used in the expression
    
    Returns:
        sympy.Expr: SymPy expression
    """
    try:
        # Handle common input issues
        expr_str = expr_str.replace("^", "**")
        expr_str = expr_str.replace("e", "E")
        
        # Define the symbol
        var = symbols(var_str)
        
        # Parse the expression
        expr = sympify(expr_str)
        
        return expr
    except Exception as e:
        raise ValueError(f"Error parsing expression: {str(e)}")

def evaluate_expression(expr_str, var_str="x", var_value=None):
    """
    Evaluate a mathematical expression.
    
    Args:
        expr_str (str): String representation of the mathematical expression
        var_str (str): The variable used in the expression
        var_value: Value to substitute for the variable (optional)
    
    Returns:
        float or sympy.Expr: Evaluated expression or symbolic expression
    """
    try:
        expr = parse_expression(expr_str, var_str)
        var = symbols(var_str)
        
        if var_value is not None:
            # Substitute the variable value and evaluate
            result = expr.subs(var, var_value)
            return float(result)
        else:
            return expr
    except Exception as e:
        raise ValueError(f"Error evaluating expression: {str(e)}")

def solve_integral(func_str, lower_bound_str, upper_bound_str, var_str="x"):
    """
    Solve a definite integral and provide step-by-step solution.
    
    Args:
        func_str (str): String representation of the function to integrate
        lower_bound_str (str): Lower bound of integration
        upper_bound_str (str): Upper bound of integration
        var_str (str): The variable of integration
    
    Returns:
        tuple: (result, steps) where result is the value of the integral and steps is a list of solution steps
    """
    try:
        # Handle the case where the integral symbol is used
        if func_str.startswith("∫("):
            func_str = func_str[2:].strip()
            if func_str.endswith(")"):
                func_str = func_str[:-1].strip()
        
        # Parse inputs
        func = parse_expression(func_str, var_str)
        var = symbols(var_str)
        
        # Convert bounds to numerical values if possible
        try:
            lower_bound = float(lower_bound_str)
        except ValueError:
            lower_bound = parse_expression(lower_bound_str)
        
        try:
            upper_bound = float(upper_bound_str)
        except ValueError:
            upper_bound = parse_expression(upper_bound_str)
        
        # Steps for the solution
        steps = []
        
        # Step 1: Set up the integral
        steps.append(f"Step 1: Set up the definite integral:\n$\\int_{{{lower_bound}}}^{{{upper_bound}}} {sp.latex(func)} \\, d{var_str}$")
        
        # Step 2: Find the antiderivative
        antiderivative = integrate(func, var)
        steps.append(f"Step 2: Find the antiderivative:\n$\\int {sp.latex(func)} \\, d{var_str} = {sp.latex(antiderivative)} + C$")
        
        # Step 3: Evaluate at the bounds
        steps.append(f"Step 3: Apply the Fundamental Theorem of Calculus:\n$\\int_{{{lower_bound}}}^{{{upper_bound}}} {sp.latex(func)} \\, d{var_str} = [{sp.latex(antiderivative)}]_{{{lower_bound}}}^{{{upper_bound}}}$")
        
        # Step 4: Substitute the upper bound
        upper_result = antiderivative.subs(var, upper_bound)
        steps.append(f"Step 4: Substitute the upper bound:\n${sp.latex(antiderivative)}\|_{{{var_str}={upper_bound}}} = {sp.latex(upper_result)}$")
        
        # Step 5: Substitute the lower bound
        lower_result = antiderivative.subs(var, lower_bound)
        steps.append(f"Step 5: Substitute the lower bound:\n${sp.latex(antiderivative)}\|_{{{var_str}={lower_bound}}} = {sp.latex(lower_result)}$")
        
        # Step 6: Subtract to get the final result
        final_result = upper_result - lower_result
        steps.append(f"Step 6: Subtract to get the final result:\n${sp.latex(upper_result)} - ({sp.latex(lower_result)}) = {sp.latex(final_result)}$")
        
        # Convert to float if possible for display
        try:
            numeric_result = float(final_result)
            steps.append(f"Step 7: Simplify:\n$= {numeric_result}$")
            return numeric_result, steps
        except:
            return final_result, steps
    
    except Exception as e:
        raise ValueError(f"Error solving integral: {str(e)}")

def calculate_derivative(func_str, var_str="x", order=1):
    """
    Calculate the derivative of a function.
    
    Args:
        func_str (str): String representation of the function
        var_str (str): The variable with respect to which to differentiate
        order (int): Order of the derivative (default: 1)
    
    Returns:
        sympy.Expr: The derivative expression
    """
    try:
        func = parse_expression(func_str, var_str)
        var = symbols(var_str)
        
        derivative = diff(func, var, order)
        return derivative
    except Exception as e:
        raise ValueError(f"Error calculating derivative: {str(e)}")

def find_critical_points(func_str, var_str="x", domain=None):
    """
    Find critical points (where derivative is zero) of a function.
    
    Args:
        func_str (str): String representation of the function
        var_str (str): The variable name
        domain (tuple): Optional domain limits as (lower, upper)
    
    Returns:
        list: List of critical points
    """
    try:
        func = parse_expression(func_str, var_str)
        var = symbols(var_str)
        
        # Calculate the derivative
        derivative = diff(func, var)
        
        # Find where derivative equals zero
        critical_points = sp.solve(derivative, var)
        
        # Filter by domain if provided
        if domain:
            lower, upper = domain
            critical_points = [cp for cp in critical_points if lower <= float(cp) <= upper]
        
        return critical_points
    except Exception as e:
        raise ValueError(f"Error finding critical points: {str(e)}")
