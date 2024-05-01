def is_prime(n):
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True

p = 1
while True:
    a = 2**p - 1
    b = 2**(p-1)
    
    if p % 1 == 0:
        print("info:",p,"step")

    if is_prime(a):
        product = a * b
        print(f"For p = {p}, the product of a and b when a is prime is: {product}")
        
    p += 1

