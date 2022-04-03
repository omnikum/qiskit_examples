import matplotlib.pyplot as plt
import numpy as np
from qiskit import QuantumCircuit, Aer, transpile, assemble
from qiskit.visualization import plot_histogram
from math import gcd
from numpy.random import randint
import pandas as pd
from fractions import Fraction

class Algorithm_Shor:

    def c_amod15(self, a, power):
        """Controlled multiplication by a mod 15"""
        if a not in [2, 4, 7, 8, 11, 13]:
            raise ValueError("'a' must be 2,4,7,8,11 or 13")
        u = QuantumCircuit(4)
        for iteration in range(power):
            if a in [2, 13]:
                u.swap(0, 1)
                u.swap(1, 2)
                u.swap(2, 3)
            if a in [7, 8]:
                u.swap(2, 3)
                u.swap(1, 2)
                u.swap(0, 1)
            if a in [4, 11]:
                u.swap(1, 3)
                u.swap(0, 2)
            if a in [7, 11, 13]:
                for q in range(4):
                    u.x(q)
        u = u.to_gate()
        u.name = "%i^%i mod 15" % (a, power)
        c_u = u.control()
        return c_u

    def qft_dagger(self, n):
        """n-qubit QFTdagger the first n qubits in circ"""
        qc = QuantumCircuit(n)
        # Don't forget the Swaps!
        for qubit in range(n // 2):
            qc.swap(qubit, n - qubit - 1)
        for j in range(n):
            for m in range(j):
                qc.cp(-np.pi / float(2 ** (j - m)), m, j)
            qc.h(j)
        qc.name = "QFT†"
        return qc
