# Impedance Matching with Lumped Networks
# Wireless Communication 1 Testate
# Author: Jeremy Allenspach
# Date: 06.11.2023

import numpy as np
import matching

def createOutputString(values):
    return f"{values[0]}: {values[1]:>6}{values[2]}"

if __name__ == '__main__':
    # Define
    cap_lim = (1.0, 1.0e-15)
    ind_lim = (1.0, 10e-9)
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
        # Table 3 NOTE: Removed for now
        [2.44e9, complex(13, 60), complex(13, -60), 60],
        [2.44e9, complex(60, -30), complex(60, 0), 60],
        [2.44e9, complex(60, 20), complex(60, 80), 60]
    ])

    for fc, source_impedance, load_impedance, z0 in circuits:
        print(f"Zs: {source_impedance}\tZt: {load_impedance}")
        networks = matching.match_network(source_impedance, load_impedance, fc, cap_lim, ind_lim)
        for l_network in networks:
            if l_network == "Normal":
                print("Network Type: Normal")
                normal_networks = networks.get(l_network).get("Values")
                for parallel, series in normal_networks:
                    print(f"{createOutputString(parallel)} | {createOutputString(series)}")
                print()
            elif l_network == "Reversed":
                print("Network Type: Reversed")
                reversed_networks = networks.get(l_network).get("Values")
                for series, parallel in reversed_networks:
                    print(f"{createOutputString(series)} | {createOutputString(parallel)}")
            else:
                print("Special Case")

        print("-----------------------------------------------------------------\n")
        # TODO: Plot Smith Charts

        # TODO: Create Circuits using Schemdraw

        # TODO: Save Results and Circuits to PDF
