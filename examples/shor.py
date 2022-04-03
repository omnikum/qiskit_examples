from lib.lib_shor import Algorithm_Shor
import matplotlib.pyplot as plt
import numpy as np
from qiskit import QuantumCircuit, Aer, transpile, assemble
from qiskit.visualization import plot_histogram
from math import gcd
from numpy.random import randint
import pandas as pd
from fractions import Fraction
from config import SHOR_BASE, SHOR_COUNT

def quantum_shor():

    qshor = Algorithm_Shor()
    # Create QuantumCircuit with SHOR_COUNT counting qubits
    # plus 4 qubits for U to act on
    qc = QuantumCircuit(SHOR_COUNT + 4, SHOR_COUNT)

    # Initialize counting qubits
    # in state |+>
    for q in range(SHOR_COUNT):
        qc.h(q)

    # And auxiliary register in state |1>
    qc.x(3 + SHOR_COUNT)

    # Do controlled-U operations
    for q in range(SHOR_COUNT):
        qc.append(qshor.c_amod15(SHOR_BASE, 2 ** q),
                  [q] + [i + SHOR_COUNT for i in range(4)])

    # Do inverse-QFT
    qc.append(qshor.qft_dagger(SHOR_COUNT), range(SHOR_COUNT))

    # Measure circuit
    qc.measure(range(SHOR_COUNT), range(SHOR_COUNT))

    aer_sim = Aer.get_backend('aer_simulator')
    t_qc = transpile(qc, aer_sim)
    qobj = assemble(t_qc)
    results = aer_sim.run(qobj).result()
    counts = results.get_counts()
    plot_histogram(counts)

    rows, measured_phases = [], []
    for output in counts:
        decimal = int(output, 2)  # Convert (base 2) string to decimal
        phase = decimal / (2 ** SHOR_COUNT)  # Find corresponding eigenvalue
        measured_phases.append(phase)
        # Add these values to the rows in our table:
        rows.append([f"{output}(bin) = {decimal:>3}(dec)",
                     f"{decimal}/{2 ** SHOR_COUNT} = {phase:.2f}"])
    # Print the rows in a table
    headers = ["Register Output", "Phase"]
    df = pd.DataFrame(rows, columns=headers)
    print(df)

    rows = []
    for phase in measured_phases:
        frac = Fraction(phase).limit_denominator(15)
        rows.append([phase, f"{frac.numerator}/{frac.denominator}", frac.denominator])
    # Print as a table
    headers = ["Phase", "Fraction", "Guess for r"]
    df = pd.DataFrame(rows, columns=headers)
    print(df)
