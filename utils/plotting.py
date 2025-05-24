import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import sympy as sp
import streamlit as st
from sympy import symbols, sympify, lambdify
from utils.calculator import parse_expression

def plot_function(func_str, x_range=(-10, 10), var_str="x", title=None, color='blue'):
    """
    Plot a function using Plotly.
    
    Args:
        func_str (str): String representation of the function
        x_range (tuple): Range for x-axis as (min, max)
        var_str (str): Variable name
        title (str): Plot title
        color (str): Line color
    
    Returns:
        plotly.graph_objects.Figure: Plotly figure object
    """
    try:
        # Parse the function
        expr = parse_expression(func_str, var_str)
        var = symbols(var_str)
        
        # Create a numeric function using lambdify
        f = lambdify(var, expr, "numpy")
        
        # Generate x values
        x_min, x_max = x_range
        x = np.linspace(x_min, x_max, 1000)
        
        # Calculate y values safely
        y = np.zeros_like(x)
        for i, x_val in enumerate(x):
            try:
                y_val = f(x_val)
                if np.isfinite(y_val) and not np.isnan(y_val):
                    y[i] = y_val
            except:
                pass  # Skip points where evaluation fails
        
        # Create plot
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name=func_str, line=dict(color=color)))
        
        # Add title and labels
        if title:
            fig.update_layout(title=title)
        else:
            fig.update_layout(title=f"Graph of f({var_str}) = {func_str}")
            
        fig.update_layout(
            xaxis_title=var_str,
            yaxis_title=f"f({var_str})",
            autosize=True,
            margin=dict(l=0, r=0, t=40, b=0),
            plot_bgcolor='rgba(240,242,246,0.8)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(
                showgrid=True,
                gridcolor='rgba(200,200,200,0.8)',
                zeroline=True,
                zerolinecolor='rgba(0,0,0,0.5)',
                zerolinewidth=1.5
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='rgba(200,200,200,0.8)',
                zeroline=True,
                zerolinecolor='rgba(0,0,0,0.5)',
                zerolinewidth=1.5
            )
        )
        
        return fig
    
    except Exception as e:
        st.error(f"Error plotting function: {str(e)}")
        # Return empty figure
        fig = go.Figure()
        fig.update_layout(
            title="Error plotting function",
            annotations=[dict(
                text=f"Error: {str(e)}",
                showarrow=False,
                xref="paper",
                yref="paper",
                x=0.5,
                y=0.5
            )]
        )
        return fig

def plot_integral(func_str, lower_bound_str, upper_bound_str, var_str="x"):
    """
    Plot a function and shade the area under the curve for a definite integral.
    
    Args:
        func_str (str): String representation of the function
        lower_bound_str (str): Lower bound of integration
        upper_bound_str (str): Upper bound of integration
        var_str (str): Variable name
    
    Returns:
        None: Displays the plot using Streamlit
    """
    try:
        # Parse the function
        expr = parse_expression(func_str, var_str)
        var = symbols(var_str)
        
        # Convert bounds to float
        lower_bound = float(lower_bound_str)
        upper_bound = float(upper_bound_str)
        
        # Create a numeric function using lambdify
        f = lambdify(var, expr, "numpy")
        
        # Generate x values
        x_range = (min(lower_bound, upper_bound) - 1, max(lower_bound, upper_bound) + 1)
        x = np.linspace(x_range[0], x_range[1], 1000)
        
        # Calculate y values
        y = np.array([float(f(x_val)) for x_val in x])
        
        # Create plot
        fig = go.Figure()
        
        # Add function curve
        fig.add_trace(go.Scatter(
            x=x, 
            y=y, 
            mode='lines', 
            name=func_str,
            line=dict(color='blue', width=2)
        ))
        
        # Add filled area for the integral
        x_fill = np.linspace(lower_bound, upper_bound, 500)
        y_fill = np.array([float(f(x_val)) for x_val in x_fill])
        
        # Create fill from function down to x-axis
        fig.add_trace(go.Scatter(
            x=x_fill,
            y=y_fill,
            fill='tozeroy',
            fillcolor='rgba(30, 136, 229, 0.3)',
            line=dict(color='rgba(0,0,0,0)'),
            name=f'Integral from {lower_bound} to {upper_bound}'
        ))
        
        # Add vertical lines at bounds
        fig.add_shape(
            type="line",
            x0=lower_bound, y0=0, x1=lower_bound, y1=f(lower_bound),
            line=dict(color="red", width=2, dash="dash"),
        )
        
        fig.add_shape(
            type="line",
            x0=upper_bound, y0=0, x1=upper_bound, y1=f(upper_bound),
            line=dict(color="red", width=2, dash="dash"),
        )
        
        # Update layout
        fig.update_layout(
            title=f"Definite Integral of f({var_str}) = {func_str} from {lower_bound} to {upper_bound}",
            xaxis_title=var_str,
            yaxis_title=f"f({var_str})",
            autosize=True,
            margin=dict(l=0, r=0, t=40, b=0),
            plot_bgcolor='rgba(240,242,246,0.8)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(
                showgrid=True,
                gridcolor='rgba(200,200,200,0.8)',
                zeroline=True,
                zerolinecolor='rgba(0,0,0,0.5)',
                zerolinewidth=1.5
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='rgba(200,200,200,0.8)',
                zeroline=True,
                zerolinecolor='rgba(0,0,0,0.5)',
                zerolinewidth=1.5
            ),
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            )
        )
        
        # Display the plot in Streamlit
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error plotting integral: {str(e)}")

def plot_area_between_curves(func1_str, func2_str, lower_bound, upper_bound, var_str="x"):
    """
    Plot two functions and shade the area between them.
    
    Args:
        func1_str (str): String representation of the first function
        func2_str (str): String representation of the second function
        lower_bound (float): Lower bound of the interval
        upper_bound (float): Upper bound of the interval
        var_str (str): Variable name
    
    Returns:
        None: Displays the plot using Streamlit
    """
    try:
        # Parse the functions
        expr1 = parse_expression(func1_str, var_str)
        expr2 = parse_expression(func2_str, var_str)
        var = symbols(var_str)
        
        # Create numeric functions using lambdify
        f1 = lambdify(var, expr1, "numpy")
        f2 = lambdify(var, expr2, "numpy")
        
        # Generate x values
        x_range = (min(lower_bound, upper_bound) - 1, max(lower_bound, upper_bound) + 1)
        x = np.linspace(x_range[0], x_range[1], 1000)
        
        # Calculate y values
        y1 = np.array([float(f1(x_val)) for x_val in x])
        y2 = np.array([float(f2(x_val)) for x_val in x])
        
        # Create plot
        fig = go.Figure()
        
        # Add function curves
        fig.add_trace(go.Scatter(
            x=x, 
            y=y1, 
            mode='lines', 
            name=func1_str,
            line=dict(color='blue', width=2)
        ))
        
        fig.add_trace(go.Scatter(
            x=x, 
            y=y2, 
            mode='lines', 
            name=func2_str,
            line=dict(color='green', width=2)
        ))
        
        # Add filled area between curves
        x_fill = np.linspace(lower_bound, upper_bound, 500)
        y1_fill = np.array([float(f1(x_val)) for x_val in x_fill])
        y2_fill = np.array([float(f2(x_val)) for x_val in x_fill])
        
        # Add top curve
        fig.add_trace(go.Scatter(
            x=x_fill,
            y=y1_fill,
            mode='lines',
            line=dict(width=0),
            showlegend=False
        ))
        
        # Add bottom curve and fill
        fig.add_trace(go.Scatter(
            x=x_fill,
            y=y2_fill,
            mode='lines',
            line=dict(width=0),
            fill='tonexty',
            fillcolor='rgba(30, 136, 229, 0.3)',
            name=f'Area between curves'
        ))
        
        # Add vertical lines at bounds
        fig.add_shape(
            type="line",
            x0=lower_bound, y0=min(f1(lower_bound), f2(lower_bound)), 
            x1=lower_bound, y1=max(f1(lower_bound), f2(lower_bound)),
            line=dict(color="red", width=2, dash="dash"),
        )
        
        fig.add_shape(
            type="line",
            x0=upper_bound, y0=min(f1(upper_bound), f2(upper_bound)), 
            x1=upper_bound, y1=max(f1(upper_bound), f2(upper_bound)),
            line=dict(color="red", width=2, dash="dash"),
        )
        
        # Update layout
        fig.update_layout(
            title=f"Area Between Curves: {func1_str} and {func2_str} from {lower_bound} to {upper_bound}",
            xaxis_title=var_str,
            yaxis_title=f"y",
            autosize=True,
            margin=dict(l=0, r=0, t=40, b=0),
            plot_bgcolor='rgba(240,242,246,0.8)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(
                showgrid=True,
                gridcolor='rgba(200,200,200,0.8)',
                zeroline=True,
                zerolinecolor='rgba(0,0,0,0.5)',
                zerolinewidth=1.5
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='rgba(200,200,200,0.8)',
                zeroline=True,
                zerolinecolor='rgba(0,0,0,0.5)',
                zerolinewidth=1.5
            ),
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            )
        )
        
        # Display the plot in Streamlit
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error plotting area between curves: {str(e)}")

def plot_riemann_sum(func_str, lower_bound, upper_bound, n, method='left', var_str="x"):
    """
    Plot a function with Riemann sum rectangles.
    
    Args:
        func_str (str): String representation of the function
        lower_bound (float): Lower bound of the interval
        upper_bound (float): Upper bound of the interval
        n (int): Number of subdivisions
        method (str): Method for selecting sample points ('left', 'right', 'midpoint')
        var_str (str): Variable name
    
    Returns:
        None: Displays the plot using Streamlit
    """
    try:
        # Parse the function
        expr = parse_expression(func_str, var_str)
        var = symbols(var_str)
        
        # Create a numeric function using lambdify
        f = lambdify(var, expr, "numpy")
        
        # Generate x values for the function curve
        x_range = (min(lower_bound, upper_bound) - 1, max(lower_bound, upper_bound) + 1)
        x_curve = np.linspace(x_range[0], x_range[1], 1000)
        
        # Calculate y values for the function curve
        y_curve = np.array([float(f(x_val)) for x_val in x_curve])
        
        # Calculate Riemann sum rectangles
        width = (upper_bound - lower_bound) / n
        rectangles = []
        
        for i in range(n):
            x_left = lower_bound + i * width
            x_right = lower_bound + (i + 1) * width
            
            if method == 'left':
                sample_point = x_left
            elif method == 'right':
                sample_point = x_right
            elif method == 'midpoint':
                sample_point = (x_left + x_right) / 2
            else:
                raise ValueError(f"Unknown method: {method}")
            
            height = f(sample_point)
            
            # Rectangle vertices
            rectangles.append({
                'x': [x_left, x_right, x_right, x_left, x_left],
                'y': [0, 0, height, height, 0],
                'height': height
            })
        
        # Create plot
        fig = go.Figure()
        
        # Add rectangles
        for i, rect in enumerate(rectangles):
            fig.add_trace(go.Scatter(
                x=rect['x'],
                y=rect['y'],
                fill="toself",
                fillcolor=f'rgba(30, 136, 229, 0.4)',
                line=dict(color='rgba(30, 136, 229, 0.8)'),
                name=f'Rectangle {i+1} (h={rect["height"]:.4f})',
                showlegend=False
            ))
        
        # Add function curve
        fig.add_trace(go.Scatter(
            x=x_curve, 
            y=y_curve, 
            mode='lines', 
            name=func_str,
            line=dict(color='blue', width=2)
        ))
        
        # Calculate the Riemann sum
        riemann_sum = sum(rect['height'] * width for rect in rectangles)
        
        # Update layout
        fig.update_layout(
            title=f"Riemann Sum ({method}) of f({var_str}) = {func_str} with {n} subdivisions<br>Sum = {riemann_sum:.6f}",
            xaxis_title=var_str,
            yaxis_title=f"f({var_str})",
            autosize=True,
            margin=dict(l=0, r=0, t=60, b=0),
            plot_bgcolor='rgba(240,242,246,0.8)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(
                showgrid=True,
                gridcolor='rgba(200,200,200,0.8)',
                zeroline=True,
                zerolinecolor='rgba(0,0,0,0.5)',
                zerolinewidth=1.5
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='rgba(200,200,200,0.8)',
                zeroline=True,
                zerolinecolor='rgba(0,0,0,0.5)',
                zerolinewidth=1.5
            ),
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            )
        )
        
        # Display the plot in Streamlit
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error plotting Riemann sum: {str(e)}")
