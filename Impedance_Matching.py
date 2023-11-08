# Impedance Matching with Lumped Networks
# Wireless Communication 1 Testate
# Author: Jeremy Allenspach
# Date: 06.11.2023

from math import sqrt
import numpy as np

# Let's assume the Input and Output Impedance.
# For future use in a Smith Chart Z0 will be assumed as 50 Ohms
load_impedance = complex(50, 10)
source_impedance = complex(100, 50)
Z_0 = 50
f_c = 500e6  # Center Frequency


def calculate_q(numerator: complex, denominator: complex):
    """

    :param numerator:
    :param denominator:
    :return:
    """
    return sqrt(numerator.real / denominator.real - 1 + numerator.imag ** 2 / (numerator.real * denominator.real))


def calculate_capacitance(frequency, impedance):
    """

    :param frequency:
    :param impedance:
    :return:
    """
    w = 2 * np.pi * frequency
    return 1 / (w * impedance)


def calculate_inductance(frequency, impedance):
    """

    :param frequency:
    :param impedance:
    :return:
    """
    w = 2 * np.pi * frequency
    return w * impedance


def calculate_x1(nominator_impedance: complex, denominator_impedance: complex, q):
    x1_p = ((nominator_impedance.imag + nominator_impedance.real * q) /
            (nominator_impedance.real / denominator_impedance.real - 1))
    x1_n = ((nominator_impedance.imag - nominator_impedance.real * q) /
            (nominator_impedance.real / denominator_impedance.real - 1))
    return x1_p, x1_n


def calculate_x2(impedance: complex, q):
    x2_p = -(impedance.imag + impedance.real * q)
    x2_n = -(impedance.imag - impedance.real * q)
    return x2_p, x2_n


if __name__ == '__main__':
    # Determine which Lumped Networks are suitable
    if source_impedance.real > load_impedance.real:
        print("Normal L-Section")
        Q = calculate_q(source_impedance, load_impedance)
        X1_1 = (source_impedance.imag + source_impedance.real * Q) / (source_impedance.real / load_impedance.real - 1)
        X1_2 = source_impedance.real / Q
    elif source_impedance.real < load_impedance.real:
        q = calculate_q(load_impedance, source_impedance)
        print(calculate_x1(load_impedance, source_impedance, q))
        print(calculate_x2(source_impedance, q))
        print("Reversed L-Section")
    else:
        # X1 is infinite
        # X2 is -(XL + XG)
        print("Short")
