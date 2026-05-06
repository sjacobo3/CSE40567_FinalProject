'''Imports'''
import secrets

'''Define Key Generation Functions (For Testing, Future Implementation)'''
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a
def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x1, y1 = extended_gcd(b, a % b)
    return g, y1, x1 - (a // b) * y1
def modinv(e, phi):
    g, x, _ = extended_gcd(e, phi)
    if g != 1:
        raise Exception("Modular inverse does not exist")
    return x % phi
def is_probable_prime(n, k=40):
    # Miller-Rabin primality test
    if n < 2:
        return False
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    if n in small_primes:
        return True
    for p in small_primes:
        if n % p == 0:
            return False
    r, d = 0, n - 1
    while d % 2 == 0:
        d //= 2
        r += 1
    for _ in range(k):
        a = secrets.randbelow(n - 4) + 2
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True
def generate_prime(bits=1024):
    while True:
        candidate = secrets.randbits(bits)
        candidate |= (1 << bits - 1) | 1  # ensure odd and correct size
        if any(candidate % p == 0 for p in [2, 3, 5, 7, 11, 13, 17, 19, 23]):
            continue
        if is_probable_prime(candidate):
            return candidate
def generate_keys(bits=1024):
    p = generate_prime(bits)
    q = generate_prime(bits)
    while p == q:
        q = generate_prime(bits)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537 
    if gcd(e, phi) != 1:
        return generate_keys(bits)
    d = modinv(e, phi)
    return (e, n), (d, n)

'''Define Helper Functions'''
def bytes_to_int(b):
    return int.from_bytes(b, byteorder='big')
def int_to_bytes(i, length):
    return i.to_bytes(length, byteorder='big')

'''Define RSA Functions'''
def rsa_encrypt_text(plaintext, e, n):
    # encrypt each character in plaintext
    return ":".join(str(pow(ord(c), e, n)) for c in plaintext)
def rsa_decrypt_text(ciphertext, d, n):
    # decrypt each character in ciphertext
    return "".join(chr(pow(int(c), d, n)) for c in ciphertext.split(":"))
def rsa_encrypt_file(plaintext, e, n):
    # determine block size
    block_len = (n.bit_length() // 8) - 1
    # initialize variables
    ciphertext = []
    i = 0
    # go through each block in the plaintext
    while i < len(plaintext):
        # get current block
        block = plaintext[i:i+block_len]
        # convert block to an integer to be compatible with our RSA procedures
        integer = int.from_bytes(block, "big")
        # process using RSA encryption
        encrypted = pow(integer, e, n)
        # append the encrypted int and the block length 
        ciphertext.append(f'{encrypted}:{len(block)}')
        i += block_len
    # return all encrypted blocks
    return "\n".join(ciphertext)
def rsa_decrypt_file(ciphertext, d, n):
    # split ciphertext into lines
    ciphertext = ciphertext.strip().split("\n")
    # initialize variables
    plaintext = bytearray()
    # go through each line in the ciphertext
    for line in ciphertext:
        # if ":" not in line:
        #     continue
        # retrieve encrypted and block_len
        encrypted, block_len = line.split(":")
        # process using RSA decryption
        decrypted = pow(int(encrypted), d, n)
        # append decrypted bytes to plaintext
        plaintext += decrypted.to_bytes(int(block_len), "big", signed=False)
    # return plaintext bytes
    return bytes(plaintext)

'''Main Function (For Testing)'''
# if __name__ == "__main__":
#     print("Generating 1024-bit keys...")
#     pub, priv = generate_keys(1024)

#     # user input
#     input_img = "download.png"
#     encrypted_img = "test.enc"
#     decrypted_img = "recovered.png"

#     print(f"Encrypting {input_img}...")
#     encrypt_file(input_img, encrypted_img, pub)

#     print(f"Decrypting {encrypted_img}...")
#     decrypt_file(encrypted_img, decrypted_img, priv)

#     print("Files encrypted and decrypted!")
