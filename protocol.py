from polynomials import *
from utils import *

def run_protocol(players, c=1):
    c = min(c, len(players) - 1)  # safety: c can't exceed n-1
    player_polynomials = [[] for _ in range(len(players))]
   # end_lambda = [0]
    # each player sends its encrypted polynomial to the next c players in the ring
    for i in range(len(players)):
        for j in range(1, c + 1):                          # range(1, c+1) = [1, 2, ..., c]
             player_polynomials[(i + j) % len(players)].append(players[i].get_encrypted_polynomial())
             
    end_lambda = players[0].calculate_lambda(None, player_polynomials[0])

    for i in range(1, len(players)):
        end_lambda = players[i].calculate_lambda(end_lambda, player_polynomials[i])

    decrypted = get_decrypted_polynomial(end_lambda)

    return decrypted

def recover_intersection(players, polynomial):
    return roots(players[0].set, polynomial)