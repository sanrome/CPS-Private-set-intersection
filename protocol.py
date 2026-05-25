from polynomials import *
from utils import *
from network import MessageBus


def run_protocol(players, c=1):
    c = min(c, len(players) - 1)

    bus = MessageBus()

    #send encrypted polynomials

    for i in range(len(players)):
        sender = players[i]

        for offset in range(1, c + 1):
            receiver = players[(i + offset)]
            sender.send_encrypted_polynomial(receiver, bus)

    phis = []

    for i in range(len(players)):
        #generate random polynomials
        random_polynomials = []

        for j in range(c + 1):
            r_ij = sample_random_polynomial(len(players[i].set),bound=20)
            random_polynomials.append(r_ij)

        #receive encrypted
        received_messages = bus.receive(players[i].id)

        #own term
        phi_i = encrypted_multiply_plain(players[i].get_encrypted_polynomial(),random_polynomials[0])

        #received terms
        for j, (sender_id, encrypted_poly) in enumerate(received_messages):
            print(players[i].id,"received encrypted polynomial from",sender_id)

            if j + 1 >= len(random_polynomials):
                print("Too many messages received")
                break

            term = encrypted_multiply_plain(encrypted_poly,random_polynomials[j + 1])

            phi_i = encrypted_add(phi_i,term)

        phis.append(phi_i)


    #lambda
    lambda_poly = phis[0]

    for i in range(1, len(players)):
        print(f"Player {i} receives lambda")

        lambda_poly = encrypted_add(lambda_poly,phis[i])

    #decrypted
    decrypted = get_decrypted_polynomial(lambda_poly)

    return decrypted