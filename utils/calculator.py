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
        expr_str = expr_str.replace("^", "**")  # Reemplazar ^ por **
        
        # Manejar nombres especiales que pueden causar conflictos
        expr_str = expr_str.replace("Exp", "exp")  # Normalizar Exp a exp
        
        # Evitar problemas con el operador e (Euler)
        if "e" in expr_str and not any(s in expr_str for s in ["exp(", "sec(", "ceiling("]):
            expr_str = expr_str.replace("e", "E")
        
        # Manejo especial para expresiones con log(n)/n para evitar división por cero
        if "log" in expr_str and var_str in expr_str and f"log({var_str})/{var_str}" in expr_str.replace(" ", ""):
            expr_str = expr_str.replace(f"log({var_str})", f"log({var_str}+0.0001)")
            expr_str = expr_str.replace(f"/{var_str}", f"/({var_str}+0.0001)")
        
        # Define the symbol
        var = symbols(var_str)
        
        # Parse the expression
        expr = sympify(expr_str)
        
        return expr
    except Exception as e:
        raise ValueError(f"Error al analizar la expresión: {str(e)}")

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
            # Manejar valores problemáticos
            if var_value == 0 and ('log' in expr_str or f'1/{var_str}' in expr_str or f'/{var_str}' in expr_str):
                # Usar un valor muy pequeño en lugar de cero para evitar errores de división
                var_value = 0.0001
            
            # Substitute the variable value and evaluate
            result = expr.subs(var, var_value)
            
            # Intentar convertir a float
            try:
                return float(result)
            except (TypeError, ValueError):
                # Si no se puede convertir a float, devolver la expresión simbólica
                return result
        else:
            return expr
    except Exception as e:
        raise ValueError(f"Error al evaluar la expresión: {str(e)}")

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
        # Reemplazar el símbolo de integral por el texto "integrate"
        if "∫" in func_str:
            # Extraer solo la función dentro del símbolo de integral
            if func_str.startswith("∫(") and func_str.endswith(")"):
                func_str = func_str[2:-1].strip()
            else:
                func_str = func_str.replace("∫", "").strip()
                # Eliminar paréntesis si están presentes
                if func_str.startswith("(") and func_str.endswith(")"):
                    func_str = func_str[1:-1].strip()
        
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
        steps.append(f"Paso 1: Configurar la integral definida:\n$\\int_{{{lower_bound}}}^{{{upper_bound}}} {sp.latex(func)} \\, d{var_str}$")
        
        # Step 2: Find the antiderivative
        antiderivative = integrate(func, var)
        steps.append(f"Paso 2: Encontrar la antiderivada:\n$\\int {sp.latex(func)} \\, d{var_str} = {sp.latex(antiderivative)} + C$")
        
        # Step 3: Evaluate at the bounds
        steps.append(f"Paso 3: Aplicar el Teorema Fundamental del Cálculo:\n$\\int_{{{lower_bound}}}^{{{upper_bound}}} {sp.latex(func)} \\, d{var_str} = [{sp.latex(antiderivative)}]_{{{lower_bound}}}^{{{upper_bound}}}$")
        
        # Step 4: Substitute the upper bound
        upper_result = antiderivative.subs(var, upper_bound)
        steps.append(f"Paso 4: Sustituir el límite superior:\n${sp.latex(antiderivative)}\|_{{{var_str}={upper_bound}}} = {sp.latex(upper_result)}$")
        
        # Step 5: Substitute the lower bound
        lower_result = antiderivative.subs(var, lower_bound)
        steps.append(f"Paso 5: Sustituir el límite inferior:\n${sp.latex(antiderivative)}\|_{{{var_str}={lower_bound}}} = {sp.latex(lower_result)}$")
        
        # Step 6: Subtract to get the final result
        final_result = upper_result - lower_result
        steps.append(f"Paso 6: Restar para obtener el resultado final:\n${sp.latex(upper_result)} - ({sp.latex(lower_result)}) = {sp.latex(final_result)}$")
        
        # Convert to float if possible for display
        try:
            numeric_result = float(final_result)
            steps.append(f"Paso 7: Simplificar:\n$= {numeric_result}$")
            return numeric_result, steps
        except:
            return final_result, steps
    
    except Exception as e:
        raise ValueError(f"Error al resolver la integral: {str(e)}")

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
