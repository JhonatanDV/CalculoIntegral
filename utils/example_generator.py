import random
import sympy as sp
import numpy as np
from sympy import symbols, sympify, integrate, sin, cos, exp, log, sqrt, Rational, pi, E, Float

def generate_random_function(complexity="medium", var_str="x"):
    """
    Genera una función matemática aleatoria.
    
    Args:
        complexity (str): Nivel de complejidad ("simple", "medium", "complex")
        var_str (str): Variable a utilizar
    
    Returns:
        tuple: (func_str, latex_form, description) - Cadena de función, formato LaTeX, descripción
    """
    var = symbols(var_str)
    
    # Funciones simples
    simple_functions = [
        (f"{var_str}^2", var**2, "función cuadrática"),
        (f"{var_str}^3", var**3, "función cúbica"),
        (f"2*{var_str} + 1", 2*var + 1, "función lineal"),
        (f"sin({var_str})", sin(var), "función seno"),
        (f"cos({var_str})", cos(var), "función coseno"),
        (f"exp({var_str})", exp(var), "función exponencial"),
        (f"log({var_str})", log(var), "función logarítmica"),
        (f"sqrt({var_str})", sqrt(var), "función raíz cuadrada"),
    ]
    
    # Funciones de complejidad media
    medium_functions = [
        (f"{var_str}^3 - 2*{var_str}^2 + 3*{var_str}", var**3 - 2*var**2 + 3*var, "polinomio de grado 3"),
        (f"sin({var_str})^2", sin(var)**2, "función seno al cuadrado"),
        (f"cos(2*{var_str})", cos(2*var), "función coseno con frecuencia 2"),
        (f"exp(-{var_str}^2)", exp(-var**2), "función gaussiana"),
        (f"{var_str}*log({var_str})", var*log(var), "función x·log(x)"),
        (f"1/({var_str}^2 + 1)", 1/(var**2 + 1), "función racional"),
        (f"sqrt(1-{var_str}^2)", sqrt(1-var**2), "semicicunferencia"),
        (f"sin({var_str})*cos({var_str})", sin(var)*cos(var), "producto de funciones trigonométricas"),
    ]
    
    # Funciones complejas
    complex_functions = [
        (f"{var_str}^4 - 3*{var_str}^3 + 2*{var_str}^2 - {var_str} + 1", var**4 - 3*var**3 + 2*var**2 - var + 1, "polinomio de grado 4"),
        (f"sin({var_str})*exp(-{var_str}/3)", sin(var)*exp(-var/3), "función oscilatoria amortiguada"),
        (f"log({var_str})/{var_str}", log(var)/var, "función log(x)/x"),
        (f"({var_str}^2 + 1)/({var_str}^3 - {var_str})", (var**2 + 1)/(var**3 - var), "función racional compleja"),
        (f"sin({var_str}^2)", sin(var**2), "función seno de x²"),
        (f"1/sqrt(1-{var_str}^2)", 1/sqrt(1-var**2), "función asociada a la integral elíptica"),
        (f"log(1+{var_str}^2)/{var_str}", log(1+var**2)/var, "función logarítmica racional"),
        (f"(exp({var_str}) - exp(-{var_str}))/2", (exp(var) - exp(-var))/2, "función seno hiperbólico"),
    ]
    
    # Seleccionar funciones según complejidad
    if complexity == "simple":
        func_collection = simple_functions
    elif complexity == "complex":
        func_collection = complex_functions
    else:  # medium
        func_collection = medium_functions
    
    # Seleccionar función aleatoria
    func_str, func_expr, func_desc = random.choice(func_collection)
    
    # Generar representación LaTeX
    latex_form = sp.latex(func_expr)
    
    return func_str, latex_form, func_desc

def generate_random_bounds(function_str, var_str="x"):
    """
    Genera límites de integración apropiados para una función dada.
    
    Args:
        function_str (str): Cadena que representa la función
        var_str (str): Variable utilizada
    
    Returns:
        tuple: (lower, upper) - Límites inferior y superior
    """
    # Comprobar casos especiales para evitar singularidades
    if "log" in function_str or "sqrt" in function_str:
        # Para funciones con logaritmos o raíces, evitar valores negativos o cero
        lower = random.uniform(0.5, 2)
        upper = random.uniform(lower + 1, lower + 3)
    elif "1/" in function_str or "/" + var_str in function_str:
        # Para funciones con divisiones, evitar divisiones por cero
        candidates = [(-3, -1), (1, 3)]
        lower, upper = random.choice(candidates)
    elif "sqrt(1-" + var_str in function_str:
        # Para sqrt(1-x²), límites entre -1 y 1
        lower = random.uniform(-0.9, 0)
        upper = random.uniform(0, 0.9)
    elif "sin" in function_str or "cos" in function_str:
        # Para funciones trigonométricas, usar múltiplos de π
        options = [
            (0, "pi/2"),
            (0, "pi"),
            ("pi/4", "3*pi/4"),
            ("-pi/2", "pi/2")
        ]
        lower, upper = random.choice(options)
    else:
        # Para otras funciones, usar valores enteros simples
        options = [
            (0, 1),
            (-1, 1),
            (1, 2),
            (0, 2),
            (-2, 0)
        ]
        lower, upper = random.choice(options)
    
    return lower, upper

def generate_integral_example():
    """
    Genera un ejemplo aleatorio de integral definida.
    
    Returns:
        dict: Ejemplo con función, límites, resultado y explicación
    """
    # Seleccionar complejidad aleatoria
    complexity = random.choice(["simple", "medium", "medium", "complex"])
    
    # Generar función aleatoria
    func_str, latex_func, func_desc = generate_random_function(complexity)
    
    # Generar límites apropiados
    lower, upper = generate_random_bounds(func_str)
    
    # Calcular el resultado de la integral con mejor manejo de errores
    try:
        var = symbols('x')
        # Reemplazar exponentes y asegurar que la expresión es válida
        func_str_processed = func_str.replace('^', '**')
        func = sympify(func_str_processed)
        
        # Calcular la antiderivada
        antiderivative = integrate(func, var)
        
        # Procesar los límites de integración con manejo seguro
        # Para el límite inferior
        if isinstance(lower, str):
            try:
                # Manejar casos especiales como "pi" o "e"
                if lower == "pi":
                    lower_val = pi
                elif lower == "e":
                    lower_val = E
                else:
                    lower_val = sympify(lower)
            except:
                # En caso de error, usar un valor predeterminado
                lower_val = Float(0.0)
        else:
            # Asegurar que es un valor numérico
            try:
                lower_val = Float(lower)
            except:
                lower_val = Float(0.0)
        
        # Para el límite superior
        if isinstance(upper, str):
            try:
                # Manejar casos especiales
                if upper == "pi":
                    upper_val = pi
                elif upper == "e":
                    upper_val = E
                else:
                    upper_val = sympify(upper)
            except:
                # En caso de error, usar un valor predeterminado
                upper_val = Float(1.0)
        else:
            # Asegurar que es un valor numérico
            try:
                upper_val = Float(upper)
            except:
                upper_val = Float(1.0)
        
        # Evaluar la antiderivada en los límites
        try:
            upper_result = antiderivative.subs(var, upper_val)
            lower_result = antiderivative.subs(var, lower_val)
            result = upper_result - lower_result
            
            # Intentar simplificar el resultado
            if isinstance(result, sp.Expr):
                try:
                    result = result.evalf()
                except:
                    pass
        except Exception as eval_error:
            # Si hay error en la evaluación
            result = "No se pudo evaluar"
        
        # Intentar convertir a float para simplificar
        try:
            result_float = float(result)
            if abs(result_float - round(result_float, 2)) < 1e-10:
                result = round(result_float, 2)
            else:
                result = result_float
        except:
            # Mantener resultado simbólico si no se puede convertir
            pass
        
        # Generar explicación
        if complexity == "simple":
            difficulty = "sencillo"
        elif complexity == "medium":
            difficulty = "intermedio"
        else:
            difficulty = "avanzado"
            
        explanation = f"Este es un ejemplo {difficulty} de integral definida con una {func_desc}. "
        
        # Añadir contexto específico según la función
        if "sin" in func_str or "cos" in func_str:
            explanation += "Las integrales de funciones trigonométricas son fundamentales en análisis de Fourier y señales periódicas."
        elif "exp" in func_str:
            explanation += "Las integrales de funciones exponenciales aparecen frecuentemente en problemas de crecimiento y decaimiento."
        elif "log" in func_str:
            explanation += "Las integrales con logaritmos son útiles en teoría de la información y problemas de entropía."
        elif "sqrt" in func_str:
            explanation += "Las integrales con raíces cuadradas son comunes en problemas de física y geometría."
        elif "^3" in func_str or "^4" in func_str:
            explanation += "Las integrales de polinomios de grado superior aparecen en problemas de momento de inercia y análisis de curvas."
        else:
            explanation += "Este tipo de integrales es común en cálculos de área bajo la curva y acumulación de cantidades."
        
        return {
            "function": func_str,
            "latex_function": latex_func,
            "lower_bound": lower,
            "upper_bound": upper,
            "result": result,
            "description": func_desc,
            "explanation": explanation
        }
    
    except Exception as e:
        # Si hay error, recurrir a un ejemplo predefinido seguro
        return {
            "function": "x^2",
            "latex_function": "x^2",
            "lower_bound": 0,
            "upper_bound": 1,
            "result": 1/3,
            "description": "función cuadrática",
            "explanation": "Este es un ejemplo clásico de integral definida con una función cuadrática. El resultado 1/3 representa el área bajo la curva y=x² desde x=0 hasta x=1."
        }

def generate_area_between_curves_example():
    """
    Genera un ejemplo aleatorio de área entre curvas.
    
    Returns:
        dict: Ejemplo con funciones, límites, resultado y explicación
    """
    # Generar dos funciones y asegurar que una esté por encima de la otra en al menos una parte del dominio
    try:
        # Crear función base
        base_func_str, _, base_desc = generate_random_function("simple", "x")
        base_func = sympify(base_func_str.replace('^', '**'))
        var = symbols('x')
        
        # Crear segunda función sumando o restando una cantidad
        if random.choice([True, False]):
            # Función 2 por encima de función 1
            offset = random.randint(1, 5)
            second_func = base_func + offset
            second_func_str = f"({base_func_str}) + {offset}"
            top_func = second_func
            bottom_func = base_func
            top_func_str = second_func_str
            bottom_func_str = base_func_str
        else:
            # Función 1 por encima de función 2
            offset = random.randint(1, 5)
            second_func = base_func - offset
            second_func_str = f"({base_func_str}) - {offset}"
            top_func = base_func
            bottom_func = second_func
            top_func_str = base_func_str
            bottom_func_str = second_func_str
        
        # Generar límites adecuados
        lower, upper = generate_random_bounds(base_func_str)
        
        # Calcular el área entre las curvas
        diff_func = top_func - bottom_func
        
        # Integrar para obtener el área
        if isinstance(lower, str):
            lower_val = sympify(lower)
        else:
            lower_val = lower
            
        if isinstance(upper, str):
            upper_val = sympify(upper)
        else:
            upper_val = upper
        
        area_expr = integrate(diff_func, (var, lower_val, upper_val))
        
        # Intentar convertir a float
        try:
            area = float(area_expr)
        except:
            area = area_expr
        
        # Generar explicación
        explanation = f"Este ejemplo muestra cómo calcular el área entre dos curvas: una {base_desc} y una versión desplazada de la misma. "
        explanation += f"Observa que la función superior es {top_func_str} y la inferior es {bottom_func_str}. "
        explanation += "El área entre curvas es importante en aplicaciones como el cálculo de trabajo en física, el excedente del consumidor en economía, y la diferencia acumulada entre dos procesos en ingeniería."
        
        return {
            "function1": base_func_str,
            "function2": second_func_str,
            "lower_bound": lower,
            "upper_bound": upper,
            "result": area,
            "explanation": explanation
        }
    
    except Exception as e:
        # Ejemplo seguro predefinido
        return {
            "function1": "x^2",
            "function2": "x",
            "lower_bound": 0,
            "upper_bound": 1,
            "result": 1/6,
            "explanation": "Este es un ejemplo clásico de área entre curvas. La función y=x está por encima de y=x² en el intervalo [0,1], y el área entre ellas es 1/6 unidades cuadradas."
        }

def generate_riemann_sum_example():
    """
    Genera un ejemplo aleatorio de suma de Riemann.
    
    Returns:
        dict: Ejemplo con función, límites, número de subdivisiones, método y explicación
    """
    # Generar función aleatoria (preferimos funciones simples para sumas de Riemann)
    func_str, latex_func, func_desc = generate_random_function("simple", "x")
    
    # Generar límites apropiados
    lower, upper = generate_random_bounds(func_str)
    
    # Asegurar que los límites son numéricos para la suma de Riemann
    if isinstance(lower, str):
        try:
            lower_val = float(sympify(lower))
        except:
            lower_val = 0
    else:
        lower_val = lower
        
    if isinstance(upper, str):
        try:
            upper_val = float(sympify(upper))
        except:
            upper_val = 1
    else:
        upper_val = upper
    
    # Generar número de subdivisiones (mantenerlo pequeño para visualización clara)
    n = random.choice([4, 5, 6, 8, 10])
    
    # Seleccionar método
    method = random.choice(["left", "right", "midpoint"])
    
    # Generar explicación
    method_names = {"left": "izquierdo", "right": "derecho", "midpoint": "punto medio"}
    method_name = method_names[method]
    
    explanation = f"Este ejemplo utiliza la suma de Riemann con el método del punto {method_name} y {n} subdivisiones para aproximar la integral de una {func_desc}. "
    
    if method == "left":
        explanation += "El método del punto izquierdo evalúa la función en el extremo izquierdo de cada subintervalo, lo que tiende a sobreestimar el área bajo curvas crecientes y subestimarla para curvas decrecientes."
    elif method == "right":
        explanation += "El método del punto derecho evalúa la función en el extremo derecho de cada subintervalo, lo que tiende a subestimar el área bajo curvas crecientes y sobreestimarla para curvas decrecientes."
    else:  # midpoint
        explanation += "El método del punto medio evalúa la función en el centro de cada subintervalo, lo que generalmente proporciona una mejor aproximación que los métodos de punto izquierdo o derecho."
    
    explanation += f" Al aumentar el número de subdivisiones, la aproximación se acerca cada vez más al valor exacto de la integral definida."
    
    return {
        "function": func_str,
        "lower_bound": lower_val,
        "upper_bound": upper_val,
        "subdivisions": n,
        "method": method,
        "explanation": explanation
    }

def generate_engineering_application():
    """
    Genera un ejemplo aleatorio de aplicación de ingeniería relacionada con integrales.
    
    Returns:
        dict: Ejemplo con función, límites, tipo de cálculo, descripción y explicación
    """
    # Posibles escenarios de ingeniería
    engineering_scenarios = [
        {
            "title": "Consumo de Recursos del Servidor",
            "template": "Un servidor web tiene un consumo de recursos que varía según la función R(t) = {func} unidades por hora, donde t es el tiempo en horas desde que se inició el servicio. Calcula el consumo total de recursos durante el período desde t = {lower} hasta t = {upper} horas.",
            "var": "t",
            "type": "definite_integral",
            "complexity": "medium"
        },
        {
            "title": "Análisis de Tráfico de Red",
            "template": "El tráfico de datos en una red sigue la función T(t) = {func} GB por hora, donde t es la hora del día (de 0 a 24). Determina el volumen total de datos transferidos entre las {lower} y las {upper} horas.",
            "var": "t",
            "type": "definite_integral",
            "complexity": "medium"
        },
        {
            "title": "Optimización de Algoritmos",
            "template": "Dos algoritmos tienen tiempos de ejecución modelados por A₁(n) = {func1} y A₂(n) = {func2} milisegundos, donde n es el tamaño de entrada. Calcula la diferencia acumulada en rendimiento para entradas de tamaño entre n = {lower} y n = {upper}.",
            "var": "n",
            "type": "area_between_curves",
            "complexity": "simple"
        },
        {
            "title": "Fiabilidad del Software",
            "template": "La tasa de fallos de un sistema sigue la función F(t) = {func} fallos por día, donde t es el tiempo en días desde el despliegue. Calcula el número esperado de fallos durante los primeros {upper} días.",
            "var": "t",
            "lower": 0,
            "type": "definite_integral",
            "complexity": "simple"
        },
        {
            "title": "Análisis de Rendimiento",
            "template": "La función P(n) = {func} representa el tiempo de procesamiento en milisegundos para una entrada de tamaño n. Calcula el tiempo total de procesamiento acumulado para entradas desde n = {lower} hasta n = {upper}.",
            "var": "n",
            "type": "definite_integral",
            "complexity": "medium"
        }
    ]
    
    # Seleccionar escenario aleatorio
    scenario = random.choice(engineering_scenarios)
    
    # Generar función según la complejidad requerida
    func_str, _, _ = generate_random_function(scenario["complexity"], scenario["var"])
    
    # Generar límites apropiados o usar los predefinidos
    if "lower" in scenario:
        lower = scenario["lower"]
    else:
        if scenario["var"] == "t":
            # Para tiempo, usar valores no negativos
            lower = random.choice([0, 1, 2])
        else:
            lower = random.choice([1, 2, 5])
    
    if "upper" in scenario:
        upper = scenario["upper"]
    else:
        if scenario["var"] == "t":
            # Para tiempo, valores realistas
            upper = random.choice([8, 12, 24])
        else:
            upper = lower + random.choice([5, 10, 20])
    
    # Para áreas entre curvas, generar segunda función
    if scenario["type"] == "area_between_curves":
        # Crear segunda función como versión más simple o más compleja
        offset = random.randint(1, 5)
        if random.choice([True, False]):
            func2_str = f"log({scenario['var']})*{offset}"
        else:
            func2_str = f"{scenario['var']}*{offset}"
    else:
        func2_str = None
    
    # Rellenar la plantilla
    if scenario["type"] == "area_between_curves":
        description = scenario["template"].format(
            func1=func_str,
            func2=func2_str,
            lower=lower,
            upper=upper
        )
    else:
        description = scenario["template"].format(
            func=func_str,
            lower=lower,
            upper=upper
        )
    
    # Generar resultado básico
    try:
        var = symbols(scenario["var"])
        func = sympify(func_str.replace('^', '**'))
        
        if scenario["type"] == "definite_integral":
            result = integrate(func, (var, lower, upper))
        else:  # area_between_curves
            func2 = sympify(func2_str.replace('^', '**'))
            # Determinar cuál está arriba
            midpoint = (lower + upper) / 2
            val1 = func.subs(var, midpoint)
            val2 = func2.subs(var, midpoint)
            
            if val1 > val2:
                result = integrate(func - func2, (var, lower, upper))
            else:
                result = integrate(func2 - func, (var, lower, upper))
    except:
        # Si hay error en el cálculo, dar un valor plausible
        result = round(random.uniform(10, 100), 2)
    
    # Generar explicación
    explanation = f"Este problema modela una situación real en ingeniería de software donde se utiliza el cálculo integral para analizar el comportamiento acumulativo a lo largo del tiempo o para diferentes tamaños de entrada. "
    
    if scenario["type"] == "definite_integral":
        explanation += f"La integral de la función dada representa la acumulación total de la cantidad durante el intervalo especificado. "
    else:
        explanation += f"El área entre las dos curvas representa la diferencia acumulada entre los dos modelos o procesos a lo largo del rango especificado. "
    
    explanation += "Este tipo de análisis es fundamental en la ingeniería de software para la optimización de recursos, la planificación de capacidad y la evaluación comparativa de algoritmos."
    
    # Crear y devolver el ejemplo
    example = {
        "title": scenario["title"],
        "description": description,
        "function1": func_str,
        "variable": scenario["var"],
        "lower_bound": lower,
        "upper_bound": upper,
        "calculation_type": scenario["type"],
        "explanation": explanation,
        "result": result
    }
    
    if func2_str:
        example["function2"] = func2_str
    
    return example