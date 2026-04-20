import random

def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a%b)

def prime_finder():
    test_number = random.randrange(10, 100)
    for i in range(2, test_number):
        if test_number % i == 0:
            return prime_finder()
    return test_number

def generate_keys():
    p = prime_finder()
    q = prime_finder()
    n = p * q
    phi = (p-1) * (q-1)

    pub_keys = []
    for i in range(2, phi):
        if gcd(i, phi) == 1 and gcd(i, n) == 1:
            pub_keys.append(i)
        if len(pub_keys) >= 100:
            break

    e = random.choice(pub_keys)

    priv_keys = []
    i = 2
    while len(priv_keys) < 2:
        if i * e % phi == 1:
            priv_keys.append(i)
        i += 1

    d = random.choice(priv_keys)

    # print(f"Public Keys: ({e}, {n})\nPrivate Keys: ({d}, {n})")
    return (e, n), (d, n)

def encrypt(plaintext, public_key):
    e, n = public_key
    return [pow(ord(char), e, n) for char in plaintext]

def decrypt(ciphertext, private_key):
    d, n = private_key
    return ''.join([chr(pow(char, d, n)) for char in ciphertext])


if __name__ == "__main__":
    public_key, private_key = generate_keys()

    # gui tool will take in user input
    user_input = input("Enter a message: ")
    ciphertext = encrypt(user_input, public_key)
    decryptedtext = decrypt(ciphertext, private_key)

    print("Encrypted: ", ciphertext)
    print("Decrypted: ", decryptedtext)

