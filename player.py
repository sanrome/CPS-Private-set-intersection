from phe.command_line import encrypt
from polynomials import polynomial_from_set
class Player:
    c = 5
    def __init__(self, player_id, private_set, public_key):
        self.id = player_id
        self.set = private_set
        self.public_key = public_key
        self.polynomial = polynomial_from_set(private_set)

    def get_encrypted_polynomial(self):
        rta = []
        for coef in self.polynomial:
            rta.append(self.public_key.encrypt(int(coef)))
        return rta

