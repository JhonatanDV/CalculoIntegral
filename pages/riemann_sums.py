import streamlit as st
import sympy as sp
import numpy as np
from utils.riemann_sum import calculate_riemann_sum, get_riemann_sum_steps
from utils.plotting import plot_riemann_sum
from components.math_input import create_math_input
from components.solution_display import display_riemann_sum_solution
from assets.examples import riemann_sum_examples

def show():
    st.title("📊 Calculadora de Sumas de Riemann")
    
    # Initialize page-specific session state
    if "input_value_riemann_function" not in st.session_state:
        st.session_state["input_value_riemann_function"] = "x^2"
    if "riemann_lower" not in st.session_state:
        st.session_state.riemann_lower = "0"
    if "riemann_upper" not in st.session_state:
        st.session_state.riemann_upper = "1"
    if "riemann_n" not in st.session_state:
        st.session_state.riemann_n = 10
    
    st.markdown("""
    Las sumas de Riemann se utilizan para aproximar la integral definida (área bajo una curva) 
    dividiendo el área en rectángulos.
    
    Esta calculadora te permite:
    - Calcular sumas de Riemann usando métodos de punto izquierdo, derecho o punto medio
    - Visualizar los rectángulos utilizados en la aproximación
    - Ver soluciones paso a paso
    """)
    
    # Main input section
    st.header("Función e Intervalo")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Input Method Selection
        input_method = st.radio("Método de Entrada", ["Teclado", "Subir Imagen"], horizontal=True, key="riemann_input_method")
        
        if input_method == "Teclado":
            function_input = create_math_input("Función f(x)", st.session_state.get("input_value_riemann_function", "x^2"), key="riemann_function")
        else:
            st.warning("La funcionalidad de procesamiento de imágenes matemáticas no está disponible. Por favor, usa el método de teclado.")
            function_input = st.session_state.get("input_value_riemann_function", "x^2")
                
        # Save the function input to session state
        st.session_state["input_value_riemann_function"] = function_input
        
        col1a, col1b = st.columns(2)
        with col1a:
            lower_bound = st.text_input("Límite Inferior (a)", st.session_state.get("riemann_lower", "0"), key="riemann_lower_input")
            st.session_state.riemann_lower = lower_bound
        with col1b:
            upper_bound = st.text_input("Límite Superior (b)", st.session_state.get("riemann_upper", "1"), key="riemann_upper_input")
            st.session_state.riemann_upper = upper_bound
        
        n_subdivisions = st.number_input("Número de Subdivisiones (n)", min_value=1, max_value=100, value=st.session_state.get("riemann_n", 10), key="riemann_n_input")
        st.session_state.riemann_n = n_subdivisions
        
        method = st.selectbox(
            "Método de Muestreo",
            ["left", "right", "midpoint"],
            index=0,
            key="riemann_method_input"
        )
    
    with col2:
        st.markdown("### Problemas de Ejemplo")
        selected_example = st.selectbox(
            "Selecciona un ejemplo de los materiales del curso:",
            list(riemann_sum_examples.keys()),
            key="riemann_example"
        )
        
        if st.button("Cargar Ejemplo", key="load_riemann_example"):
            example = riemann_sum_examples[selected_example]
            # Update session state values
            st.session_state["input_value_riemann_function"] = example["function"]
            st.session_state.riemann_lower = str(example["lower_bound"])
            st.session_state.riemann_upper = str(example["upper_bound"])
            st.session_state.riemann_n = example["subdivisions"]
            st.rerun()
    
    # Calculate button
    if st.button("Calcular Suma de Riemann", key="calculate_riemann"):
        try:
            # Parse inputs
            func_str = function_input
            a = float(lower_bound) if lower_bound is not None else 0
            b = float(upper_bound) if upper_bound is not None else 1
            n = int(n_subdivisions) if n_subdivisions is not None else 10
            
            # Calculate Riemann sum
            riemann_sum, _ = calculate_riemann_sum(func_str, a, b, n, method, "x")
            
            # Get step-by-step solution
            steps = get_riemann_sum_steps(func_str, a, b, n, method, "x")
            
            # Display the plot
            plot_riemann_sum(func_str, a, b, n, method, "x")
            
            # Display the solution
            display_riemann_sum_solution(func_str, a, b, n, method, riemann_sum, steps, diagram_provided=True)
            
        except Exception as e:
            st.error(f"Error al calcular la suma de Riemann: {str(e)}")
    
    # Theory section
    with st.expander("Aprende sobre las Sumas de Riemann"):
        st.markdown("""
        ### ¿Qué es una Suma de Riemann?
        
        Una suma de Riemann es un método para aproximar la integral definida (o área bajo una curva) 
        dividiendo el área en formas más simples (rectángulos) cuyas áreas son fáciles de calcular.
        
        ### Tipos de Sumas de Riemann
        
        1. **Suma de Riemann Izquierda**: Utiliza el valor de la función en el extremo izquierdo de cada subintervalo.
        2. **Suma de Riemann Derecha**: Utiliza el valor de la función en el extremo derecho de cada subintervalo.
        3. **Suma de Riemann del Punto Medio**: Utiliza el valor de la función en el punto medio de cada subintervalo.
        
        ### La Fórmula
        
        Para una función $f(x)$ en un intervalo $[a, b]$ dividido en $n$ subintervalos iguales, la suma de Riemann es:
        
        $R_n = \Delta x \sum_{i=1}^{n} f(x_i^*)$
        
        donde:
        - $\Delta x = \frac{b-a}{n}$ es el ancho de cada subintervalo
        - $x_i^*$ es el punto de muestra en el $i$-ésimo subintervalo
        
        ### Conexión con Integrales Definidas
        
        A medida que aumenta el número de subintervalos, la suma de Riemann se aproxima a la integral definida:
        
        $\lim_{n \to \infty} \sum_{i=1}^{n} f(x_i^*) \Delta x = \int_{a}^{b} f(x) \, dx$
        
        Esta es la conexión fundamental entre las sumas de Riemann y las integrales definidas.
        """)