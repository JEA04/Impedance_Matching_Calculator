from typing import Any

import matplotlib.pyplot as plt
import numpy
import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle


class SmithChart(object):

    def __init__(self, ax):
        # Class Parameters
        self.ax = ax
        self.z0 = 50
        self.text_size = 10
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
        self.ax.axis(np.array([-1.1, 1.1, -1.1, 1.1]))
        self.draw_smith_chart()

    def plot(self, *args, **kwargs):
        new_points = []
        for arg in args:
            new_points.append(arg)

        previous_point = None
        for index, point in enumerate(new_points):
            xy = self.impedance_to_gamma(point)
            if index == 0:
                self.ax.plot(xy.real, xy.imag, 'x', color='red')
                self.add_start_impedance_text(args[index])
            elif index == len(new_points) - 1:
                self.ax.plot(xy.real, xy.imag, 'o', color='green')
                self.add_target_impedance_text(args[index])
                self.draw_curve_between_points(previous_point, point)
            else:
                # TODO: Interpolate between points
                self.draw_curve_between_points(previous_point, point)
            previous_point = point

    def draw_curve_between_points(self, previous, current):
        inter_circle_x = []
        inter_circle_y = []
        if round(previous.real,3) != round(current.real, 3):
            inter_points = np.linspace((1/previous).imag, (1/current).imag, num=50)
            for point in inter_points:
                admittance_point = complex((1/previous).real, point)
                xy = self.admittance_to_gamma(admittance_point)
                inter_circle_x.append(xy.real)
                inter_circle_y.append(xy.imag)
        else:
            # Work with Impedance
            inter_points = np.linspace(previous.imag, current.imag, num=50)
            for point in inter_points:
                xy = self.impedance_to_gamma(complex(previous.real, point))
                inter_circle_x.append(xy.real)
                inter_circle_y.append(xy.imag)
        self.ax.plot(inter_circle_x, inter_circle_y, '-', color='gray', zorder=1)
        return

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
        z0_box = Rectangle(xy=(0.6, 0.9), width=0.4, height=0.15, ec='black', fc='none',)
        self.ax.add_patch(z0_box)
        rx, ry = z0_box.get_xy()
        tx = rx + z0_box.get_width() / 2.0
        ty = ry + z0_box.get_height() / 2.0
        self.z0_text = self.ax.annotate(z0_text, (tx, ty), color='black',
                                        fontsize=self.text_size, ha='center', va='center')

    def add_start_impedance_text(self, value):
        start = f"$Z_{{start}}:${value}Ω"
        self.z_start_text = self.ax.annotate(start, (-1.0, -1.1), color='red',
                                              fontsize=self.text_size, ha='left', va='center')

    def add_target_impedance_text(self, value):
        target = f"$Z_{{target}}:${value}Ω"
        self.z_target_text = self.ax.annotate(target, (1, -1.1), color='green',
                                              fontsize=self.text_size, ha='right', va='center')

    def add_component_values(self, c1, c2):
        components_text = f"[1] {c1[0]}: {c1[1]} {c1[2]}\n[2] {c2[0]}: {c2[1]} {c2[2]}"
        self.ax.annotate(components_text, (-1.1, 1.0), color='black',
                         fontsize=self.text_size, ha='left', va='center')

    def impedance_to_gamma(self, impedance):
        return complex(impedance - self.z0) / (impedance + self.z0)

    def admittance_to_gamma(self, admittance):
        y0 = 1/self.z0
        return complex(-(admittance - y0)/(admittance + y0))

    def set_z0(self, value):
        if value > 0:
            self.z0 = value
            self.z0_text.set_text(f"$Z_0$={value}Ω")


if __name__ == '__main__':
    fig = plt.figure(figsize=(10, 10))
    # for i in range(1, 4):
    #     ax = fig.add_subplot(2, 2, i)
    #     z_start = complex(100, 75)
    #     z_end = complex(60, 80)
    #     sc = SmithChart(ax)
    #     sc.set_z0(60)
    #     sc.plot(z_start, complex(120, 0), z_end)
    #     sc.add_component_values('Lp: 7.83nH', 'Cs: 1.09 pF')
    ax = fig.add_subplot()
    z_start = complex(20, 0)
    middle = complex(20, -24.5)
    z_end = complex(50, 0)
    sc = SmithChart(ax)
    sc.set_z0(50)
    sc.plot(z_start, middle, z_end)
    fig.show()

