import math

def estimate_pi():
    factor = (2*np.sqrt(2))/9801
    small = True
    k = 0
    summation = 0
    while small is True:
        main_term = (math.factorial(4*k)*(1103+26390*k))/((math.factorial(k)**4)*396**(4*k))
        k += 1
        if main_term < 10**-15:
            small = False
        summation += main_term
    pi_estimate = 1/(factor*summation)
    return pi_estimate

print("Function estimate:", estimate_pi())
print("Math.pi calculation:", math.pi)