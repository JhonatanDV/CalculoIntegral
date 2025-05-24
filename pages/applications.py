import streamlit as st
import sympy as sp
import numpy as np
from utils.calculator import evaluate_expression, solve_integral
from utils.plotting import plot_function, plot_integral, plot_area_between_curves
from components.math_input import create_math_input
from components.solution_display import display_solution, display_area_between_curves_solution
from assets.examples import engineering_applications_examples
from utils.area_calculator import calculate_area_between_curves

def show():
    st.title("🔧 Engineering Applications of Integrals")
    
    # Initialize page-specific session state
    if "input_value_application_function1" not in st.session_state:
        st.session_state["input_value_application_function1"] = "t^2 + 2*t + 1"
    if "input_value_application_function2" not in st.session_state:
        st.session_state["input_value_application_function2"] = "2*t + 5"
    if "application_description" not in st.session_state:
        st.session_state.application_description = ""
    if "application_lower_bound" not in st.session_state:
        st.session_state.application_lower_bound = "0"
    if "application_upper_bound" not in st.session_state:
        st.session_state.application_upper_bound = "5"
    if "application_calculation_type" not in st.session_state:
        st.session_state.application_calculation_type = "definite_integral"
    
    st.markdown("""
    Esta sección demuestra cómo se aplica el cálculo integral para resolver problemas de ingeniería,
    particularmente en contextos de ingeniería de software.
    
    Los ejemplos incluyen:
    - Consumo de recursos del servidor a lo largo del tiempo
    - Patrones de interacción del usuario
    - Optimización en consultas de bases de datos
    - Análisis de complejidad de algoritmos
    """)
    
    # Application selection
    application_type = st.selectbox(
        "Selecciona el tipo de aplicación",
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
        "Selecciona un problema de ejemplo:",
        list(examples.keys()) if examples else ["No hay ejemplos disponibles"],
        key="selected_application_example"
    )
    
    if st.button("Cargar ejemplo", key="load_application_example") and examples:
        example = examples[selected_example]
        st.session_state.application_description = example.get("description", "")
        st.session_state["input_value_application_function1"] = example.get("function1", "")
        if "function2" in example:
            st.session_state["input_value_application_function2"] = example.get("function2", "")
        st.session_state.application_lower_bound = str(example.get("lower_bound", "0"))
        st.session_state.application_upper_bound = str(example.get("upper_bound", "1"))
        st.session_state.application_calculation_type = example.get("calculation_type", "definite_integral")
        st.rerun()
    
    # Problem description
    st.header("Descripción del problema")
    problem_description = st.text_area(
        "Descripción del problema",
        value=st.session_state.get("application_description", ""),
        height=100,
        key="application_description_input"
    )
    st.session_state.application_description = problem_description
    
    # Calculation type
    calculation_type = st.selectbox(
        "Tipo de cálculo",
        ["Definite Integral", "Area Between Curves"],
        index=0 if st.session_state.get("application_calculation_type", "") == "definite_integral" else 1,
        key="application_calculation_type_input"
    )
    # Convert selection to internal value
    internal_calc_type = "definite_integral" if calculation_type == "Definite Integral" else "area_between_curves"
    st.session_state.application_calculation_type = internal_calc_type
    
    # Main input section
    st.header("Modelo matemático")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Input Method Selection
        input_method = st.radio("Método de entrada", ["Keyboard", "Upload Image"], horizontal=True, key="app_input_method")
        
        if input_method == "Keyboard":
            function1_input = create_math_input(
                "Primera función f₁(t)" if calculation_type == "Area Between Curves" else "Función f(t)",
                st.session_state.get("input_value_application_function1", "t^2 + 2*t + 1"),
                key="application_function1"
            )
            
            if calculation_type == "Area Between Curves":
                function2_input = create_math_input(
                    "Segunda función f₂(t)",
                    st.session_state.get("input_value_application_function2", "2*t + 5"),
                    key="application_function2"
                )
            else:
                function2_input = None
        else:
            st.markdown("#### Primera función")
            uploaded_file1 = st.file_uploader("Subir una imagen para la primera función", type=["jpg", "jpeg", "png"], key="app_file_uploader1")
            if uploaded_file1 is not None:
                st.image(uploaded_file1, caption="Primera función subida", width=300)
                st.info("La funcionalidad de procesamiento de imágenes matemáticas estará disponible próximamente.")
            function1_input = st.session_state.get("input_value_application_function1", "t^2 + 2*t + 1")
            
            if calculation_type == "Area Between Curves":
                st.markdown("#### Segunda función")
                uploaded_file2 = st.file_uploader("Subir una imagen para la segunda función", type=["jpg", "jpeg", "png"], key="app_file_uploader2")
                if uploaded_file2 is not None:
                    st.image(uploaded_file2, caption="Segunda función subida", width=300)
                    st.info("La funcionalidad de procesamiento de imágenes matemáticas estará disponible próximamente.")
                function2_input = st.session_state.get("input_value_application_function2", "2*t + 5")
            else:
                function2_input = None
        
        # Save functions to session state
        st.session_state["input_value_application_function1"] = function1_input
        if function2_input:
            st.session_state["input_value_application_function2"] = function2_input
        
        col1a, col1b = st.columns(2)
        with col1a:
            lower_bound = st.text_input(
                "Límite inferior (a)",
                st.session_state.get("application_lower_bound", "0"),
                key="application_lower_bound_input"
            )
            st.session_state.application_lower_bound = lower_bound
        with col1b:
            upper_bound = st.text_input(
                "Límite superior (b)",
                st.session_state.get("application_upper_bound", "5"),
                key="application_upper_bound_input"
            )
            st.session_state.application_upper_bound = upper_bound
    
    with col2:
        st.markdown("### Visualización del modelo")
        
        try:
            if calculation_type == "Definite Integral":
                fig = plot_function(function1_input, x_range=(float(lower_bound)-1, float(upper_bound)+1), var_str="t")
                st.plotly_chart(fig, use_container_width=True)
            else:
                fig = plot_function(function1_input, x_range=(float(lower_bound)-1, float(upper_bound)+1), var_str="t", color='blue')
                fig.add_trace(plot_function(function2_input, x_range=(float(lower_bound)-1, float(upper_bound)+1), var_str="t", color='green').data[0])
                st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.info("Ingresa funciones y límites válidos para ver la visualización")
    
    # Calculate button
    if st.button("Resolver problema", key="calculate_application"):
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
                st.header("Interpretación de ingeniería")
                st.markdown(f"""
                El valor calculado de {result:.6f} representa la cantidad total acumulada en el intervalo [{lower_bound}, {upper_bound}].
                
                En el contexto del problema:
                """)
                
                if "server" in problem_description.lower() and "resource" in problem_description.lower():
                    st.markdown(f"- Esto representa el **consumo total de recursos** del servidor durante el período de tiempo dado.")
                elif "user" in problem_description.lower() and "load" in problem_description.lower():
                    st.markdown(f"- Esto representa la **carga total de usuarios** en el sistema durante el período de tiempo dado.")
                elif "algorithm" in problem_description.lower() and "complex" in problem_description.lower():
                    st.markdown(f"- Esto representa el **tiempo de procesamiento acumulativo** del algoritmo en todos los inputs del rango.")
                else:
                    st.markdown(f"- Este valor representa la cantidad total acumulada descrita en el problema.")
                
            else:  # Area Between Curves
                # Calculate area
                area, steps = calculate_area_between_curves(function1_input, function2_input, a, b, "t")
                
                # Display the plot
                plot_area_between_curves(function1_input, function2_input, a, b, "t")
                
                # Display the solution
                display_area_between_curves_solution(function1_input, function2_input, a, b, area, steps)
                
                # Interpretation
                st.header("Interpretación de ingeniería")
                st.markdown(f"""
                El área calculada de {area:.6f} representa la diferencia total entre las dos funciones en el intervalo [{lower_bound}, {upper_bound}].
                
                En el contexto del problema:
                """)
                
                if "database" in problem_description.lower() and "optim" in problem_description.lower():
                    st.markdown(f"- Esto representa el **potencial de optimización** en las operaciones de la base de datos.")
                elif "server" in problem_description.lower() and ("memory" in problem_description.lower() or "cpu" in problem_description.lower()):
                    st.markdown(f"- Esto representa la **diferencia entre tipos de recursos** consumidos por el servidor.")
                else:
                    st.markdown(f"- Este valor representa la diferencia total entre las dos cantidades descritas en el problema.")
            
        except Exception as e:
            st.error(f"Error al resolver el problema: {str(e)}")
    
    # Theory section
    with st.expander("Aplicaciones de integrales en ingeniería de software"):
        st.markdown("""
        ### Cálculo integral en ingeniería de software
        
        El cálculo integral tiene varias aplicaciones importantes en la ingeniería de software:
        
        #### 1. Análisis de rendimiento
        
        - **Consumo de recursos**: Cálculo del uso total de memoria, CPU o ancho de banda a lo largo del tiempo
        - **Medición de rendimiento**: Análisis del número total de transacciones procesadas durante un período
        
        #### 2. Pruebas de carga y planificación de capacidad
        
        - **Modelado de carga de usuarios**: Predicción de cargas máximas y requisitos de recursos
        - **Escalado de servidores**: Determinar cuándo escalar recursos basándose en métricas de carga integradas
        
        #### 3. Análisis de algoritmos
        
        - **Complejidad temporal**: Análisis del rendimiento promedio o esperado de los algoritmos
        - **Compensaciones espacio-tiempo**: Optimización de algoritmos basada en métricas de rendimiento integradas
        
        #### 4. Análisis de datos y aprendizaje automático
        
        - **Distribuciones de probabilidad**: Trabajo con distribuciones de probabilidad continuas
        - **Minimización de errores**: Minimización de funciones de error en modelos de aprendizaje automático
        
        #### 5. Gráficos y simulación
        
        - **Motores de física**: Cálculo de trayectorias, velocidades y otras propiedades físicas
        - **Gráficos por computadora**: Trazado de rayos, modelos de iluminación y ecuaciones de renderizado
        
        Al comprender y aplicar el cálculo integral, los ingenieros de software pueden construir sistemas más eficientes,
        escalables y matemáticamente sólidos.
        """)
