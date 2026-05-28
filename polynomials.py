import secrets

#CONVENTION: a polynomial is a list of integers representing the decreasing degree coefficients 
BOUND = 2**32 ## 2^32 gives ~4 billion possible values per coefficient which is astronomically harder to brute-force than bound=20 

def sample_random_polynomial(k, bound=BOUND):
    coefficients = []

    for _ in range(k + 1):
        coeff = secrets.randbelow(2 * bound + 1) - bound
        coefficients.append(coeff)

    return coefficients

def polynomial_from_set(elements):
    n = len(elements)
    polynomial = [1] + [0] * n
    
    for i, e in enumerate(elements):
        for j in range(i + 1, 0, -1):
            polynomial[j] = polynomial[j] - e * polynomial[j - 1]
            
    return polynomial

# returns the quotient and reminder of the polynomial division
def ruffini_divide(polynomial, element):
    current_val = polynomial[0]
    quotient = [current_val]

    for i in range(1, len(polynomial)):
        current_val = polynomial[i] + (current_val * element)
        quotient.append(current_val)

    reminder = quotient.pop()
    return quotient, reminder

# returns the elements from the multiset that are roots of the given polynomial
def roots(elements, polynomial):
    rta = []
    for e in elements:
        quotient, reminder = ruffini_divide(polynomial, e)
        if(reminder == 0):
            # replace the polynomial with the factored version without the root
            polynomial = quotient
            rta.append(e)
    return rta

def multiply_polynomials(p1, p2):
    result = [0] * (len(p1) + len(p2) - 1)

    for i in range(len(p1)):
        for j in range(len(p2)):
            result[i+j] += p1[i] * p2[j]

    return result

def add_polynomials(p1, p2):
    max_len = max(len(p1), len(p2))
    p1 = p1 + [0]*(max_len-len(p1))
    p2 = p2 + [0]*(max_len-len(p2))

    return [p1[i] + p2[i] for i in range(max_len)]
