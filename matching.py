from math import sqrt

import numpy
import numpy as np


def match_network(source_impedance, load_impedance):
    """
    TODO: Docstring Comment for match_network function
    :param source_impedance:
    :param load_impedance:
    :return:
    """
    if source_impedance.real > load_impedance.real:
        if abs(load_impedance.imag) >= sqrt(load_impedance.real * (source_impedance.real - load_impedance.real)):
            # Normal and Reversed
            networks = calculate_normal(source_impedance, load_impedance)
            networks = numpy.vstack((networks, calculate_reversed(source_impedance, load_impedance)))
        else:
            # Only Normal
            networks = calculate_normal(source_impedance, load_impedance)
    elif source_impedance.real < load_impedance.real:
        if abs(source_impedance.imag) >= sqrt(source_impedance.real * (load_impedance.real - source_impedance.real)):
            networks = calculate_normal(source_impedance, load_impedance)
            networks = np.vstack((networks, calculate_reversed(source_impedance, load_impedance)))
        else:
            networks = calculate_reversed(source_impedance, load_impedance)
    else:
        x1 = float("inf")
        x2 = -(load_impedance.imag + source_impedance.imag)
        networks = np.array([x1, x2]).reshape((2, 1))
    return networks


def calculate_q(numerator: complex, denominator: complex):
    """
    Functions calculates the Q value which is used to calculate the two Impedances in a L-Network
    :param numerator:
    :param denominator:
    :return:
    """
    return sqrt(numerator.real / denominator.real - 1 + numerator.imag ** 2 / (numerator.real * denominator.real))


def calculate_x1(nominator_impedance: complex, denominator_impedance: complex, q):
    """
    TODO: Docstring for calculate_x1
    :param nominator_impedance:
    :param denominator_impedance:
    :param q:
    :return:
    """
    x1_p = ((nominator_impedance.imag + nominator_impedance.real * q) /
            (nominator_impedance.real / denominator_impedance.real - 1))
    x1_n = ((nominator_impedance.imag - nominator_impedance.real * q) /
            (nominator_impedance.real / denominator_impedance.real - 1))
    return x1_p, x1_n


def calculate_x2(impedance: complex, q):
    """
    TODO: Docstring for calculate_x2
    :param impedance:
    :param q:
    :return:
    """
    x2_p = -(impedance.imag + impedance.real * q)
    x2_n = -(impedance.imag - impedance.real * q)
    return x2_p, x2_n


def calculate_reversed(source: complex, load: complex):
    """
    TODO: Docstring for calculate_reversed
    :param source:
    :param load:
    :return:
    """
    Q = calculate_q(load, source)
    X1 = np.array(calculate_x1(load, source, Q)).reshape((2, 1))
    X2 = np.array(calculate_x2(source, Q)).reshape((2, 1))
    sol = np.hstack((X1, X2))
    return sol


def calculate_normal(source: complex, load: complex):
    """
    TODO: Docstring for calculate_normal
    :param source:
    :param load:
    :return:
    """
    Q = calculate_q(source, load)
    X1 = np.array(calculate_x1(source, load, Q)).reshape((2, 1))
    X2 = np.array(calculate_x2(source, Q)).reshape((2, 1))
    sol = np.hstack((X1, X2))
    return sol
