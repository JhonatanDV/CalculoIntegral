import streamlit as st
import sympy as sp
import numpy as np
import random
from utils.calculator import evaluate_expression, solve_integral
from utils.plotting import plot_function, plot_integral, plot_area_between_curves
from components.math_input import create_math_input
from components.solution_display import display_solution, display_area_between_curves_solution
from utils.area_calculator import calculate_area_between_curves

# Lista de escenarios de ingeniería de software
SOFTWARE_ENGINEERING_SCENARIOS = [
    {
        "title": "Consumo de Recursos del Servidor",
        "description": "Un servidor web tiene un consumo de recursos de memoria modelado por la función M(t) = t² + 2t + 1 MB, donde t es el tiempo en minutos desde que inició el proceso. Calcula el total de recursos utilizados durante los primeros {n} minutos.",
        "function": "t^2 + 2*t + 1",
        "variable": "t",
        "default_lower": 0,
        "default_upper": 5,
        "type": "integral",
        "interpretation": "Este resultado representa la cantidad total de memoria (en MB) consumida por el servidor durante el período de tiempo especificado. Esta información es crucial para planificar la capacidad y optimizar el rendimiento del servidor."
    },
    {
        "title": "Optimización de Base de Datos",
        "description": "La velocidad de consulta en una base de datos se modela mediante la función V(n) = 3n² + 2n + 1 milisegundos, donde n representa el tamaño del conjunto de datos. Calcula el tiempo acumulado para consultas con tamaños desde {a} hasta {b}.",
        "function": "3*n^2 + 2*n + 1",
        "variable": "n",
        "default_lower": 1,
        "default_upper": 10,
        "type": "integral",
        "interpretation": "Este resultado representa el tiempo total acumulado (en milisegundos) para procesar consultas de diferentes tamaños. Esto ayuda a identificar cuellos de botella y optimizar el rendimiento de la base de datos."
    },
    {
        "title": "Interacción de Usuarios",
        "description": "La tasa de usuarios que interactúan con una aplicación web sigue la función U(t) = 50e^(-0.2t) usuarios por minuto, donde t es el tiempo en minutos desde el lanzamiento. Calcula el número total de usuarios que interactuaron durante las primeras {n} horas.",
        "function": "50*exp(-0.2*t)",
        "variable": "t",
        "default_lower": 0,
        "default_upper": 60,
        "type": "integral",
        "interpretation": "Este resultado representa el número total de usuarios que interactuaron con la aplicación durante el período especificado. Esto es útil para analizar patrones de uso y planificar la capacidad del sistema."
    },
    {
        "title": "Diferencia entre Uso de CPU y Memoria",
        "description": "Un proceso de computación utiliza CPU según la función C(t) = 2t + 5 unidades y memoria según M(t) = t² + 2t + 1 unidades, donde t es el tiempo en minutos. Calcula la diferencia acumulada entre estos recursos durante un período de {a} a {b} minutos.",
        "function1": "t^2 + 2*t + 1",
        "function2": "2*t + 5",
        "variable": "t",
        "default_lower": 0,
        "default_upper": 5,
        "type": "area_between_curves",
        "interpretation": "Este resultado representa la diferencia acumulada entre el uso de memoria y CPU durante el período especificado. Un valor positivo indica que el proceso es más intensivo en memoria, mientras que un valor negativo indica que es más intensivo en CPU."
    },
    {
        "title": "Rendimiento de Algoritmos",
        "description": "Dos algoritmos de ordenamiento tienen tiempos de ejecución modelados por A₁(n) = 0.1n² + n y A₂(n) = 5n·log(n), donde n es el tamaño de la entrada. Determina para qué tamaños de entrada el primer algoritmo supera al segundo calculando el área entre las curvas desde n = {a} hasta n = {b}.",
        "function1": "0.1*n^2 + n",
        "function2": "5*n*log(n)",
        "variable": "n",
        "default_lower": 1,
        "default_upper": 100,
        "type": "area_between_curves",
        "interpretation": "Este resultado ayuda a identificar los rangos de tamaños de entrada donde un algoritmo supera al otro. Esta información es crucial para seleccionar el algoritmo óptimo según el tamaño de los datos."
    },
    {
        "title": "Crecimiento de la Complejidad de Software",
        "description": "La complejidad de un sistema de software crece según la función C(t) = t³ - 2t² + 3t, donde t es el tiempo en meses desde el inicio del proyecto. Calcula el incremento total de complejidad entre los meses {a} y {b}.",
        "function": "t^3 - 2*t^2 + 3*t",
        "variable": "t",
        "default_lower": 1,
        "default_upper": 12,
        "type": "integral",
        "interpretation": "Este resultado representa el aumento acumulado en la complejidad del software durante el período especificado. Entender este crecimiento es esencial para la planificación de refactorizaciones y mantenimiento del código."
    },
    {
        "title": "Fiabilidad del Software",
        "description": "La tasa de fallos de un sistema sigue la función F(t) = 10e^(-0.5t) fallos por día, donde t es el tiempo en días desde el despliegue. Calcula el número esperado de fallos durante los primeros {n} días.",
        "function": "10*exp(-0.5*t)",
        "variable": "t",
        "default_lower": 0,
        "default_upper": 30,
        "type": "integral",
        "interpretation": "Este resultado representa el número total esperado de fallos durante el período especificado. Esta información es valiosa para la planificación de pruebas y garantía de calidad."
    },
    {
        "title": "Rendimiento en Procesamiento Paralelo",
        "description": "La eficiencia de un sistema de procesamiento paralelo varía según la función E(n) = 1 - log(n)/n, donde n es el número de núcleos. Calcula la eficiencia acumulada cuando el sistema escala de {a} a {b} núcleos.",
        "function": "1 - log(n)/n",
        "variable": "n",
        "default_lower": 1,
        "default_upper": 64,
        "type": "integral",
        "interpretation": "Este resultado representa la eficiencia acumulada a medida que el sistema escala en el número de núcleos. Esto ayuda a determinar el punto óptimo de paralelización para maximizar el rendimiento."
    }
]

def generate_random_scenario():
    """Genera un escenario aleatorio de la lista de escenarios predefinidos."""
    scenario = random.choice(SOFTWARE_ENGINEERING_SCENARIOS)
    
    # Generar valores aleatorios para los parámetros del problema
    if 'default_lower' in scenario and 'default_upper' in scenario:
        a = scenario['default_lower']
        b = scenario['default_upper']
        
        # Añadir algo de variabilidad a los límites
        if scenario['type'] == 'integral':
            scenario_copy = scenario.copy()
            
            # Ajustar la descripción con los valores reales
            if '{a}' in scenario_copy['description'] and '{b}' in scenario_copy['description']:
                scenario_copy['description'] = scenario_copy['description'].format(a=a, b=b)
            elif '{n}' in scenario_copy['description']:
                scenario_copy['description'] = scenario_copy['description'].format(n=b)
                
            return scenario_copy
        elif scenario['type'] == 'area_between_curves':
            scenario_copy = scenario.copy()
            
            # Ajustar la descripción con los valores reales
            if '{a}' in scenario_copy['description'] and '{b}' in scenario_copy['description']:
                scenario_copy['description'] = scenario_copy['description'].format(a=a, b=b)
                
            return scenario_copy
    
    return scenario

def show():
    st.title("🔄 Generador de Escenarios de Ingeniería de Software")
    
    st.markdown("""
    Esta sección genera automáticamente problemas de cálculo integral aplicados a situaciones reales 
    de ingeniería de software. Estos problemas representan casos prácticos donde el cálculo integral 
    es útil para modelar y resolver desafíos comunes en el desarrollo y operación de software.
    """)
    
    # Botón para generar un nuevo escenario
    if st.button("Generar Nuevo Escenario", key="generate_scenario"):
        st.session_state.current_scenario = generate_random_scenario()
    
    # Inicializar el escenario actual si no existe
    if 'current_scenario' not in st.session_state:
        st.session_state.current_scenario = generate_random_scenario()
    
    # Mostrar el escenario actual
    scenario = st.session_state.current_scenario
    
    st.header(scenario['title'])
    st.markdown(f"**Descripción del Problema:**\n\n{scenario['description']}")
    
    # Sección de solución
    st.header("Resolver el Problema")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Variables de entrada según el tipo de problema
        if scenario['type'] == 'integral':
            # Mostrar y permitir editar la función
            function_input = create_math_input("Función a integrar", scenario['function'], key="scenario_function")
            
            # Límites de integración
            col1a, col1b = st.columns(2)
            with col1a:
                lower_bound = st.text_input("Límite inferior", str(scenario['default_lower']), key="scenario_lower")
            with col1b:
                upper_bound = st.text_input("Límite superior", str(scenario['default_upper']), key="scenario_upper")
            
            variable = st.text_input("Variable", scenario['variable'], key="scenario_variable")
            
            # Botón para calcular
            if st.button("Calcular Integral", key="calculate_scenario_integral"):
                try:
                    # Asegurar que la variable sea un string
                    var_str = str(variable) if variable is not None else "x"
                    
                    # Calcular la integral
                    result, steps = solve_integral(function_input, lower_bound, upper_bound, var_str)
                    
                    # Mostrar la gráfica
                    plot_integral(function_input, lower_bound, upper_bound, var_str)
                    
                    # Mostrar la solución
                    display_solution(function_input, lower_bound, upper_bound, result, steps)
                    
                    # Interpretación del resultado
                    st.header("Interpretación en Ingeniería de Software")
                    st.markdown(scenario['interpretation'])
                    st.markdown(f"""
                    En este caso específico, el valor calculado de **{result:.6f}** representa:
                    
                    - Para el problema "{scenario['title']}"
                    - En el intervalo [{lower_bound}, {upper_bound}] de {var_str}
                    """)
                    
                except Exception as e:
                    st.error(f"Error al calcular la integral: {str(e)}")
        
        elif scenario['type'] == 'area_between_curves':
            # Mostrar y permitir editar las funciones
            function1_input = create_math_input("Primera Función", scenario['function1'], key="scenario_function1")
            function2_input = create_math_input("Segunda Función", scenario['function2'], key="scenario_function2")
            
            # Límites de integración
            col1a, col1b = st.columns(2)
            with col1a:
                lower_bound = st.text_input("Límite inferior", str(scenario['default_lower']), key="scenario_lower")
            with col1b:
                upper_bound = st.text_input("Límite superior", str(scenario['default_upper']), key="scenario_upper")
            
            variable = st.text_input("Variable", scenario['variable'], key="scenario_variable")
            
            # Botón para calcular
            if st.button("Calcular Área Entre Curvas", key="calculate_scenario_area"):
                try:
                    # Asegurar que la variable sea un string
                    var_str = str(variable) if variable is not None else "x"
                    
                    # Calcular área entre curvas
                    area, steps = calculate_area_between_curves(function1_input, function2_input, float(lower_bound), float(upper_bound), var_str)
                    
                    # Mostrar la gráfica
                    plot_area_between_curves(function1_input, function2_input, float(lower_bound), float(upper_bound), var_str)
                    
                    # Mostrar la solución
                    display_area_between_curves_solution(function1_input, function2_input, float(lower_bound), float(upper_bound), area, steps)
                    
                    # Interpretación del resultado
                    st.header("Interpretación en Ingeniería de Software")
                    st.markdown(scenario['interpretation'])
                    st.markdown(f"""
                    En este caso específico, el valor calculado de **{area:.6f}** representa:
                    
                    - Para el problema "{scenario['title']}"
                    - En el intervalo [{lower_bound}, {upper_bound}] de {var_str}
                    """)
                    
                except Exception as e:
                    st.error(f"Error al calcular el área entre curvas: {str(e)}")
    
    with col2:
        st.markdown("### Información del Modelo Matemático")
        
        if scenario['type'] == 'integral':
            st.markdown(f"""
            **Tipo de problema:** Integral Definida
            
            **Función a integrar:** 
            ```
            {scenario['function']}
            ```
            
            **Variable de integración:** {scenario['variable']}
            
            **Rango típico:** [{scenario['default_lower']}, {scenario['default_upper']}]
            
            La integral representa la acumulación o suma total de la cantidad 
            que está siendo modelada por la función a lo largo del intervalo.
            """)
        
        elif scenario['type'] == 'area_between_curves':
            st.markdown(f"""
            **Tipo de problema:** Área Entre Curvas
            
            **Primera función:** 
            ```
            {scenario['function1']}
            ```
            
            **Segunda función:** 
            ```
            {scenario['function2']}
            ```
            
            **Variable:** {scenario['variable']}
            
            **Rango típico:** [{scenario['default_lower']}, {scenario['default_upper']}]
            
            El área entre curvas representa la diferencia acumulada entre las dos 
            funciones a lo largo del intervalo especificado.
            """)
    
    # Sección de teoría y aplicación
    with st.expander("Más sobre aplicaciones del cálculo integral en ingeniería de software"):
        st.markdown("""
        ### Aplicaciones del Cálculo Integral en Ingeniería de Software
        
        El cálculo integral tiene numerosas aplicaciones en ingeniería de software:
        
        #### 1. Análisis de Rendimiento
        - **Consumo de recursos:** Permite calcular el uso total de memoria, CPU o ancho de banda a lo largo del tiempo.
        - **Optimización:** Ayuda a identificar cuellos de botella en el rendimiento del sistema.
        
        #### 2. Análisis de Fiabilidad
        - **Tasas de fallo:** Calcula el número esperado de fallos durante períodos específicos.
        - **Tiempo medio entre fallos (MTBF):** Modelado mediante integrales para sistemas complejos.
        
        #### 3. Optimización de Algoritmos
        - **Comparación de algoritmos:** Permite determinar qué algoritmo es más eficiente para diferentes tamaños de entrada.
        - **Complejidad amortizada:** Utiliza integrales para analizar el rendimiento a lo largo del tiempo.
        
        #### 4. Modelado de Usuarios y Carga
        - **Patrones de uso:** Calcula el número total de usuarios o solicitudes durante períodos específicos.
        - **Planificación de capacidad:** Ayuda a dimensionar infraestructura basándose en patrones de carga modelados matemáticamente.
        
        #### 5. Crecimiento y Evolución del Software
        - **Acumulación de deuda técnica:** Modelada como la integral de la tasa de introducción de deuda técnica.
        - **Evolución de la complejidad:** Cuantifica cómo crece la complejidad a lo largo del tiempo.
        """)