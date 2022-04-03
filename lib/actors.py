from qiskit import QuantumCircuit, Aer, transpile, assemble
from qiskit.visualization import plot_histogram, plot_bloch_multivector
from numpy.random import randint
import numpy as np


class Actor:

    def __init__(self, length: int, seed=None):
        self.bits = self.random_binary_row(length, seed)
        self.bases = self.random_binary_row(length, seed)

    def random_binary_row(self, length: int, seed=None):
        np.random.seed(seed)
        row = randint(2, size=length)
        return row

