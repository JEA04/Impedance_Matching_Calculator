# Impedance Matching with Lumped Networks
# Wireless Communication 1 Testate
# Author: Jeremy Allenspach
# Date: 06.11.2023

import numpy as np
import matplotlib.pyplot as plt
import matching
import smitchart


def create_output_string(values):
    return f"{values[0]}: {values[1]:>6}{values[2]}"

def add_new_subplot(index):
    ax = fig.add_subplot(2, 2, index)
    smith_ax = smitchart.SmithChart(ax)
    return smith_ax

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
        # Table 3
        [2.44e9, complex(13, 60), complex(13, -60), 60],
        [2.44e9, complex(60, -30), complex(60, 0), 60],
        [2.44e9, complex(60, 20), complex(60, 80), 60]
    ])

    for fc, source_impedance, load_impedance, z0 in circuits:
        subplot_index = 1
        print(f"Zs: {source_impedance}\tZt: {load_impedance}")
        networks = matching.match_network(source_impedance, load_impedance, fc, cap_lim, ind_lim)
        fig = plt.figure(figsize=(10, 10))
        fig.tight_layout()
        for l_network in networks:
            if l_network == "Normal":
                print("Network Type: Normal")
                normal_networks = networks.get(l_network).get("Values")
                for parallel, series in normal_networks:
                    # Create Smith Chart Plot
                    chart = add_new_subplot(subplot_index)
                    subplot_index += 1

                    # Plot to Smith Chart

                    # Save to PDF
                    # Debug print to Console
                    print(f"{create_output_string(parallel)} | {create_output_string(series)}")
                print()
            elif l_network == "Reversed":
                print("Network Type: Reversed")
                reversed_networks = networks.get(l_network).get("Values")
                for series, parallel in reversed_networks:
                    chart = add_new_subplot(subplot_index)
                    subplot_index += 1

                    # Plot to Smith Chart

                    # Save to PDF
                    # Debug print to Console
                    print(f"{create_output_string(series)} | {create_output_string(parallel)}")
            else:
                print("Special Case")
                network = networks.get(l_network).get("Values")
                chart = add_new_subplot(subplot_index)
                subplot_index += 1

                # Plot to Smith Chart

                # Save to PDF
                # Debug print to Console
                print(network)
        fig.show()
        print("-----------------------------------------------------------------\n")
        # TODO: Plot Smith Charts

        # TODO: Create Circuits using Schemdraw

        # TODO: Save Results and Smith Charts to PDF
