from phe import paillier

public_key, private_key = paillier.generate_paillier_keypair()


def get_decrypted_polynomial(enc_poly):
    decrypted = []

    for coef in enc_poly:
        decrypted.append(private_key.decrypt(coef))

    decrypted.reverse()
    return decrypted

def encrypted_add(p1, p2):
    max_len = max(len(p1), len(p2))
    result = []

    for i in range(max_len):
        a = p1[i] if i < len(p1) else public_key.encrypt(0)
        b = p2[i] if i < len(p2) else public_key.encrypt(0)
        result.append(a + b)

    return result

def encrypted_multiply_plain(enc_poly, plain_poly):
    result = [public_key.encrypt(0)] * (len(enc_poly) + len(plain_poly) - 1)

    for i in range(len(enc_poly)):
        for j in range(len(plain_poly)):
            result[i + j] += enc_poly[i] * plain_poly[j]

    return result
