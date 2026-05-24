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

def is_root(polynomial, element):
    current_val = polynomial[0]
    
    for i in range(1, len(polynomial)):
        current_val = polynomial[i] + (current_val * element)
    
    return current_val == 0

# returns the elements from the set that are roots of the given polynomial
def roots(set, polynomial):
    rta = []
    for e in set:
        if(is_root(polynomial, e)):
            rta.append(e)
    return rta

print(polynomial_from_set([1,2]))
print(is_root([1,-3,2],34))
print(roots([1,25,4],[1, -3, 2]))