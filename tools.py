import numpy as np
import matplotlib.pyplot as plt

def plot_linear_equation(m, b, min_x=-10, max_x=10):
    """
    Plots the line y = mx + b and shows the graph with labels.

    Parameters:
    - m (float): The slope of the line.
    - b (float): The y-intercept of the line.
    - min_x (float): The minimum x value to plot. Default is -10.
    - max_x (float): The maximum x value to plot. Default is 10.
    """
    x_range=(min_x, max_x)
    # Generate x values in the given range
    x = np.linspace(x_range[0], x_range[1], 400)
    
    # Calculate the corresponding y values based on the equation y = mx + b
    y = m * x + b
    
    # Create the plot
    plt.figure(figsize=(6, 4))
    plt.plot(x, y, label=f'y = {m}x + {b}', color='b')
    
    # Labeling the axes
    plt.xlabel('x')
    plt.ylabel('y')
    
    # Add a title
    plt.title(f'Plot of y = {m}x + {b}')
    
    # Show a grid
    plt.grid(True)
    
    # Add a legend
    plt.legend()
    
    # Show the plot
    plt.show()

