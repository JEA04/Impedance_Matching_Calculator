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
        self.normalized_values = [0.2, 0.5, 1, 2, 5, 10]
        self.impedance_color = 'red'
        self.admittance_color = 'blue'

        # Initialize Smith Chart
        self.fig = plt.figure(figsize=(10, 10))
        self.ax = self.fig.add_subplot()
        self.ax.axis('off')
        self.ax.set_ylim(-1.25, 1.25)
        self.ax.set_xlim(-1.25, 1.25)
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
        self.smith_circle = Circle((0, 0), 1, fc='none', ec='black')
        self.ax.add_patch(self.smith_circle)

        # Draw Horizontal Line
        line = FancyArrowPatch((-1, 0), (1, 0))
        self.ax.add_patch(line)

    def draw_impedance_circle(self):
        for constant_real in self.normalized_values:
            # Draw Constant Real Impedance Circles
            center = (constant_real / (constant_real + 1), 0)
            radius = 1 / (constant_real + 1)
            circle = Circle(center, radius, fc='none', ec=self.impedance_color)
            self.ax.add_patch(circle)

            # Constant imaginary Impedance Circles
            i_center = (1, 1/constant_real)
            i_center_n = (1, -1/constant_real)
            i_radius = 1/constant_real
            circle = Circle(i_center, i_radius, fc='none', ec=self.impedance_color)
            circle.set_clip_path(self.smith_circle)
            neg_const = Circle(i_center_n, i_radius, fc='none', ec=self.impedance_color)
            neg_const.set_clip_path(self.smith_circle)
            self.ax.add_patch(circle)
            self.ax.add_patch(neg_const)

    def draw_admittance_circle(self):
        for constant_real in self.normalized_values:
            # Draw Constant Real Admittance Circles
            center = (- (constant_real/ (constant_real + 1)), 0)
            print(center)
            radius = 1 / (constant_real + 1)
            circle = Circle(center, radius, fc='none', ec=self.admittance_color)
            self.ax.add_patch(circle)

            # Draw Constant Imaginary Admittance Circles
            # Constant imaginary Impedance Circles
            i_center = (-1, 1 / constant_real)
            i_center_n = (-1, -1 / constant_real)
            i_radius = 1 / constant_real
            circle = Circle(i_center, i_radius, fc='none', ec=self.admittance_color)
            circle.set_clip_path(self.smith_circle)
            neg_const = Circle(i_center_n, i_radius, fc='none', ec=self.admittance_color)
            neg_const.set_clip_path(self.smith_circle)
            self.ax.add_patch(circle)
            self.ax.add_patch(neg_const)

    def add_text(self):
        # Add Normalizing Impedance Text Box
        z0_text = f"$Z_0:$ {self.z0}"
        z0_box = Rectangle(xy=(1, 1), width=0.2, height=0.1, ec='black', fc='none')
        self.ax.add_patch(z0_box)
        rx, ry = z0_box.get_xy()
        tx = rx + z0_box.get_width() / 2.0
        ty = ry + z0_box.get_height() / 2.0
        self.ax.annotate(z0_text, (tx, ty), color='black', fontsize=self.text_size, ha='center', va='center')

        # Add Start Impedance
        start_impedance = complex(120)
        start = f"$Z_{{start}}:${start_impedance}Ω"
        self.ax.annotate(start, (-1, -1), color='red', fontsize=self.text_size)

        # Add Target Impedance Text
        target_impedance = complex(60, 0)
        target = f"$Z_{{target}}:${target_impedance}Ω"
        self.ax.annotate(target, (1, -1), color='green', fontsize=self.text_size)

        # Add Component Values


if __name__ == '__main__':
    sc = SmithChart()
    sc.show()
