from polynomials import *
from utils import *

def run_protocol(players):
    encrypted_fis = []
    c = 2
    player_polynomials = [[] for _ in range(len(players))]
    end_lambda = [0]
    # each player sends its encrypted polynomial
    for i in range(len(players)):
        for j in range(1, c):
            player_polynomials[(i + c) % len(players)].append(players[i].get_encrypted_polynomial())
    
    for i in range(len(players)):
        end_lambda = players[i].calculate_lambda(end_lambda, player_polynomials[i])

    decrypted = get_decrypted_polynomial(end_lambda)

    return decrypted

def recover_intersection(players, polynomial):
    return roots(players[0].set, polynomial)