from phe.command_line import encrypt
from polynomials import polynomial_from_set
from utils import *
from polynomials import *
class Player:
    c = 5
    def __init__(self, player_id, private_set, public_key):
        self.id = player_id
        self.set = private_set
        self.public_key = public_key
        self.polynomial = polynomial_from_set(private_set)
        encrypted_polynomial = []
        for coef in self.polynomial:
            encrypted_polynomial.append(self.public_key.encrypt(int(coef)))
        self.encrypted_polynomial = encrypted_polynomial

    def get_encrypted_polynomial(self):
        return self.encrypted_polynomial

    def calculate_lambda(self):
        phis = []

        for i in range(len(players)):
            # generate random polynomials
            random_polynomials = []

            for j in range(c + 1):
                r_ij = sample_random_polynomial(len(players[i].set), bound=20)
                random_polynomials.append(r_ij)

            # receive encrypted
            received_messages = bus.receive(players[i].id)

            # own term
            phi_i = encrypted_multiply_plain(players[i].get_encrypted_polynomial(), random_polynomials[0])

            # received terms
            for j, (sender_id, encrypted_poly) in enumerate(received_messages):
                print(players[i].id, "received encrypted polynomial from", sender_id)

                if j + 1 >= len(random_polynomials):
                    print("Too many messages received")
                    break

                term = encrypted_multiply_plain(encrypted_poly, random_polynomials[j + 1])

                phi_i = encrypted_add(phi_i, term)

            phis.append(phi_i)

        # lambda
        lambda_poly = phis[0]

        for i in range(1, len(players)):
            print(f"Player {i} receives lambda")

            lambda_poly = encrypted_add(lambda_poly, phis[i])
