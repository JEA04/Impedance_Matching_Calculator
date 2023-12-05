from math import sqrt, floor, log10
import numpy as np


def match_network(source_impedance: complex, load_impedance: complex, frequency,
                  cap_lim: (float, float), ind_lim: (float, float)):
    """
    Matching Function determines Network Type and then Calculates all possible networks
    :param ind_lim: Minimal allowed Inductance
    :param cap_lim: Minimal allowed Capacitance
    :param frequency: Frequency at which the elements need to be matched
    :param source_impedance: Source Impedance
    :param load_impedance: Load Impedance
    :return: Returns a Dictionary which holds all possible Networks
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
    :param numerator:   Load or source Impedance based on L-Network Type
    :param denominator: Load or source Impedance based on L-Network Type
    :return:
    """
    return sqrt(numerator.real / denominator.real - 1 + numerator.imag ** 2 / (numerator.real * denominator.real))


def calculate_x1(nominator_impedance: complex, denominator_impedance: complex, q):
    """
    Calculates Parallel Impedance of the Matching Network
    :param nominator_impedance: Source or Load Impedance based on L-Network Type
    :param denominator_impedance: Source or Load Impedance based on L-Network Type
    :param q: Q-Factor
    :return: both possible values of x1
    """
    x1_p = ((nominator_impedance.imag + nominator_impedance.real * q) /
            (nominator_impedance.real / denominator_impedance.real - 1))
    x1_n = ((nominator_impedance.imag - nominator_impedance.real * q) /
            (nominator_impedance.real / denominator_impedance.real - 1))
    return x1_p, x1_n


def calculate_x2(impedance: complex, q):
    """
    Calculate Series Component of the Network
    :param impedance: Load or Source Impedance based on the
    :param q: Q-Factor
    :return: Both possible values of x2
    """
    x2_p = -(impedance.imag + impedance.real * q)
    x2_n = -(impedance.imag - impedance.real * q)
    return x2_p, x2_n


def calculate_reversed(source: complex, load: complex, frequency):
    """
    Calculates both possible networks for a reversed L-Section (series then parallel)
    :param frequency: Frequency at which the elements need to be matched
    :param source: Source Impedance
    :param load: Load Impedance
    :return: Dictionary which holds both the Impedance and Component Values
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
    Function calculates both possible values for the normal (parallel then series) L-Section
    :param source: Source Impedance
    :param load: Load Impedance
    :param frequency: Frequency at which the elements need to be matched
    :return: Dictionary which holds both the Impedance and Component Values
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
    """
    Function calculates the possible Network for a special Case where the real part stays the same
    :param source: Source Impedance
    :param load: Load Impedance
    :param frequency: Frequency at which the elements need to be matched
    :return: Dictionary which holds both the Impedance and Component Value
    """
    x2 = -(load.imag + source.imag)
    lumped_elements = {
        "Impedance": x2
    }
    xs = calculate_component_value(frequency, x2)
    if xs[1] != 0:
        xs[0] = f"{xs[0]}s"
    else:
        xs[0] = ""
        xs[1] = "Short"
    lumped_elements.update({"Values": xs})
    return lumped_elements


def calculate_component_value(frequency, impedance):
    """
    Calculates the Components Value.
    :param frequency:
    :param impedance: Negative Impedance means capacitor. Positive means inductance
    :return: A list with three Elements [Component Type, Value, Unit with SI-Prefix
    """
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
    Calculate the Capacitance Value based on impedance and Frequency
    :param frequency:
    :param impedance: Negative Impedance
    :return: Returns rounded Capacitance Value and the exponent
    """
    w = 2 * np.pi * frequency
    capacitance = (1 / (w * impedance)).real
    exponent = get_exponent(capacitance)
    component_value = reformat_value(capacitance, exponent) * (-1)
    return component_value, exponent


def calculate_inductance(frequency, impedance):
    """
    Calculates Impedance based on Frequency and Impedance
    :param frequency:
    :param impedance: Positive Impedance
    :return: Return rounded Impedance Value and it's exponent
    """
    w = 2 * np.pi * frequency
    inductance = (impedance / w).real
    exponent = get_exponent(inductance)
    component_value = reformat_value(inductance, exponent)
    return component_value, exponent


def get_exponent(value: float):
    """
    Function calculates the exponent of the value
    :param value:  preferably in scientific notation
    :return: Only returns the exponent (5.042e-12 --> 12)
    """
    return floor(log10(abs(value)))


def reformat_value(value, exponent):
    """
    Function reformats the value based on its exponents. Rounds the value, so it's always three digits
    867.553
    :param value: Value which needs to be reformatted
    :param exponent:
    :return: Returns the Reformatted Value
    """
    decimal_points = 2 - exponent % 3
    exp = exponent - (exponent % 3)
    if exponent > 0:
        formatted_value = round(value / (10 ** exp), decimal_points)
    elif exponent < 0:
        formatted_value = round(value * 10 ** abs(exp), decimal_points)
    else:
        formatted_value = round(value, decimal_points)
    if decimal_points == 0:
        formatted_value = int(formatted_value)
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
