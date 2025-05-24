# Manual de Uso - Calculadora de Cálculo Integral

## Introducción

Bienvenido a la Calculadora de Cálculo Integral, una aplicación interactiva que te permite resolver y visualizar problemas de cálculo integral. Esta herramienta es ideal para estudiantes y profesionales que necesitan realizar cálculos de integrales definidas, sumas de Riemann, áreas entre curvas y aplicaciones en ingeniería de software.

## Cómo Ingresar Expresiones Matemáticas

Para ingresar expresiones matemáticas correctamente, sigue estas pautas:

### Operadores Básicos
- Suma: `+` (ejemplo: `x + 2`)
- Resta: `-` (ejemplo: `x - 2`)
- Multiplicación: `*` (ejemplo: `2*x` o `2x`)
- División: `/` (ejemplo: `x/2`)
- Potencia: `^` (ejemplo: `x^2`)

### Funciones Comunes
- Funciones trigonométricas: `sin(x)`, `cos(x)`, `tan(x)`
- Logaritmos: `log(x)` (logaritmo natural), `log10(x)` (logaritmo base 10)
- Exponencial: `exp(x)` o `e^x`
- Raíz cuadrada: `sqrt(x)`
- Valor absoluto: `abs(x)`

### Constantes
- Pi: `pi`
- Número de Euler: `e`
- Infinito: `oo`

### Integrales

Para ingresar una integral, usa el símbolo `∫`:
- Ejemplo 1: `∫(x^2)` representa ∫x² dx
- Ejemplo 2: `∫(cos(2*x))` representa ∫cos(2x) dx

O puedes usar la forma tradicional:
- `integrate(x^2)` representa ∫x² dx

## Secciones de la Aplicación

### 1. Inicio
La página principal te permite calcular integrales definidas rápidamente. Ingresa una función, los límites inferior y superior, y haz clic en "Calcular Integral".

**Ejemplo**: Para calcular ∫cos(2x)dx desde 0 hasta π:
- Función: `cos(2*x)`
- Límite inferior: `0`
- Límite superior: `pi`

### 2. Integrales Definidas
Esta sección te permite explorar integrales definidas con más detalle, mostrando paso a paso la solución.

### 3. Sumas de Riemann
Aquí puedes aproximar integrales usando sumas de Riemann con diferentes métodos (izquierda, derecha, punto medio). Puedes ajustar el número de subdivisiones para ver cómo afecta a la precisión.

### 4. Área Entre Curvas
Calcula el área encerrada entre dos curvas en un intervalo específico. Ingresa dos funciones y los límites del intervalo.

**Ejemplo**: Para encontrar el área entre y=x² y y=x desde x=0 hasta x=1:
- Primera función: `x^2`
- Segunda función: `x`
- Límite inferior: `0`
- Límite superior: `1`

### 5. Aplicaciones en Ingeniería
Explora aplicaciones prácticas del cálculo integral en la ingeniería, especialmente en contextos de ingeniería de software.

### 6. Escenarios de Ingeniería de Software
Genera automáticamente problemas de cálculo integral relacionados con escenarios reales de ingeniería de software, como consumo de recursos, optimización de bases de datos, análisis de rendimiento de algoritmos, etc.

## Consejos para Usar la Aplicación

1. **Sintaxis correcta**: Asegúrate de usar paréntesis para agrupar correctamente las operaciones, como en `sin(x^2)` en lugar de `sin x^2`.

2. **Visualización de ecuaciones**: La aplicación muestra una vista previa en LaTeX de tu expresión, lo que te ayuda a verificar que la has ingresado correctamente.

3. **Formato para ecuaciones como ∫cos(2x)dx**:
   - Forma recomendada: `∫(cos(2*x))`
   - También válido: `integrate(cos(2*x))`

4. **Multiplicación explícita**: Siempre usa el operador `*` para multiplicación, especialmente con variables. Escribe `2*x` en lugar de solo `2x` para evitar errores.

5. **Potencias**: Usa `^` para potencias, como en `x^2` para x².

## Ejemplos de Expresiones

| Expresión matemática | Cómo ingresarla |
|----------------------|-----------------|
| ∫x² dx               | `∫(x^2)` o `integrate(x^2)` |
| ∫cos(2x) dx          | `∫(cos(2*x))` o `integrate(cos(2*x))` |
| ∫e^x dx              | `∫(exp(x))` o `∫(e^x)` |
| ∫ln(x) dx            | `∫(log(x))` |
| ∫√(1-x²) dx          | `∫(sqrt(1-x^2))` |

## Resolución de Problemas

- Si recibes un error al calcular, verifica que tu expresión esté sintácticamente correcta y que uses los operadores adecuados.
- Para expresiones con raíces, usa `sqrt()` en lugar de `√` directamente.
- Si estás trabajando con límites de integración que contienen expresiones, asegúrate de que estén bien formateadas (por ejemplo, usa `pi/4` en lugar de `π/4`).

---

¡Disfruta utilizando la Calculadora de Cálculo Integral para tus estudios y proyectos!