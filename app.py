import streamlit as st
import sympy as sp
from sympy import symbols, sympify, solve, diff, integrate, Rational
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from components.math_input import create_math_input
from components.solution_display import display_solution
from utils.calculator import evaluate_expression, solve_integral
from utils.plotting import plot_function, plot_integral
import streamlit.components.v1 as components
from components.math_keyboard import math_keyboard

# Page configuration
st.set_page_config(
    page_title="CalcuMaster - Calculadora de Cálculo Integral",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",  # Ocultar sidebar por defecto
)

# Custom CSS
st.markdown("""
<style>
    /* Colores y estilos generales */
    .main {
        background-color: #f0f2f6;
    }
    h1, h2, h3 {
        color: #1e3a8a;
        font-weight: 600;
    }
    .stButton>button {
        background-color: #4e8df5;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 8px 16px;
        font-weight: 600;
    }
    .stButton>button:hover {
        background-color: #3670cc;
    }
    
    /* Ocultar la barra de hamburguesa y el footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Estilo para la caja de entrada matemática */
    .math-input-box {
        border: 2px solid #4e8df5;
        border-radius: 8px;
        padding: 15px;
        background-color: white;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Estilos para los tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f1f3f6;
        border-radius: 4px 4px 0 0;
        padding: 10px 16px;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #4e8df5;
        color: white;
    }
    
    /* Estilo para la sección de soluciones */
    .solution-box {
        background-color: #eef4ff;
        border-left: 4px solid #4e8df5;
        padding: 16px;
        border-radius: 0 8px 8px 0;
        margin-top: 16px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    /* Ocultar sidebar completamente */
    .css-1d391kg, .css-14xtw13 {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state variables if they don't exist
if 'function_str' not in st.session_state:
    st.session_state.function_str = "x^2"
if 'lower_bound' not in st.session_state:
    st.session_state.lower_bound = "0"
if 'upper_bound' not in st.session_state:
    st.session_state.upper_bound = "1"
if 'variable' not in st.session_state:
    st.session_state.variable = "x"
if 'n_subdivisions' not in st.session_state:
    st.session_state.n_subdivisions = 6
if 'show_keyboard' not in st.session_state:
    st.session_state.show_keyboard = False
if 'math_expression' not in st.session_state:
    st.session_state.math_expression = "x^2"

# Function to process uploaded math images
def process_uploaded_math_image():
    # Placeholder for future OCR functionality
    st.error("La funcionalidad de procesamiento de imágenes matemáticas no está disponible actualmente.")
    st.info("Por favor, ingresa la expresión matemática usando el teclado.")

# Main application header
st.title("🧮 CalcuMaster: Calculadora de Cálculo Integral")
st.markdown("La herramienta interactiva para resolver y visualizar problemas de cálculo integral")

# Main mode selection
app_mode = st.selectbox(
    "Selecciona un Modo",
    ["Inicio", "Integrales Definidas", "Sumas de Riemann", "Área Entre Curvas", "Aplicaciones de Ingeniería", "Escenarios de Ingeniería de Software"],
    key="app_mode_select"
)

# Home page
if app_mode == "Inicio":
    st.header("Calculadora Rápida de Integrales")
    
    # Math keyboard toggle
    if st.button("Mostrar Teclado Matemático", key="toggle_keyboard"):
        st.session_state.show_keyboard = not st.session_state.show_keyboard
        st.rerun()
        
    # Show math keyboard if enabled
    if st.session_state.show_keyboard:
        keyboard_open = math_keyboard("home")
        if not keyboard_open:
            st.session_state.show_keyboard = False
            st.rerun()
        # Sincronizar la expresión del teclado con el campo de función
        if "math_expression_home" in st.session_state:
            st.session_state.function_str = st.session_state["math_expression_home"]
    
    # Mathematical input section
    st.markdown("<div class='math-input-box'>", unsafe_allow_html=True)
    
    # Text input field
    function_input = st.text_input(
        "Función f(x)", 
        value=st.session_state.function_str,
        key="function_input",
        help="Ingresa una función matemática como sin(x), x^2, etc."
    )
    st.session_state.function_str = function_input
    if "math_expression_home" in st.session_state:
        st.session_state["math_expression_home"] = function_input
    
    # Preview the expression with LaTeX
    try:
        expr = sp.sympify(function_input.replace("^", "**"))
        st.latex(expr)
    except Exception as e:
        st.warning("La expresión ingresada no es válida. Por favor, revisa la sintaxis.")
    
    col1, col2 = st.columns(2)
    with col1:
        lower_bound = st.text_input("Límite Inferior (a)", st.session_state.lower_bound, key="lower_bound_input")
        st.session_state.lower_bound = lower_bound
    with col2:
        upper_bound = st.text_input("Límite Superior (b)", st.session_state.upper_bound, key="upper_bound_input")
        st.session_state.upper_bound = upper_bound
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Calculate button
    if st.button("Calcular Integral", key="calculate_btn"):
        try:
            # Obtener la función de entrada actual
            function_str = st.session_state.function_str
            
            # Calculate the integral
            result, steps = solve_integral(function_str, lower_bound, upper_bound)
            
            # Display solution in a styled box
            st.markdown("<div class='solution-box'>", unsafe_allow_html=True)
            st.subheader("Solución")
            
            # Plot the function and shade the area
            plot_integral(function_str, lower_bound, upper_bound)
            
            # Display solution
            display_solution(function_str, lower_bound, upper_bound, result, steps)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error al calcular la integral: {str(e)}")
    
    # Examples section
    with st.expander("Ejemplos de Integrales"):
        st.markdown("""
        ### Prueba estos ejemplos:
        
        1. $\\int_{0}^{1} x^2 \\, dx = \\frac{1}{3}$
        2. $\\int_{0}^{\\pi} \\sin(x) \\, dx = 2$
        3. $\\int_{1}^{e} \\ln(x) \\, dx = 1$
        4. $\\int_{0}^{1} e^x \\, dx = e - 1$
        5. $\\int_{-1}^{1} \\sqrt{1-x^2} \\, dx = \\frac{\\pi}{2}$
        
        Haz clic en un ejemplo para probarlo.
        """)
        
        col1, col2 = st.columns(2)
        
        if col1.button("Ejemplo 1: $\\int_{0}^{1} x^2 \\, dx$", key="example1"):
            st.session_state.function_str = "x^2"
            st.session_state.lower_bound = "0"
            st.session_state.upper_bound = "1"
            st.session_state.math_expression = "x^2"
            st.rerun()
            
        if col2.button("Ejemplo 2: $\\int_{0}^{\\pi} \\sin(x) \\, dx$", key="example2"):
            st.session_state.function_str = "sin(x)"
            st.session_state.lower_bound = "0"
            st.session_state.upper_bound = "pi"
            st.session_state.math_expression = "sin(x)"
            st.rerun()
            
        if col1.button("Ejemplo 3: $\\int_{1}^{e} \\ln(x) \\, dx$", key="example3"):
            st.session_state.function_str = "log(x)"
            st.session_state.lower_bound = "1"
            st.session_state.upper_bound = "e"
            st.session_state.math_expression = "log(x)"
            st.rerun()
            
        if col2.button("Ejemplo 4: $\\int_{0}^{1} e^x \\, dx$", key="example4"):
            st.session_state.function_str = "exp(x)"
            st.session_state.lower_bound = "0"
            st.session_state.upper_bound = "1"
            st.session_state.math_expression = "exp(x)"
            st.rerun()
            
        if col1.button("Ejemplo 5: $\\int_{-1}^{1} \\sqrt{1-x^2} \\, dx$", key="example5"):
            st.session_state.function_str = "sqrt(1-x^2)"
            st.session_state.lower_bound = "-1"
            st.session_state.upper_bound = "1"
            st.session_state.math_expression = "sqrt(1-x^2)"
            st.rerun()

# Load other pages based on mode selection
elif app_mode == "Integrales Definidas":
    import pages.definite_integrals
    pages.definite_integrals.show()
    
elif app_mode == "Sumas de Riemann":
    import pages.riemann_sums
    pages.riemann_sums.show()
    
elif app_mode == "Área Entre Curvas":
    import pages.area_between_curves
    pages.area_between_curves.show()
    
elif app_mode == "Aplicaciones de Ingeniería":
    import pages.applications
    pages.applications.show()
    
elif app_mode == "Escenarios de Ingeniería de Software":
    import pages.software_engineering_scenarios
    pages.software_engineering_scenarios.show()

# Footer - Hidden by CSS but keeping for accessibility
st.markdown("---")
st.markdown("© 2025 CalcuMaster - Calculadora de Cálculo Integral")