import secrets

# a polynomial is a list of integers representing the increasing degree coeficients 

def sample_random_polynomial(k, paillier_public_key):
    plaintext_space_upper_bound = paillier_public_key.n 
    
    random_coefficients = []
    for _ in range(k + 1):
        random_coeff = secrets.randbelow(plaintext_space_upper_bound)
        random_coefficients.append(random_coeff)
        
    return random_coefficients

def polynomial_from_set(set):
    n = len(set)
    polynomial = [1] + [0] * n
    
    for i, e in enumerate(set):
        for j in range(i + 1, 0, -1):
            polynomial[j] = polynomial[j] - e * polynomial[j - 1]
            
    return polynomial

# returns if the element is a root of the polynomial, the quotient and reminder of the polynomial division
def ruffini_divide(polynomial, element):
    current_val = polynomial[0]
    quotient = [current_val]

    for i in range(1, len(polynomial)):
        current_val = polynomial[i] + (current_val * element)
        quotient.append(current_val)

    reminder = quotient.pop()
    return quotient, reminder

# returns the elements from the multiset that are roots of the given polynomial
def roots(set, polynomial):
    rta = []
    for e in set:
        quotient, reminder = ruffini_divide(polynomial, e)
        if(reminder == 0):
            # replace the polynomial with the factored version without the root
            polynomial = quotient
            rta.append(e)
    return rta

print(polynomial_from_set([1,2]))
print(ruffini_divide([1,-3,2],1))
print(roots([1,1,1,4],[1, -2, 1]))