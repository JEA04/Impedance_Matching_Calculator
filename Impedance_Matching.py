# Impedance Matching with Lumped Networks
# Wireless Communication 1 Testate
# Author: Jeremy Allenspach
# Date: 06.11.2023

from math import sqrt

# Let's assume the Input and Output Impedance.
# For future use in a Smith Chart Z0 will be assumed as 50 Ohms
Z_G = complex(70, 0)
Z_L = complex(50, 0)
Z_0 = 50
f_c = 2.44e9        # Center Frequency


if __name__ == '__main__':
    # Determine which Lumped Networks are suitable
    if Z_G.real > Z_L.real:
        print("Normal L-Section")
        Q = sqrt(Z_G.real/Z_L.real - 1 + Z_G.imag ** 2 /(Z_L.real * Z_G.real))
        X1_1 = (Z_G.imag + Z_G.real * Q) / (Z_G.real / Z_L.real - 1)
        X1_2 = Z_G.real / Q
    elif Z_G.real < Z_L.real:
        print("Reversed L-Section")
    else:
        # X1 is infinite
        # X2 is -(XL + XG)
        print("Short")
