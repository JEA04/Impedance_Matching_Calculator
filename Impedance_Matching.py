# Impedance Matching with Lumped Networks
# Wireless Communication 1 Testat
# Author: Jeremy Allenspach
# Date: 06.11.2023

import cmath

if __name__ == '__main__':
    z_In = complex(20, 0)
    z_End = complex(50, 0)
    z0 = 50
    fc = 2.44e9

    # Determine which Lumped Networks are suitable
    if z_In.real > z_End.real:
        print("Normal L-Section")
    elif z_In.real < z_End.real:
        print("Reversed L-Section")
    else:
        print("Short")



