# Impedance Matching with Lumped Networks
# Wireless Communication 1 Testate
# Author: Jeremy Allenspach
# Date: 06.11.2023

import numpy as np
import matching


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

    for fc, source_impedance, load_impedance, z0 in circuits:
        print(f"Zs: {source_impedance}\tZt: {load_impedance}")
        networks = matching.match_network(source_impedance, load_impedance)
        print("-----------------------------------------------------------------\n")
        # TODO: Plot Smith Charts

    # Calculate Component Values of all Networks
    # for network in networks:
    #    for value in network:
    #        if value >= 0:
    #            component = calculate_inductance(center_frequency, value)
    #        else:
    #            component = calculate_capacitance(center_frequency, value)
    #        print(f"Impedance: {value: .2e} | Component: {component: .2e}")
    #    print("------------------------------------------------")
