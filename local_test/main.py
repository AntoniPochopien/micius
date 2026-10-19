from micius import MiciusClient
from qiskit import QuantumCircuit


def main():
    base_url = "http://localhost:8000"
    alice = MiciusClient(base_url, caller="alice")
    bob = MiciusClient(base_url, caller="bob", session_id=alice.session_id)

    prep = QuantumCircuit(2)
    prep.h(0)
    prep.cx(0, 1)
    alice.sync(prep)

    alice.transfer(1, "bob")
    alice.measure()
    print(alice.execute())
    print(bob.execute())


if __name__ == "__main__":
    main()
