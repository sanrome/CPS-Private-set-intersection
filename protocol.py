from polynomials import *
from utils import *

def run_protocol(players, c=1):
    """
    Implements the Set-Intersection-HBC protocol from Figure 1 of
    Kissner & Song, 'Privacy-Preserving Set Operations', Crypto 2005.

    Security model: honest-but-curious adversaries (Section 3.1)
    Correctness:    Theorem 4
    Security:       Theorem 5, relies on semantic security of Paillier (Section 3.2)
    
    Parameters:
        players: list of Player objects, each holding a private set S_i
        c:       collusion threshold, up to c players may collude
                 and the protocol remains secure (must be c < n)
    
    Protocol steps (matching Figure 1 numbering):
        Step 1: Each player encrypts f_i and sends to c neighbours
        Step 2: Each player computes phi_i (blinded combination)
        Step 3: Players sum phi_i values to get lambda
        Step 4: Group decryption of lambda → polynomial p
        Step 5: Each player finds roots of p in their own set
    """
    c = min(c, len(players) - 1)  # safety: c can't exceed n-1
    player_polynomials = [[] for _ in range(len(players))]

    # each player sends its encrypted polynomial to the next c players in the ring
    for i in range(len(players)):
        for j in range(1, c + 1):                          # range(1, c+1) = [1, 2, ..., c]
             player_polynomials[(i + j) % len(players)].append(players[i].get_encrypted_polynomial())

    end_lambda = players[0].calculate_lambda(None, player_polynomials[0])

    for i in range(len(players)):
        end_lambda = players[i].calculate_lambda(end_lambda, player_polynomials[i])

    decrypted = get_decrypted_polynomial(end_lambda)

    return decrypted

def recover_intersection(players, polynomial):
    return roots(players[0].set, polynomial)