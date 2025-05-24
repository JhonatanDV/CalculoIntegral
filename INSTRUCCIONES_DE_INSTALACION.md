# Instrucciones de Instalación y Ejecución

## Requisitos del Sistema

Para ejecutar esta aplicación de cálculo integral, necesitarás tener instalado:

1. Python 3.9 o superior
2. pip (el gestor de paquetes de Python)

## Instalación

Sigue estos pasos para instalar y ejecutar la aplicación en tu sistema local:

### 1. Clona o descarga el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd <NOMBRE_DEL_DIRECTORIO>
```

### 2. Crea un entorno virtual (opcional pero recomendado)

En Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

En macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instala las dependencias

```bash
pip install -r requirements.txt
```

O instala las dependencias manualmente:
```bash
pip install streamlit matplotlib numpy plotly sympy
```

## Ejecución de la Aplicación

Para ejecutar la aplicación, utiliza el siguiente comando:

```bash
streamlit run app.py
```

Esto iniciará el servidor de Streamlit y abrirá automáticamente la aplicación en tu navegador web predeterminado. Si no se abre automáticamente, puedes acceder a ella a través de:

```
http://localhost:5000
```

## Comandos útiles

- Para detener la aplicación: presiona `Ctrl+C` en la terminal donde se está ejecutando.
- Para reiniciar la aplicación: vuelve a ejecutar el comando `streamlit run app.py`.
- Para actualizar las dependencias si has realizado cambios: `pip install -r requirements.txt --upgrade`.

## Solución de problemas

1. **Error de importación de módulos**: Asegúrate de que estás ejecutando la aplicación desde el directorio raíz del proyecto.

2. **Error de instalación de dependencias**: Intenta instalar cada dependencia por separado si el archivo requirements.txt falla.

3. **La aplicación no muestra gráficos**: Asegúrate de tener instaladas las bibliotecas matplotlib y plotly correctamente.

4. **Error al procesar expresiones matemáticas**: Verifica la sintaxis de las expresiones de acuerdo con el manual de usuario.

## Notas adicionales

- La aplicación está optimizada para funcionar en navegadores modernos como Chrome, Firefox o Edge.
- Para una mejor experiencia, utiliza una pantalla con resolución de al menos 1366x768 pixeles.
- Las imágenes y archivos estáticos se almacenan en el directorio `assets/`.