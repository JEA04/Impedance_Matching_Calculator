from typing import Any

import matplotlib.pyplot as plt
import numpy
import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle
from matplotlib.lines import Line2D
from matplotlib.text import Text


class SmithChart(object):

    def __init__(self):
        self.z0 = 50
        self.text_size = 12
        self.smith_circle = None
        self.circle_values = [0.2, 0.5, 1, 2, 5, 10]
        print("Smith")

        # Initialize Smith Chart
        self.fig = plt.figure(figsize=(10, 10))
        self.ax = self.fig.add_subplot()
        self.ax.axis('off')
        self.ax.set_ylim(-0.25, 1.25)
        self.ax.set_xlim(-0.25, 1.25)
        self.draw_smith_chart()

    def show(self):
        self.fig.show()

    def draw_smith_chart(self):
        self.draw_chart()

        # Draw Additional Circles
        self.draw_admittance_circle()
        self.draw_impedance_circle()
        self.add_text()

    def draw_chart(self):
        # Draw Outline Circle
        self.smith_circle = Circle((0.5, 0.5), 0.5, fc='none', ec='black')
        self.ax.add_patch(self.smith_circle)

        # Draw Horizontal Line
        line = FancyArrowPatch((0, 0.5), (1, 0.5))
        self.ax.add_patch(line)

    def draw_impedance_circle(self):
        intersect_points = self.calculate_intersect_points()
        print(intersect_points)
        for point in intersect_points:
            radius = (1 - point) / 2
            x_center = point + (1 - point) / 2
            circle = Circle((x_center, 0.5), radius, fc='none', ec='blue')
            self.ax.add_patch(circle)

        # self.z0_circle = Circle((0.75, 0.5), 0.25, fc ='none', ec = 'blue')
        # self.ax.add_patch(self.z0_circle)

    def draw_admittance_circle(self):
        intersect_points = self.calculate_intersect_points()
        for point in reversed(intersect_points):
            radius = point / 2.0
            circle = Circle((radius, 0.5), radius, fc='none', ec='red')
            self.ax.add_patch(circle)

    def calculate_intersect_points(self):
        bigger = []
        smaller = []
        for value in self.circle_values:
            if value > 1:
                bigger.append(value)
            elif value < 1:
                smaller.append(value)
        # Calculate intersect points for values smaller than 1
        step = 0.5 / (len(smaller) + 1)
        smaller_points = [i * step for i in range(1, len(smaller) + 1)]

        # Calculate intersect points for values bigger than 1
        step = 0.5 / (len(bigger) + 1)
        bigger_points = [i * step + 0.5 for i in range(1, len(bigger) + 1)]
        return smaller_points + [0.5] + bigger_points

    def calculate_circle_intersect_points(self):
        radius = np.pi

    def add_text(self):
        # Add Normalizing Impedance Text Box
        z0_text = f"$Z_0:$ {self.z0}"
        z0_box = Rectangle(xy=(0.85, 0.9), width=0.2, height=0.1, ec='black', fc='none')
        self.ax.add_patch(z0_box)
        rx, ry = z0_box.get_xy()
        tx = rx + z0_box.get_width() / 2.0
        ty = ry + z0_box.get_height() / 2.0
        self.ax.annotate(z0_text, (tx, ty), color='black', fontsize=self.text_size, ha='center', va='center')

        # Add Start Impedance
        start_impedance = complex(120)
        start = f"$Z_{{start}}:${start_impedance}Ω"
        self.ax.annotate(start, (0, 0), color='red', fontsize=self.text_size)

        # Add Target Impedance Text
        target_impedance = complex(60, 0)
        target = f"$Z_{{target}}:${target_impedance}Ω"
        self.ax.annotate(target, (0.75, 0), color='green', fontsize=self.text_size)

        # Add Component Values


if __name__ == '__main__':
    print("Hello World")
    sc = SmithChart()
    sc.show()
