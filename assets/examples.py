# Riemann sum examples from the provided document
riemann_sum_examples = {
    "Example 1: x² + 3x + 2 on [2, 4]": {
        "function": "x^2 + 3*x + 2",
        "lower_bound": 2,
        "upper_bound": 4,
        "subdivisions": 6,
        "method": "left"
    },
    "Example 2: x² + 2x on [0, 3]": {
        "function": "x^2 + 2*x",
        "lower_bound": 0,
        "upper_bound": 3,
        "subdivisions": 6,
        "method": "left"
    },
    "Example 3: e^x + 1 on [0, 4]": {
        "function": "exp(x) + 1",
        "lower_bound": 0,
        "upper_bound": 4,
        "subdivisions": 4,
        "method": "midpoint"
    },
    "Example 4: cos(x) on [0, 3π/2]": {
        "function": "cos(x)",
        "lower_bound": 0,
        "upper_bound": 3*sp.pi/2,
        "subdivisions": 6,
        "method": "right"
    },
    "Example 5: 2x² + 3x - 2 on [0, 3]": {
        "function": "2*x^2 + 3*x - 2",
        "lower_bound": 0,
        "upper_bound": 3,
        "subdivisions": 6,
        "method": "left"
    },
    "Example 6: 3 + (1/2)x on [-1, 7]": {
        "function": "3 + (1/2)*x",
        "lower_bound": -1,
        "upper_bound": 7,
        "subdivisions": 6,
        "method": "left"
    },
    "Example 7: sin(x) + cos(x) on [π/2, 3π/2]": {
        "function": "sin(x) + cos(x)",
        "lower_bound": sp.pi/2,
        "upper_bound": 3*sp.pi/2,
        "subdivisions": 6,
        "method": "right"
    },
    "Example 8: 2x³ - 3x² + 2 on [0, 4]": {
        "function": "2*x^3 - 3*x^2 + 2",
        "lower_bound": 0,
        "upper_bound": 4,
        "subdivisions": 6,
        "method": "left"
    },
    "Example 9: e^x + 2 on [2, 4]": {
        "function": "exp(x) + 2",
        "lower_bound": 2,
        "upper_bound": 4,
        "subdivisions": 4,
        "method": "midpoint"
    },
    "Example 10: (x-2)³ + (x-2)² + 1 on [0, 6]": {
        "function": "(x-2)^3 + (x-2)^2 + 1",
        "lower_bound": 0,
        "upper_bound": 6,
        "subdivisions": 6,
        "method": "left"
    }
}

# Definite integral examples
definite_integral_examples = {
    "Area under sin(x) and cos(x)": {
        "function": "sin(x)",
        "lower_bound": 0,
        "upper_bound": "pi",
        "variable": "x"
    },
    "Area under 2x² + 3x - 2": {
        "function": "2*x^2 + 3*x - 2",
        "lower_bound": 0,
        "upper_bound": 3,
        "variable": "x"
    },
    "Area under 5 - 2t²": {
        "function": "5 - 2*t^2",
        "lower_bound": 0,
        "upper_bound": 5,
        "variable": "t"
    },
    "Server resource usage: 50e^(-0.2t)": {
        "function": "50*exp(-0.2*t)",
        "lower_bound": 0,
        "upper_bound": 30,
        "variable": "t"
    },
    "Algorithm time complexity: 3n² + 2n + 1": {
        "function": "3*n^2 + 2*n + 1",
        "lower_bound": 1,
        "upper_bound": 10,
        "variable": "n"
    }
}

# Area between curves examples
area_between_curves_examples = {
    "Sin and Cos intersection": {
        "function1": "sin(x)",
        "function2": "cos(x)",
        "lower_bound": 0,
        "upper_bound": "pi/4",
        "description": "The sine and cosine curves intersect infinitely many times, creating regions of equal areas."
    },
    "Database optimization (Example 2)": {
        "function1": "3 + y^2",
        "function2": "y + 1",
        "lower_bound": 0,
        "upper_bound": 2,
        "description": "The optimization in database queries is measured by the convergence of speed (3 + y²) and precision (y + 1)."
    },
    "Server resource consumption (Example 3)": {
        "function1": "(t + 4)^2 + 2*(t + 4) + 1",
        "function2": "-t + 5",
        "lower_bound": 0,
        "upper_bound": 5,
        "description": "A server's memory usage M(t) = (t + 4)² + 2(t + 4) + 1 and CPU usage C(t) = -t + 5 during data loading."
    },
    "Database optimization (Example 6)": {
        "function1": "sqrt(3 - x)",
        "function2": "x - 1",
        "lower_bound": 0,
        "upper_bound": 1,
        "description": "The optimization in database queries is measured by the convergence of speed (√(3-x)) and precision (x-1)."
    },
    "Server memory and CPU usage (Example 9)": {
        "function1": "t^2 + 2*t + 1",
        "function2": "2*t + 5",
        "lower_bound": 0,
        "upper_bound": 3,
        "description": "A server's memory usage M(t) = t² + 2t + 1 and CPU usage C(t) = 2t + 5 during data loading."
    },
    "Database optimization (Example 10)": {
        "function1": "(x - 1)^2",
        "function2": "2*x - 4",
        "lower_bound": 1,
        "upper_bound": 2,
        "description": "The optimization in database queries is measured by the convergence of speed ((x-1)²) and precision (2x-4)."
    }
}

# Engineering applications examples
engineering_applications_examples = {
    "Server Resource Consumption": {
        "Example 1: Server Memory and CPU": {
            "description": "A server web has memory usage M(t) = t² + 2t + 1 and CPU usage C(t) = 2t + 5 during data loading, where t is time in minutes. Calculate the total resources used in the first 3 minutes.",
            "function1": "t^2 + 2*t + 1",
            "function2": "2*t + 5",
            "lower_bound": 0,
            "upper_bound": 3,
            "calculation_type": "area_between_curves"
        },
        "Example 2: Resource Decay": {
            "description": "A server's resource consumption is modeled by R(t) = 5 - 2t² MB per minute during a data loading process, where t is time in minutes. Calculate the total resources used in the first 5 minutes.",
            "function1": "5 - 2*t^2",
            "lower_bound": 0,
            "upper_bound": 5,
            "calculation_type": "definite_integral"
        }
    },
    "User Load Analysis": {
        "Example 1: Exponential Decay": {
            "description": "The user load on a system during an event is modeled by C(t) = 50e^(-0.2t), where t is time in minutes and C(t) is the number of active users. Calculate the total user interactions over the first 30 minutes.",
            "function1": "50*exp(-0.2*t)",
            "lower_bound": 0,
            "upper_bound": 30,
            "calculation_type": "definite_integral"
        },
        "Example 2: 8-Hour User Load": {
            "description": "The user load on a system is modeled by C(t) = 20e^(-0.5t), where t is time in minutes. Calculate the total accumulated users from 1 to 8 hours (60 to 480 minutes).",
            "function1": "20*exp(-0.5*t)",
            "lower_bound": 60,
            "upper_bound": 480,
            "calculation_type": "definite_integral"
        }
    },
    "Database Optimization": {
        "Example 1: Optimization Metrics": {
            "description": "Database optimization is measured by the convergence of speed (3 + y²) and precision (y + 1) in query reviews. Find the area between these functions from y = 0 to y = 2, representing the maximum optimization potential.",
            "function1": "3 + y^2",
            "function2": "y + 1",
            "lower_bound": 0,
            "upper_bound": 2,
            "calculation_type": "area_between_curves"
        },
        "Example 2: Parabolic Optimization": {
            "description": "Database optimization is measured by speed ((x-1)²) and precision (2x-4). Find the area between these functions from x = 1 to x = 2, representing the maximum optimization potential.",
            "function1": "(x-1)^2",
            "function2": "2*x-4",
            "lower_bound": 1,
            "upper_bound": 2,
            "calculation_type": "area_between_curves"
        }
    },
    "Algorithm Complexity": {
        "Example 1: Quadratic Complexity": {
            "description": "An algorithm has a time complexity T(n) = 3n² + 2n + 1 milliseconds, where n is the input size. Calculate the total execution time for processing data from n = 1 to n = 10.",
            "function1": "3*n^2 + 2*n + 1",
            "lower_bound": 1,
            "upper_bound": 10,
            "calculation_type": "definite_integral"
        }
    }
}
