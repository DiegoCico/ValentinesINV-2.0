import tkinter as tk
import math
import random

def draw_better_heart(canvas, x, y, size, tag="heart", fill_color="red", outline_color="darkred"):
    """
    Draws a heart shape on the given canvas using a parametric equation.
    
    :param canvas: The tkinter canvas on which to draw.
    :param x: The x-coordinate of the heart's center.
    :param y: The y-coordinate of the heart's center.
    :param size: The scaling factor for the heart.
    :param tag: The tag assigned to the drawn heart.
    :param fill_color: The fill color of the heart.
    :param outline_color: The outline color of the heart.
    """
    points = []
    for t in range(0, 360, 5):
        rad = math.radians(t)
        x_val = 16 * (math.sin(rad) ** 3)
        y_val = 13 * math.cos(rad) - 5 * math.cos(2 * rad) - 2 * math.cos(3 * rad) - math.cos(4 * rad)
        x_scaled = x + x_val * size / 50.0
        y_scaled = y - y_val * size / 50.0
        points.append((x_scaled, y_scaled))
    flat_points = [coord for point in points for coord in point]
    canvas.create_polygon(flat_points, fill=fill_color, outline=outline_color, tags=tag)

def start_bouncing_hearts(canvas):
    """
    Animates multiple small hearts that move randomly and bounce off the canvas edges.
    
    :param canvas: The tkinter canvas on which to animate the hearts.
    """
    hearts = []
    colors = ["pink", "lightblue", "lightgreen", "yellow", "orange", "purple"]
    width = int(canvas['width'])
    height = int(canvas['height'])
    for _ in range(20):
        heart = {
            "x": random.randint(0, width),
            "y": random.randint(0, height),
            "vx": random.choice([-3, -2, -1, 1, 2, 3]),
            "vy": random.choice([-3, -2, -1, 1, 2, 3]),
            "size": random.randint(10, 30),
            "color": random.choice(colors)
        }
        hearts.append(heart)

    def animate_hearts():
        canvas.delete("bg_heart")
        for heart in hearts:
            heart['x'] += heart['vx']
            heart['y'] += heart['vy']
            if heart['x'] <= 0 or heart['x'] >= width:
                heart['vx'] *= -1
            if heart['y'] <= 0 or heart['y'] >= height:
                heart['vy'] *= -1
            draw_better_heart(canvas, heart['x'], heart['y'], heart['size'],
                              tag="bg_heart", fill_color=heart['color'], outline_color="")
        canvas.after(50, animate_hearts)
    animate_hearts()

def start_pulsing_heart(canvas):
    """
    Animates a large heart in the center of the canvas that scales up and down (beats).
    
    :param canvas: The tkinter canvas on which to animate the pulsing heart.
    """
    scale = 1.0
    scale_direction = 0.02
    width = int(canvas['width'])
    height = int(canvas['height'])
    
    def animate():
        nonlocal scale, scale_direction
        canvas.delete("pulsing_heart")
        new_size = 100 * scale
        draw_better_heart(canvas, width/2, height/2, new_size, tag="pulsing_heart", fill_color="red", outline_color="darkred")
        scale += scale_direction
        if scale > 1.2 or scale < 0.8:
            scale_direction *= -1
        canvas.after(50, animate)
    
    animate()
