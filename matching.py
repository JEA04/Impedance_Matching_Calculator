from math import sqrt, floor, log10
import numpy as np


def match_network(source_impedance: complex, load_impedance: complex, frequency,
                  cap_lim: (float, float), ind_lim: (float, float)):
    """
    TODO: Docstring Comment for match_network function
    :param ind_lim:
    :param cap_lim:
    :param frequency:
    :param source_impedance:
    :param load_impedance:
    :return:
    """
    if source_impedance.real > load_impedance.real:
        if abs(load_impedance.imag) >= sqrt(load_impedance.real * (source_impedance.real - load_impedance.real)):
            # Normal and Reversed
            networks = {
                "Normal": calculate_normal(source_impedance, load_impedance, frequency),
                "Reversed": calculate_reversed(source_impedance, load_impedance, frequency)
            }
        else:
            # Only Normal
            normal = calculate_normal(source_impedance, load_impedance, frequency)
            networks = {
                "Normal": normal
            }
    elif source_impedance.real < load_impedance.real:
        if abs(source_impedance.imag) >= sqrt(source_impedance.real * (load_impedance.real - source_impedance.real)):
            networks = {
                "Normal": calculate_normal(source_impedance, load_impedance, frequency),
                "Reversed": calculate_reversed(source_impedance, load_impedance, frequency)
            }
        else:
            networks = {
                "Reversed": calculate_reversed(source_impedance, load_impedance, frequency)
            }
    else:
        networks = {
            "Special": calculate_special_case(source_impedance, load_impedance, frequency)
        }
    return networks


def calculate_q(numerator: complex, denominator: complex):
    """
    Functions calculates the Q value which is used to calculate the two Impedance's in an L-Network
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


def calculate_reversed(source: complex, load: complex, frequency):
    """
    TODO: Docstring for calculate_reversed
    :param frequency:
    :param source:
    :param load:
    :return:
    """
    q = calculate_q(load, source)
    x1 = np.array(calculate_x1(load, source, q)).reshape((2, 1))
    x2 = np.array(calculate_x2(source, q)).reshape((2, 1))
    solution = np.hstack((x1, x2))
    lumped_elements = {
        "Impedance": solution
    }

    # Calculate Component Values
    values = []
    for x1, x2 in solution:
        xp = calculate_component_value(frequency, x1)
        xp[0] = f"{xp[0]}p"
        xs = calculate_component_value(frequency, x2)
        xs[0] = f"{xs[0]}s"
        values.append([xs, xp])
    component_values = np.asarray(values)
    lumped_elements.update({"Values": component_values})
    return lumped_elements


def calculate_normal(source: complex, load: complex, frequency):
    """
    TODO: Docstring for calculate_normal
    :param frequency:
    :return:
    :param source:
    :param load:
    :return:
    """
    q = calculate_q(source, load)
    x1 = np.array(calculate_x1(source, load, q)).reshape((2, 1))
    x2 = np.array(calculate_x2(load, q)).reshape((2, 1))
    solution = np.hstack((x1, x2))
    lumped_elements = {
        "Impedance": solution
    }

    # Calculate Component Values
    values = []
    for x1, x2 in solution:
        xp = calculate_component_value(frequency, x1)
        xp[0] = f"{xp[0]}p"
        xs = calculate_component_value(frequency, x2)
        xs[0] = f"{xs[0]}s"
        values.append([xp, xs])
    component_values = np.asarray(values)
    lumped_elements.update({"Values": component_values})
    return lumped_elements


def calculate_special_case(source: complex, load: complex, frequency):
    x2 = -(load.imag + source.imag)
    lumped_elements = {
        "Impedance": x2
    }
    xs = calculate_component_value(frequency, x2)
    lumped_elements.update({"Values": xs})
    return lumped_elements

def calculate_component_value(frequency, impedance):
    if impedance > 0:
        value, exp = calculate_inductance(frequency, impedance)
        unit = get_prefix(exp) + "H"
        return ["L", value, unit]
    elif impedance < 0:
        value, exp = calculate_capacitance(frequency, impedance)
        unit = get_prefix(exp) + "F"
        return ["C", value, unit]
    else:
        return ["",0, ""]


def calculate_capacitance(frequency, impedance):
    """
    TODO: Docstring for calculate_capacitance
    :param frequency:
    :param impedance:
    :return:
    """
    w = 2 * np.pi * frequency
    capacitance = (1 / (w * impedance)).real
    exponent = get_exponent(capacitance)
    component_value = reformat_value(capacitance, exponent, 2) * (-1)
    return component_value, exponent


def calculate_inductance(frequency, impedance):
    """
    TODO: Docstring for calculate_inductance
    :param frequency:
    :param impedance:
    :return:
    """
    w = 2 * np.pi * frequency
    inductance = (impedance / w).real
    exponent = get_exponent(inductance)
    component_value = reformat_value(inductance, exponent, 2)
    return component_value, exponent


def get_exponent(value: float):
    """
    Function calculates the exponent of the value
    :param value:  preferably in scientific notation
    :return: Only returns the exponent (5.042e-12 --> 12)
    """
    return floor(log10(abs(value)))


def reformat_value(value, exponent, decimal_points: int):
    exp = exponent - (exponent % 3)
    if exponent > 0:
        formatted_value = round(value / (10 ** exp), decimal_points)
    elif exponent < 0:
        formatted_value = round(value * 10 ** abs(exp), decimal_points)
    else:
        formatted_value = round(value, decimal_points)
    return formatted_value


def get_prefix(exponent: int):
    """
    Function takes an exponent as parameter and returns the corresponding SI-Prefix
    :param exponent:
    :return:    SI-Prefix (exponent = 3 --> m)
    """
    si = [
        "q",  # -30
        "r",  # -27
        "y",  # -24
        "z",  # -21
        "a",  # -18
        "f",  # -15
        "p",  # -12
        "n",  # -9
        "u",  # -6
        "m",  # -3
        "",  # 0
        "K",  # 3
        "M",  # 6
        "G",  # 9
        "T",  # 12
        "P",  # 15
        "E",  # 18
        "Z",  # 21
        "Y",  # 24
        "R",  # 27
        "Q"  # 30
    ]
    return si[floor(exponent / 3 + 10)]
