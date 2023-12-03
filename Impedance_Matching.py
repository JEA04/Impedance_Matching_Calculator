# Impedance Matching with Lumped Networks
# Wireless Communication 1 Testate
# Author: Jeremy Allenspach
# Date: 06.11.2023

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from fpdf import FPDF
from PIL import Image
import matching
import smitchart


def create_output_string(values):
    return f"{values[0]}: {values[1]:>6}{values[2]}"


def add_new_subplot(index):
    ax = fig.add_subplot(2, 2, index)
    smith_ax = smitchart.SmithChart(ax)
    return smith_ax


def create_pdf_table(pdf, fc, source, load, z0):
    data = [["$$f_c$$", "$$Z_{start}$$", "$$Z_{target}$$", "$$Z_0"],
            [f"{fc.real / 10 ** 9}GHz", f"{source_impedance}Ω", f"{load_impedance}Ω", f"{z0}Ω"]]

    pdf.set_x(10)
    pdf.set_y(40)
    with pdf.table(text_align="CENTER") as table:
        for data_row in data:
            row = table.row()
            for value in data_row:
                row.cell(value)

if __name__ == '__main__':
    # Define
    cap_lim = (1.0, 1.0e-15)
    ind_lim = (1.0, 10e-9)
    network_num = 0
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

    # Create a new PDF Object
    pdf = FPDF()
    pdf.add_font("roboto", style="", fname="font/Roboto-Regular.ttf")
    pdf.add_font("roboto", style="B", fname="font/Roboto-Bold.ttf")
    pdf.set_font("roboto", "", 12)

    for fc, source_impedance, load_impedance, z0 in circuits:
        subplot_index = 1
        network_num += 1
        print(f"Zs: {source_impedance}\tZt: {load_impedance}")
        networks = matching.match_network(source_impedance, load_impedance, fc, cap_lim, ind_lim)

        # Create Plot
        fig = plt.figure(figsize=(10, 10), dpi=300)
        fig.tight_layout()

        # Add New Page to PDF
        pdf.add_page()
        pdf.set_font(size=24)
        pdf.text(10, 20, text=f"Network {network_num}")
        pdf.set_font(size=8)
        create_pdf_table(pdf, fc, source_impedance, load_impedance, z0)


        for l_network in networks:
            if l_network == "Normal":
                print("Network Type: Normal")
                normal_networks = networks.get(l_network).get("Values")
                for parallel, series in normal_networks:
                    # Create Smith Chart Plot
                    chart = add_new_subplot(subplot_index)
                    subplot_index += 1

                    # Plot to Smith Chart
                    chart.plot(source_impedance, load_impedance)

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
                    chart.plot(source_impedance,load_impedance)

                    # Save to PDF
                    # Debug print to Console
                    print(f"{create_output_string(series)} | {create_output_string(parallel)}")
            else:
                print("Network Type: Special")
                network = networks.get(l_network).get("Values")
                chart = add_new_subplot(subplot_index)
                subplot_index += 1

                # Plot to Smith Chart
                chart.plot(source_impedance, load_impedance)

                # Save to PDF
                # Debug print to Console
                print(create_output_string(network))

        # fig.show()
        canvas = FigureCanvas(fig)
        canvas.draw()
        img = Image.fromarray(np.asarray(canvas.buffer_rgba()))
        pdf.image(img, h=pdf.epw, w=pdf.epw)
        print("-----------------------------------------------------------------\n")


        # TODO: Create Circuits using Schemdraw

        # TODO: Save Results and Smith Charts to PDF

    pdf.output("report.pdf")
