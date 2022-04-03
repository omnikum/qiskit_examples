from qiskit import QuantumCircuit, Aer, assemble
import numpy as np
from numpy.random import randint
from math import pi
class BB84:

    def encode_message(self, bits, bases):
        if len(bits) != len(bases):
            print("number of bits and bases are not equal!")
            exit(0)

        message = []

        length = len(bits)

        for i in range(length):
            qc = QuantumCircuit(1, 1)
            if bases[i] == 0:     # Prepare qubit in Z-basis
                if bits[i] == 0:
                    pass
                else:
                    qc.x(0)
            elif bases[i] == 1:   # Prepare qubit in X-basis
                if bits[i] == 0:
                    qc.h(0)       # 45 grad state
                else:
                    qc.x(0)
                    qc.h(0)       # 135 grad state
            qc.barrier()
            print(qc)
            message.append(qc)
        return message

    def measure_message(self, message, bases):
        if len(message) != len(bases):
            print("bits number in message and number of bases are not equal!")
            exit(0)
        length = len(message)

        measurements = []
        for q in range(length):
            if bases[q] == 0:  # measuring in Z-basis
                message[q].measure(0, 0)
            if bases[q] == 1:  # measuring in X-basis
                message[q].h(0)
                message[q].measure(0, 0)
            aer_sim = Aer.get_backend('aer_simulator')
            qobj = assemble(message[q], shots=1, memory=True)
            result = aer_sim.run(qobj).result()
            measured_bit = int(result.get_memory()[0])
            measurements.append(measured_bit)
        return measurements

    def remove_garbage(self, a_bases, b_bases, bits):
        good_bits = []
        length = len(bits)
        for q in range(length):
            if a_bases[q] == b_bases[q]:
                # If both used the same basis, add
                # this to the list of 'good' bits
                good_bits.append(bits[q])
        return good_bits

    def sample_bits(self, bits, selection):
        sample = []
        for i in selection:
            # use np.mod to make sure the
            # bit we sample is always in
            # the list range
            i = np.mod(i, len(bits))
            # pop(i) removes the element of the
            # list at index 'i'
            sample.append(bits.pop(i))
        return sample

    def bit_selection(self, length, sample_size):
        selection = randint(length, size=sample_size)
        return selection
