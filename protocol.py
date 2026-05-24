from polynomials import *
from utils import *

def run_protocol(players):
    encrypted_fis = []

    for p in players:
        encrypted_fis.append(p.get_encrypted_polynomial())

    phis = []

    for i in range(len(players)):
        ri = sample_random_polynomial(len(players[i].set),bound=20)
        phi_i = encrypted_multiply_plain(encrypted_fis[i],ri)
        phis.append(phi_i)

    total = phis[0]

    for i in range(1, len(phis)):
        total = encrypted_add(total, phis[i])

    decrypted = get_decrypted_polynomial(total)

    return decrypted

def recover_intersection(players, polynomial):
    intersection = set(players[0].set)

    for player in players:
        valid = set()

        for element in player.set:
            if is_root(polynomial, element):
                valid.add(element)

        intersection = intersection.intersection(valid)

    return list(intersection)