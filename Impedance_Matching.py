# Impedance Matching with Lumped Networks
# Wireless Communication 1 Testate
# Author: Jeremy Allenspach
# Date: 06.11.2023

import numpy as np
import matching

# Let's assume the Input and Output Impedance.
# For future use in a Smith Chart Z0 will be assumed as 50 Ohms
load_impedance = complex(100, 50)
source_impedance = complex(50, 10)
Z_0 = 50
center_frequency = 500e6  # Center Frequency

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
    return impedance / w


if __name__ == '__main__':
    # Define Network
    circuits = np.array([
        # Table 1
        [2.44e9, complex(20, 0), complex(50, 0), 50],
        [2.44e9, complex(20, -10), complex(60, 60), 50],
        [2.44e9, complex(100, 75), complex(30, 0), 50],
        # Table 2
        [2.44e9, complex(15, 50), complex(50, 0), 30],
        [2.44e9, complex(15, 50), complex(50, -10), 30],
        [2.44e9, complex(30, -45), complex(45, -30), 30],
        # Table 3
        [2.44e9, complex(13, 60), complex(13, -60), 60],
        [2.44e9, complex(60, -30), complex(60, 0), 60],
        [2.44e9, complex(60, 20), complex(60, 80), 60]
    ])

    load_impedance = complex(20, 0)
    source_impedance = complex(50, 0)

    networks = matching.match_network(load_impedance, source_impedance)
    print(networks)

    # Plot Smith Charts

    # Calculate Component Values of all Networks
    # for network in networks:
    #    for value in network:
    #        if value >= 0:
    #            component = calculate_inductance(center_frequency, value)
    #        else:
    #            component = calculate_capacitance(center_frequency, value)
    #        print(f"Impedance: {value: .2e} | Component: {component: .2e}")
    #    print("------------------------------------------------")
