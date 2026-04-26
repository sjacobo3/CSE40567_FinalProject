
import secrets

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

# Miller-Rabin primality test
def is_probable_prime(n, k=40):
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

def encrypt(plaintext, public_key):
    e, n = public_key
    return [pow(ord(c), e, n) for c in plaintext]

def decrypt(ciphertext, private_key):
    d, n = private_key
    return ''.join(chr(pow(c, d, n)) for c in ciphertext)

# larger files
def bytes_to_int(b):
    return int.from_bytes(b, byteorder='big')

def int_to_bytes(i, length):
    return i.to_bytes(length, byteorder='big')

def encrypt_file(input_path, output_path, key):
    e, n = key
    block_size = (n.bit_length() // 8) - 1

    with open(input_path, "rb") as fin, open(output_path, "w") as fout:
        while True: 
            block = fin.read(block_size)
            if not block:
                break

            block_int = int.from_bytes(block, "big")
            ciphertext = pow(block_int, e, n)
            
            # Record the block length so we can trim leading zeros during decryption
            fout.write(f"{ciphertext}:{len(block)}\n")

def decrypt_file(input_path, output_path, key):
    d, n = key
    # block_size = (n.bit_length() // 8) - 1

    with open(input_path, "r") as fin, open(output_path, "wb") as fout:
        for line in fin:
            encrypted_int, block_len = line.strip().split(":")
            encrypted_int = int(encrypted_int)
            block_len = int(block_len)

            decrypted_int = pow(encrypted_int, d, n)
            block_bytes = decrypted_int.to_bytes(block_len, "big", signed=False)

            fout.write(block_bytes)

if __name__ == "__main__":
    print("Generating 1024-bit keys...")
    pub, priv = generate_keys(1024)

    # user input
    input_img = "download.png"
    encrypted_img = "test.enc"
    decrypted_img = "recovered.png"

    print(f"Encrypting {input_img}...")
    encrypt_file(input_img, encrypted_img, pub)

    print(f"Decrypting {encrypted_img}...")
    decrypt_file(encrypted_img, decrypted_img, priv)

    print("Files encrypted and decrypted!")
