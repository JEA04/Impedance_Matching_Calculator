from typing import Any

import matplotlib.pyplot as plt
import numpy
import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle
from matplotlib.lines import Line2D


class SmithChart(object):

    def __init__(self, ax):
        # Class Parameters
        self.ax = ax
        self.z0 = 50
        self.text_size = 12
        self.smith_circle = None
        self.normalized_values = [0.2, 0.5, 1, 2, 5, 10]
        self.impedance_color = 'red'
        self.admittance_color = 'blue'
        self.line_style = ':'
        self.z0_text = None
        self.z_start_text = None
        self.z_target_text = None

        # Initialize Smith Chart
        self.ax.axis('off')
        self.ax.axis(np.array([-1, 1, -1, 1]))
        self.draw_smith_chart()

    def draw_smith_chart(self):
        self.draw_chart()

        # Draw Additional Circles
        self.draw_admittance_circle()
        self.draw_impedance_circle()
        self.set_z0_text()

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
            circle = Circle(center, radius, fc='none', ec=self.impedance_color, ls=self.line_style)
            self.ax.add_patch(circle)

            # Constant imaginary Impedance Circles
            i_center = (1, 1/constant_real)
            i_center_n = (1, -1/constant_real)
            i_radius = 1/constant_real
            circle = Circle(i_center, i_radius, fc='none', ec=self.impedance_color, ls=self.line_style)
            circle.set_clip_path(self.smith_circle)
            neg_const = Circle(i_center_n, i_radius, fc='none', ec=self.impedance_color, ls=self.line_style)
            neg_const.set_clip_path(self.smith_circle)
            self.ax.add_patch(circle)
            self.ax.add_patch(neg_const)

    def draw_admittance_circle(self):
        for constant_real in self.normalized_values:
            # Draw Constant Real Admittance Circles
            center = (- (constant_real / (constant_real + 1)), 0)
            radius = 1 / (constant_real + 1)
            circle = Circle(center, radius, fc='none', ec=self.admittance_color, ls=self.line_style)
            self.ax.add_patch(circle)

            # Draw Constant Imaginary Admittance Circles
            # Constant imaginary Impedance Circles
            i_center = (-1, 1 / constant_real)
            i_center_n = (-1, -1 / constant_real)
            i_radius = 1 / constant_real
            circle = Circle(i_center, i_radius, fc='none', ec=self.admittance_color, ls=self.line_style)
            circle.set_clip_path(self.smith_circle)
            neg_const = Circle(i_center_n, i_radius, fc='none', ec=self.admittance_color, ls=self.line_style)
            neg_const.set_clip_path(self.smith_circle)
            self.ax.add_patch(circle)
            self.ax.add_patch(neg_const)

    def set_z0_text(self):
        z0_text = f"$Z_0:$ {self.z0}"
        z0_box = Rectangle(xy=(0.75, 0.8), width=0.2, height=0.1, ec='black', fc='none')
        self.ax.add_patch(z0_box)
        rx, ry = z0_box.get_xy()
        tx = rx + z0_box.get_width() / 2.0
        ty = ry + z0_box.get_height() / 2.0
        self.z0_text = self.ax.annotate(z0_text, (tx, ty), color='black', fontsize=self.text_size, ha='center', va='center')

    def add_start_impedance_text(self, value):
        start_impedance = complex(120)
        start = f"$Z_{{start}}:${start_impedance}Ω"
        self.z_start_text =  self.ax.annotate(start, (-1, -0.9), color='red', fontsize=self.text_size)

    def add_target_impedance_text(self, value):
        target_impedance = complex(60, 0)
        target = f"$Z_{{target}}:${target_impedance}Ω"
        self.z_target_text = self.ax.annotate(target, (0.75, -0.9), color='green', fontsize=self.text_size)

    def plot(self, *args, **kwargs):
        new_args = []
        for arg in args:
            xy = self.impedance_to_gamma(arg)
            new_args.append([xy.real, xy.imag])

        for index, [real, imag] in enumerate(new_args):
            if index == 0:
                self.ax.plot(real, imag, 'x', color='red')
                self.add_start_impedance_text(args[index])
            elif index == len(new_args) - 1:
                self.ax.plot(real, imag, 'o', color='green')
                self.add_target_impedance_text(args[index])
            else:
                # TODO: Interpolate between points
                print("Else")

        #self.ax.plot(gamma.real, gamma.imag, 'o', color="green")

    def impedance_to_gamma(self, impedance):
        return complex(impedance - self.z0) / (impedance + self.z0)

    def admittance_to_gamma(self, admittance):
        return complex(admittance - 1 / self.z0) / (admittance + 1 / self.z0)

    def set_z0(self, value):
        if value > 0:
            self.z0 = value
            self.z0_text.set_text(f"Z0={value}Ω")


if __name__ == '__main__':
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot()
    z_start = complex(120, 0)
    z_end = complex(60, 0)
    sc = SmithChart(ax)
    sc.set_z0(60)
    sc.plot(z_start, z_end)
    fig.show()
