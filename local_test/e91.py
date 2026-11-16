from qiskit import QuantumCircuit
import random
import math

from micius import MiciusClient

BASE_URL = "http://127.0.0.1:8000"

# Alice i Bob ustalają kąty dla pomiarów
# Alice: 0 → 0,  1 → π/4,  2 → π/2
# Bob:   0 → π/4, 1 → π/2,  2 → -π/4
ALICE_ANGLES = [0, math.pi / 4, math.pi / 2]
BOB_ANGLES = [math.pi / 4, math.pi / 2, -math.pi / 4]

# te same kąty → bity klucza
KEY_PAIRS = {(1, 0), (2, 1)}

# kombinacje CHSH: Alice {0, π/2} × Bob {π/4, -π/4}
CHSH_PAIRS = {(0, 0), (0, 2), (2, 0), (2, 2)}


def prepare_bell_pair() -> QuantumCircuit:
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    return qc


def basis_rotation(angle: float) -> QuantumCircuit:
    qc = QuantumCircuit(1)
    qc.ry(-angle, 0)
    return qc


def bit_from_counts(counts: dict[str, int]) -> int:
    outcome = max(counts, key=counts.get)
    return int(outcome[-1])


def measure_bell_pair(alice_basis: int, bob_basis: int) -> tuple:
    with MiciusClient(BASE_URL, caller="alice", shots=1) as alice:
        with MiciusClient(
            BASE_URL,
            caller="bob",
            session_id=alice.session_id,
            shots=1,
        ) as bob:
            # 1–2. Alice przygotowuje parę Bella i przekazuje qubit B Bobowi
            alice.sync(prepare_bell_pair())
            alice.transfer(1, "bob")

            # 4. lokalne rotacje baz, potem pomiar (execute dopina measure)
            alice.sync(basis_rotation(ALICE_ANGLES[alice_basis]))
            bob.sync(basis_rotation(BOB_ANGLES[bob_basis]))

            alice_result = alice.execute()
            bob_result = bob.execute()

            alice_bit = bit_from_counts(alice_result.counts)
            bob_bit = bit_from_counts(bob_result.counts)
            return alice_bit, bob_bit


def correlation(pairs: list) -> float:
    if len(pairs) == 0:
        return 0.0
    total = 0
    for a, b in pairs:
        # bit 0 → +1, bit 1 → -1
        total += (1 - 2 * a) * (1 - 2 * b)
    return total / len(pairs)


def bits_to_key_bytes(bits: list, length: int) -> list:
    if len(bits) < length * 8:
        raise ValueError(
            f"Za krótki klucz: potrzeba {length * 8} bitów, jest {len(bits)}. Zwiększ n."
        )
    key_bytes = []
    for c in range(length):
        byte = 0
        for b in range(8):
            byte = (byte << 1) | bits[c * 8 + b]
        key_bytes.append(byte)
    return key_bytes


n = 600

alice_bases = []
bob_bases = []
alice_results = []
bob_results = []

for i in range(n):
    # 1. przygotuj parę Bella
    # 2. Alice dostaje qubit A, Bob dostaje qubit B
    # 3. Alice i Bob losują bazy pomiarowe
    a_base = random.randint(0, 2)
    b_base = random.randint(0, 2)
    alice_bases.append(a_base)
    bob_bases.append(b_base)

    # 4. wykonaj pomiary (przez Micius)
    a_bit, b_bit = measure_bell_pair(a_base, b_base)
    alice_results.append(a_bit)
    bob_results.append(b_bit)

# 5–6. zbierz korelacje: część → klucz, część → test CHSH
key_alice = []
key_bob = []
chsh_buckets = {
    (0, 0): [],
    (0, 2): [],
    (2, 0): [],
    (2, 2): [],
}

for i in range(n):
    pair = (alice_bases[i], bob_bases[i])
    if pair in KEY_PAIRS:
        key_alice.append(alice_results[i])
        key_bob.append(bob_results[i])
    elif pair in CHSH_PAIRS:
        chsh_buckets[pair].append((alice_results[i], bob_results[i]))

# 7. policz S = E(0,π/4) + E(0,-π/4) + E(π/2,π/4) - E(π/2,-π/4)
E_00 = correlation(chsh_buckets[(0, 0)])
E_02 = correlation(chsh_buckets[(0, 2)])
E_20 = correlation(chsh_buckets[(2, 0)])
E_22 = correlation(chsh_buckets[(2, 2)])
S = E_00 + E_02 + E_20 - E_22

print("Alice bazy:   ", alice_bases)
print("Bob bazy:     ", bob_bases)
print("Alice wyniki: ", alice_results)
print("Bob wyniki:   ", bob_results)
print("Klucz Alice:  ", key_alice)
print("Klucz Bob:    ", key_bob)
print("Klucze zgodne?", key_alice == key_bob)
print(f"E(0, π/4)  = {E_00:.3f}  ({len(chsh_buckets[(0, 0)])} próbek)")
print(f"E(0,-π/4)  = {E_02:.3f}  ({len(chsh_buckets[(0, 2)])} próbek)")
print(f"E(π/2, π/4)= {E_20:.3f}  ({len(chsh_buckets[(2, 0)])} próbek)")
print(f"E(π/2,-π/4)= {E_22:.3f}  ({len(chsh_buckets[(2, 2)])} próbek)")
print(f"S = {S:.3f}")

# 8. |S| > 2 → wykrywalna kwantowa korelacja
if abs(S) > 2:
    print("|S| > 2 → kanał kwantowy OK, używamy klucza")
else:
    print("|S| ≤ 2 → brak kwantowej korelacji, odrzucamy klucz")
    raise SystemExit(1)

alice_message = "Hello, Bob!"

alice_key = bits_to_key_bytes(key_alice, len(alice_message))
bob_key = bits_to_key_bytes(key_bob, len(alice_message))

alice_cipher = []
for i in range(len(alice_message)):
    alice_cipher.append(ord(alice_message[i]) ^ alice_key[i])

print("Alice zaszyfrowana wiadomość: ", alice_cipher)

bob_message = ""
for i in range(len(alice_cipher)):
    bob_message += chr(alice_cipher[i] ^ bob_key[i])

print("Bob deszyfrowana wiadomość: ", bob_message)
