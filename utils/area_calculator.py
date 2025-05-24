import sympy as sp
import numpy as np
from sympy import symbols, sympify, integrate, solve
from scipy import integrate as sp_integrate
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
        
        # Determinar qué función está arriba de manera más robusta
        # Verificar en múltiples puntos en lugar de solo el punto medio
        try:
            # Convertir límites a float si son strings
            if isinstance(lower_bound, str):
                lower_bound = float(lower_bound)
            if isinstance(upper_bound, str):
                upper_bound = float(upper_bound)
                
            # Crear una secuencia de puntos para muestreo
            sample_points = np.linspace(lower_bound, upper_bound, 5)
            
            # Evaluar ambas funciones en los puntos de muestra
            values1 = []
            values2 = []
            
            for point in sample_points:
                try:
                    val1 = float(expr1.subs(var, point))
                    val2 = float(expr2.subs(var, point))
                    values1.append(val1)
                    values2.append(val2)
                except:
                    # Si hay error en algún punto, continuar con el siguiente
                    continue
            
            # Contar cuántas veces cada función está arriba
            func1_on_top_count = sum(1 for v1, v2 in zip(values1, values2) if v1 > v2)
            func2_on_top_count = sum(1 for v1, v2 in zip(values1, values2) if v2 > v1)
            
            # Determinar cuál función está arriba la mayoría del tiempo
            if func1_on_top_count >= func2_on_top_count:
                top_expr = expr1
                bottom_expr = expr2
                top_func_str = func1_str
                bottom_func_str = func2_str
                top_idx = 1
                bottom_idx = 2
            else:
                top_expr = expr2
                bottom_expr = expr1
                top_func_str = func2_str
                bottom_func_str = func1_str
                top_idx = 2
                bottom_idx = 1
                
        except Exception as e:
            # En caso de error, usar el punto medio como fallback
            midpoint = (lower_bound + upper_bound) / 2
            
            # Intentar evaluar en el punto medio
            try:
                val1 = float(expr1.subs(var, midpoint))
                val2 = float(expr2.subs(var, midpoint))
                
                if val1 > val2:
                    top_expr = expr1
                    bottom_expr = expr2
                    top_func_str = func1_str
                    bottom_func_str = func2_str
                    top_idx = 1
                    bottom_idx = 2
                else:
                    top_expr = expr2
                    bottom_expr = expr1
                    top_func_str = func2_str
                    bottom_func_str = func1_str
                    top_idx = 2
                    bottom_idx = 1
            except:
                # Si todo falla, asumir que la primera función está arriba
                top_expr = expr1
                bottom_expr = expr2
                top_func_str = func1_str
                bottom_func_str = func2_str
                top_idx = 1
                bottom_idx = 2
        
        # Calcular la diferencia de expresiones
        diff_expr = top_expr - bottom_expr
        
        # Intentar calcular la integral simbólicamente
        try:
            # Usar la integración simbólica
            integral = integrate(diff_expr, (var, lower_bound, upper_bound))
            float_result = float(integral)
        except Exception as int_e:
            # Si falla la integración simbólica, intentar con integración numérica
            try:
                # Convertir límites a float para integración numérica
                lb = float(lower_bound)
                ub = float(upper_bound)
                
                # Definir una función lambda para evaluación numérica
                import numpy as np
                from scipy import integrate as sp_integrate
                
                # Crear funciones numéricas a partir de expresiones simbólicas
                func_top = sp.lambdify(var, top_expr, modules=["numpy"])
                func_bottom = sp.lambdify(var, bottom_expr, modules=["numpy"])
                
                # Función diferencia para integración
                def diff_func(x):
                    try:
                        return func_top(x) - func_bottom(x)
                    except:
                        return 0
                
                # Calcular la integral numéricamente
                float_result, _ = sp_integrate.quad(diff_func, lb, ub)
                integral = float_result
            except Exception as num_e:
                # Si también falla la integración numérica, usar aproximación rectangular simple
                n_steps = 1000
                x_vals = np.linspace(lower_bound, upper_bound, n_steps)
                dx = (upper_bound - lower_bound) / n_steps
                
                # Calcular la suma de Riemann
                area_sum = 0
                for x in x_vals:
                    try:
                        top_val = float(top_expr.subs(var, x))
                        bottom_val = float(bottom_expr.subs(var, x))
                        area_sum += (top_val - bottom_val) * dx
                    except:
                        continue
                
                float_result = area_sum
                integral = float_result
        
        # Format the steps (ahora en español)
        steps = []
        
        # Paso 1: Identificar las funciones
        steps.append(f"Paso 1: Identificar las dos funciones")
        steps.append(f"f₁({var_str}) = {func1_str}")
        steps.append(f"f₂({var_str}) = {func2_str}")
        
        # Paso 2: Determinar qué función está arriba
        steps.append(f"Paso 2: Determinar qué función tiene valores mayores en el intervalo [{lower_bound}, {upper_bound}]")
        steps.append(f"Según el análisis del intervalo, f{top_idx} está por encima de f{bottom_idx} en la mayoría de los puntos.")
        
        # Paso 3: Configurar la integral
        steps.append(f"Paso 3: Configurar la integral para el área entre curvas")
        steps.append(f"Área = ∫_{{{lower_bound}}}^{{{upper_bound}}} [función_superior - función_inferior] d{var_str}")
        steps.append(f"Área = ∫_{{{lower_bound}}}^{{{upper_bound}}} [{top_func_str} - ({bottom_func_str})] d{var_str}")
        
        # Paso 4: Simplificar el integrando
        steps.append(f"Paso 4: Simplificar el integrando")
        steps.append(f"Área = ∫_{{{lower_bound}}}^{{{upper_bound}}} [{sp.latex(diff_expr)}] d{var_str}")
        
        # Paso 5: Calcular la integral
        steps.append(f"Paso 5: Calcular la integral")
        
        # Intentar mostrar los pasos de cálculo si es posible
        try:
            antiderivative = integrate(diff_expr, var)
            steps.append(f"Área = [{sp.latex(antiderivative)}]_{{{lower_bound}}}^{{{upper_bound}}}")
            
            # Paso 6: Evaluar en los límites
            upper_result = antiderivative.subs(var, upper_bound)
            lower_result = antiderivative.subs(var, lower_bound)
            steps.append(f"Área = {sp.latex(upper_result)} - ({sp.latex(lower_result)})")
        except:
            # Si no se puede mostrar el proceso paso a paso
            steps.append(f"Área = ∫_{{{lower_bound}}}^{{{upper_bound}}} [{sp.latex(diff_expr)}] d{var_str}")
        
        # Paso 7: Calcular el resultado final
        steps.append(f"Paso 7: Calcular el resultado final")
        steps.append(f"Área = {float_result:.6f} unidades cuadradas")
        
        return float_result, steps
    
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        raise ValueError(f"Error al calcular el área entre curvas: {str(e)}\nDetalles: {error_details}")
