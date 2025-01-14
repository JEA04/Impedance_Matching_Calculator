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
import smithchart


def create_output_string(values):
    """
    Formatting Function which creates an f-string of a Component
    :param values: Value which needs to be formatted
    :return: Formatted f-string
    """
    return f"{values[0]}: {values[1]:>6}{values[2]}"


def add_new_subplot(subplot_i, normalizing_impedance):
    """
    Functions adds a new subplot to the current figure
    :param subplot_i: Index of the current subplot
    :param normalizing_impedance: Normalizing Impedance according to which the Smith Chart will be drawn
    :return:
    """
    ax = fig.add_subplot(2, 2, subplot_i)
    smith_ax = smithchart.SmithChart(ax, normalizing_impedance)
    return smith_ax


def create_pdf_table(pdf, fc, source, load, z0):
    """
    Function creates the PDF-Table which holds the Information about the Elements that need to be matched
    :param pdf: PDF-File/Object
    :param fc: Matching Frequency
    :param source: Source Impedance
    :param load: Load Impedance
    :param z0: Normalising Impedance
    :return: returns nothing
    """
    data = [[f"fc", f"Zstart", f"Ztarget", f"Z0"],
            [f"{fc.real / 10 ** 9}GHz", f"{source}Ω", f"{load}Ω", f"{z0}Ω"]]
    pdf.set_x(10)
    pdf.set_y(30)
    with pdf.table(text_align="CENTER") as table:
        for table_data in data:
            table_row = table.row()
            for value in table_data:
                table_row.cell(value)


def calculate_point(start, impedance, is_parallel):
    """
    Function calculates the next point based on the given start point and given impedance value
    :param start: Start Impedance
    :param impedance: Impedance which transforms the Start Impedance
    :param is_parallel: Defines whether the given impedance is parrallel to the Start Impedance or not
    :return: Returns the new Impedance as a complex Value
    """
    if is_parallel:
        start_admittance = 1/start
        admittance = 1/impedance
        new_point = 1/(start_admittance + admittance)
    else:
        if impedance != 0:
            new_point = start + impedance
        else:
            new_point = complex(start.real, -start.imag)
    return new_point


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
        [2.44e9, complex(60, 20), complex(60, 80), 60],
    ])

    # Create a new PDF Object
    pdf = FPDF()
    pdf.add_font("roboto", style="", fname="font/Roboto-Regular.ttf")
    pdf.add_font("roboto", style="B", fname="font/Roboto-Bold.ttf")
    pdf.set_font("roboto", "", 12)

    for fc, source_impedance, load_impedance, normalising_impedance in circuits:
        subplot_index = 1
        network_num += 1
        network_text = []
        z0 = int(normalising_impedance.real)
        print(f"Zs: {source_impedance}\tZt: {load_impedance}")
        networks = matching.match_network(source_impedance, load_impedance, fc, cap_lim, ind_lim)

        # Create Plot
        fig = plt.figure(figsize=(10, 10), dpi=250)
        fig.tight_layout()

        # Add New Page to PDF
        pdf.add_page()
        pdf.set_font(size=24)
        pdf.text(10, 20, text=f"Network {network_num}")
        pdf.set_font(size=12)
        create_pdf_table(pdf, fc, source_impedance, load_impedance, z0)

        for l_network in networks:
            if l_network == "Normal":
                print("Network Type: Normal")
                normal_networks = networks.get(l_network).get("Values")
                normal_impedance = networks.get(l_network).get("Impedance")
                for index, [parallel, series] in enumerate(normal_networks):
                    chart = add_new_subplot(subplot_index, z0)
                    subplot_index += 1
                    middle = calculate_point(source_impedance, complex(0, normal_impedance[index][0]), True)
                    end_point = calculate_point(middle, complex(0, normal_impedance[index][1]), False)
                    chart.plot(source_impedance, middle, end_point)
                    chart.add_component_values(parallel, series)
                    text = [create_output_string(parallel), create_output_string(series)]
                    network_text.append(text)
                    print(f"{text[0]} |  {text[1]}")
            elif l_network == "Reversed":
                print("Network Type: Reversed")
                reversed_networks = networks.get(l_network).get("Values")
                reversed_impedance = networks.get(l_network).get("Impedance")
                for index, [series, parallel] in enumerate(reversed_networks):
                    chart = add_new_subplot(subplot_index, z0)
                    subplot_index += 1
                    middle = calculate_point(source_impedance, complex(0, reversed_impedance[index][1]), False)
                    end_point = calculate_point(middle, complex(0, reversed_impedance[index][0]), True)
                    chart.plot(source_impedance, middle, end_point)
                    chart.add_component_values(series, parallel)
                    text = [create_output_string(series), create_output_string(parallel)]
                    network_text.append(text)
                    print(f"{text[0]} |  {text[0]}")
            else:
                print("Network Type: Special")
                special_network = networks.get(l_network).get("Impedance")
                network = networks.get(l_network).get("Values")
                chart = add_new_subplot(subplot_index, z0)
                subplot_index += 1
                end_point = calculate_point(source_impedance, complex(0, special_network), False)
                chart.plot(source_impedance, end_point)
                text = create_output_string(network)
                network_text.append(text)
                print(text)

        # Add Results to PDF
        pdf.set_font(size=16)
        pdf.text(10, 60, text="Results")
        pdf.set_font(size=10)
        pdf.set_y(65)
        with pdf.table(text_align="CENTER", first_row_as_headings=False) as network_table:
            for index, data_row in enumerate(network_text):
                row = network_table.row()
                row.cell(f"L-Network {index + 1}")
                length = len(data_row)
                if len(network_text) == 1:
                    row.cell(data_row)
                else:
                    for i, values in enumerate(data_row):
                        row.cell(values)
        # Add Smith Charts to PDF
        canvas = FigureCanvas(fig)
        canvas.draw()
        img = Image.fromarray(np.asarray(canvas.buffer_rgba()))
        pdf.set_x(0)
        pdf.set_y(95)
        pdf.image(img, h=pdf.epw*0.9, w=pdf.epw*0.9)
        print("-----------------------------------------------------------------\n")
    pdf.output("report.pdf")
