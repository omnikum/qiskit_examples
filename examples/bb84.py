from qiskit import Aer
from lib.actors import Actor
from lib.protocol import BB84
from config import BITS_BASES_LENGTH, SAMPLE_SIZE

print("Imports Successful")


def bb84_without_intercept():
    # initialize actors and protocol
    alice = Actor(length=BITS_BASES_LENGTH)
    print("Alice bits   = ", alice.bits)
    print("Alice bases  = ", alice.bases)
    bob = Actor(length=BITS_BASES_LENGTH)
    print("Bob bases    = ", bob.bases)
    bb84 = BB84()
    backend = Aer.get_backend('aer_simulator')

    # prepare Alice message
    alice_message = bb84.encode_message(alice.bits, alice.bases)

    # Bob receive message, if alice.bases and bob.bases are equal, then Bob can read
    # bit with 100% probability, or if they not equal then 50% probability
    bob_results = bb84.measure_message(message=alice_message, bases=bob.bases)
    print("Bob results  = ", bob_results)

    # now we need to remove all bits, where are bases is not equal
    alice_key = bb84.remove_garbage(alice.bases, bob.bases, alice.bits)
    print("Alice key    = ", alice_key)
    bob_key = bb84.remove_garbage(alice.bases, bob.bases, bob_results)
    print("Bob key      = ", bob_key)

    # use random number of "good" bits in keys (just need to choose a sample size)
    sample = bb84.bit_selection(length=len(alice.bits), sample_size=SAMPLE_SIZE)
    bob_sample = bb84.sample_bits(bits=bob_key, selection=sample)
    alice_sample = bb84.sample_bits(bits=alice_key, selection=sample)

    print("Alice sample = ", alice_sample)
    print("Bob sample   = ", bob_sample)


def bb84_with_intercept():
    # initialize actors and protocol
    alice = Actor(length=BITS_BASES_LENGTH)
    print("Alice bits   = ", alice.bits)
    print("Alice bases  = ", alice.bases)
    bob = Actor(length=BITS_BASES_LENGTH)
    print("Bob bases    = ", bob.bases)
    eve = Actor(length=BITS_BASES_LENGTH)
    print("Eve bases    = ", eve.bases)

    bb84 = BB84()
    backend = Aer.get_backend('aer_simulator')

    # prepare Alice message
    alice_message = bb84.encode_message(alice.bits, alice.bases)

    # interception (!)
    eve_results = bb84.measure_message(message=alice_message, bases=eve.bases)
    print("Eve results  = ", eve_results)

    # Bob receive message, if alice.bases and bob.bases are equal, then Bob can read
    # bit with 100% probability, or if they not equal then 50% probability
    bob_results = bb84.measure_message(message=alice_message, bases=bob.bases)
    print("Bob results  = ", bob_results)

    # now we need to remove all bits, where are bases is not equal
    alice_key = bb84.remove_garbage(alice.bases, bob.bases, alice.bits)
    print("Alice key    = ", alice_key)
    bob_key = bb84.remove_garbage(alice.bases, bob.bases, bob_results)
    print("Bob key      = ", bob_key)

    # use random number of "good" bits in keys (just need to choose a sample size)
    sample = bb84.bit_selection(length=len(alice.bits), sample_size=SAMPLE_SIZE)
    bob_sample = bb84.sample_bits(bits=bob_key, selection=sample)
    alice_sample = bb84.sample_bits(bits=alice_key, selection=sample)

    print("Alice sample = ", alice_sample)
    print("Bob sample   = ", bob_sample)
