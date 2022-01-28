from math import sqrt

def factor(a, b, c):
    disc = sqrt(b**2-(4*a*c))
    return (-b + disc)/(2*a), (-b - disc)/(2*a)

print(factor(2, -7, 4)) 