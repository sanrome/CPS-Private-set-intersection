from phe.command_line import encrypt
from polynomials import polynomial_from_set, sample_random_polynomial
from utils import *

class Player:
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

    def calculate_lambda(self, previous_lambda, encrypted_polynomials):
        phi = encrypted_multiply_plain(self.encrypted_polynomial, sample_random_polynomial(len(self.set)))
        
        for p in encrypted_polynomials:
            phi = encrypted_add(phi, encrypted_multiply_plain(p, sample_random_polynomial(len(self.set))))

        if previous_lambda is None:
            return phi
        
        return encrypted_add(previous_lambda, phi)