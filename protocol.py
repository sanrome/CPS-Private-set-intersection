from polynomials import *
from utils import *
from network import MessageBus


def run_protocol(players, c=1):

    c = min(c, len(players) - 1)

    bus = MessageBus()

    # ==========================================
    # STEP 1:
    # SEND ENCRYPTED POLYNOMIALS
    # ==========================================

    for i in range(len(players)):

        sender = players[i]

        encrypted_poly = (
            sender.get_encrypted_polynomial()
        )

        for offset in range(1, c + 1):

            receiver = players[
                (i + offset) % len(players)
            ]

            bus.send(
                sender.id,
                receiver.id,
                encrypted_poly
            )

    # ==========================================
    # STEP 2:
    # BUILD PHI_i
    # ==========================================

    phis = []

    for i in range(len(players)):

        # --------------------------------------
        # GENERATE RANDOM POLYNOMIALS
        # r_i,0 ... r_i,c
        # --------------------------------------

        random_polynomials = []

        for j in range(c + 1):

            r_ij = sample_random_polynomial(
                len(players[i].set),
                bound=20
            )

            random_polynomials.append(r_ij)

        # --------------------------------------
        # RECEIVE ENCRYPTED POLYNOMIALS
        # --------------------------------------

        received_messages = bus.receive(
            players[i].id
        )

        # ======================================
        # START WITH OWN TERM
        # phi_i = f_i * r_i,0
        # ======================================

        phi_i = encrypted_multiply_plain(
            players[i].get_encrypted_polynomial(),
            random_polynomials[0]
        )

        # ======================================
        # ADD RECEIVED TERMS
        # phi_i += f_j * r_i,j
        # ======================================

        for j, (sender_id, encrypted_poly) in enumerate(received_messages):

            print(
                players[i].id,
                "received encrypted polynomial from",
                sender_id
            )

            # ----------------------------------
            # PREVENT INDEX OVERFLOW
            # ----------------------------------

            if j + 1 >= len(random_polynomials):

                print(
                    "Too many messages received"
                )

                break

            term = encrypted_multiply_plain(
                encrypted_poly,
                random_polynomials[j + 1]
            )

            phi_i = encrypted_add(
                phi_i,
                term
            )

        # ======================================
        # SAVE PHI_i
        # ======================================

        phis.append(phi_i)

    # ==========================================
    # STEP 3:
    # LAMBDA AGGREGATION
    # ==========================================

    print("\nNumber of phis:", len(phis))

    lambda_poly = phis[0]

    for i in range(1, len(players)):

        print(
            f"Player {i} receives lambda"
        )

        lambda_poly = encrypted_add(
            lambda_poly,
            phis[i]
        )

    # ==========================================
    # STEP 4:
    # DECRYPT FINAL POLYNOMIAL
    # ==========================================

    decrypted = get_decrypted_polynomial(
        lambda_poly
    )

    return decrypted