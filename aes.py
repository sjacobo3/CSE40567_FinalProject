import os

# 1. s-box (substitution box) - figure 7
# derived from the multiplicative inverse over GF(2^8)
SBOX = [
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
]

# round constants for key expansion
RCON = [0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36]

def subWord(word):
    # apply s-box substitution to a 4-byte word
    return [SBOX[b] for b in word]

def rotWord(word):
    # perform cyclic permutation of 4-byte word
    return word[1:] + word[:1]

def keyExpansion(key):
    # expands a 128-bit key into 11 key rounds (176 bytes total)
    w = []
    
    # first 4 words are the key itself
    for i in range(4):
        w.append([key[4*i], key[4*i+1], key[4*i+2], key[4*i+3]])

    for i in range(4, 44):
        temp = w[i-1]
        if i % 4 == 0:
            # apply rotWord, subWord, and XOR with Rcon
            temp = [b ^ r for b, r in zip(subWord(rotWord(temp)), [RCON[i//4], 0, 0, 0])]

        # XOR with the word 4 positions back
        new_word = [b1 ^ b2 for b1, b2 in zip(w[i-4], temp)]
        w.append(new_word)

    # flatten the list of words into a list of round keys
    round_keys = []
    for i in range(0, 44, 4):
        round_keys.append(w[i:i+4])
    
    return round_keys

def addRoundKey(state, round_keys):
    # XORs the state with the round keys
    for c in range(4):
        for r in range(4):
            state[r][c] ^= round_keys[c][r]

def subBytes(state):
    # non-linear byte substitution using s-box
    for r in range(4):
        for c in range(4):
            state[r][c] = SBOX[state[r][c]]

def shiftRows(state):
    # cyclically shifts the last three rows of the state
    state[1] = state[1][1:] + state[1][:1]  # shift row 1 by 1
    state[2] = state[2][2:] + state[2][:2]  # shift row 2 by 2
    state[3] = state[3][3:] + state[3][:3]  # shift row 3 by 3

def xtime(a):
    # multiplication by 0x02 in GF(2^8)
    return ((a << 1) ^ 0x1b) & 0xff if (a & 0x80) else (a << 1) & 0xff

def mixColumns(state):
    # mixes the columns of the state using Galois Field math
    for c in range(4):
        s0, s1, s2, s3 = state[0][c], state[1][c], state[2][c], state[3][c]
        # formula: s'0,c = ({02}*s0, c) XOR ({03}*s1, c) XOR (s2, c) XOR (s3, c)
        state[0][c] = xtime(s0) ^ (xtime(s1) ^ s1) ^ s2 ^ s3
        state[1][c] = s0 ^ xtime(s1) ^ (xtime(s2) ^ s2) ^ s3
        state[2][c] = s0 ^ s1 ^ xtime(s2) ^ (xtime(s3) ^ s3)
        state[3][c] = (xtime(s0) ^ s0) ^ s1 ^ s2 ^ xtime(s3)

def text_to_bytes(text):
    return list(text.encode('utf-8'))

def bytes_to_text(byte_list):
    return bytes(byte_list).decode('utf-8')

def pad(data):
    pad_len = 16 - (len(data) % 16)
    return data + [pad_len] * pad_len

def unpad(data):
    pad_len = data[-1]
    return data[:-pad_len]

def xor_bytes(a, b):
    return [x ^ y for x, y in zip(a, b)]

def encrypt(plaintext, key):
    # convert plaintext to 4x4 state matrix (column-major order)
    state = [[0]*4 for _ in range(4)]
    for r in range(4):
        for c in range(4):
            state[r][c] = plaintext[r + (4*c)]

    # key expansion
    round_keys = keyExpansion(key)

    # initial round
    addRoundKey(state, round_keys[0])

    # round 1 to 9
    for round_idx in range(1, 10):
        subBytes(state)
        shiftRows(state)
        mixColumns(state)
        addRoundKey(state, round_keys[round_idx])

    # final round w/o mixColumns
    subBytes(state)
    shiftRows(state)
    addRoundKey(state, round_keys[10])

    # convert state back to flat list
    output = [0] * 16
    for r in range(4):
        for c in range(4):
            output[r + (4*c)] = state[r][c]

    return output

INV_SBOX = [0] * 256
for i in range(256):
    INV_SBOX[SBOX[i]] = i

def invSubBytes(state):
    for r in range(4):
        for c in range(4):
            state[r][c] = INV_SBOX[state[r][c]]

def invShiftRows(state):
    state[1] = state[1][-1:] + state[1][:-1]
    state[2] = state[2][-2:] + state[2][:-2]
    state[3] = state[3][-3:] + state[3][:-3]

def gmul(a, b):
    p = 0
    for _ in range(8):
        if b & 1:
            p ^= a
        hi_bit = a & 0x80
        a = (a << 1) & 0xff
        if hi_bit: 
            a ^= 0x1b
        b >>= 1
    return p

def invMixColumns(state):
    for c in range(4):
        s0, s1, s2, s3 = state[0][c], state[1][c], state[2][c], state[3][c]

        state[0][c] = gmul(s0, 0x0e) ^ gmul(s1, 0x0b) ^ gmul(s2, 0x0d) ^ gmul(s3, 0x09)
        state[1][c] = gmul(s0, 0x09) ^ gmul(s1, 0x0e) ^ gmul(s2, 0x0b) ^ gmul(s3, 0x0d)
        state[2][c] = gmul(s0, 0x0d) ^ gmul(s1, 0x09) ^ gmul(s2, 0x0e) ^ gmul(s3, 0x0b)
        state[3][c] = gmul(s0, 0x0b) ^ gmul(s1, 0x0d) ^ gmul(s2, 0x09) ^ gmul(s3, 0x0e)

def decrypt(ciphertext, key):
    # convert cipher to state matrix
    state = [[0]*4 for _ in range(4)]
    for r in range(4):
        for c in range(4):
            state[r][c] = ciphertext[r + (4*c)]
    
    # key expansion
    round_keys = keyExpansion(key)

    # initial round
    addRoundKey(state, round_keys[10])

    # rounds 9 to 1
    for round_idx in range(9, 0, -1):
        invShiftRows(state)
        invSubBytes(state)
        addRoundKey(state, round_keys[round_idx])
        invMixColumns(state)

    # final round w/o mixColumns
    invShiftRows(state)
    invSubBytes(state)
    addRoundKey(state, round_keys[0])

    # flatten state back to list
    output = [0] * 16
    for r in range(4):
        for c in range(4):
            output[r + (4*c)] = state[r][c]

    return output

def encrypt_text(plaintext, key):
    data = text_to_bytes(plaintext)
    data = pad(data)

    iv = list(os.urandom(16))   # random 16-byte initialization vector
    ciphertext = []

    prev = iv
    for i in range(0, len(data), 16):
        block = data[i:i+16]
        block = xor_bytes(block, prev)
        enc = encrypt(block, key)
        ciphertext.extend(enc)
        prev = enc
    return iv + ciphertext

def decrypt_text(ciphertext, key):
    iv = ciphertext[:16]
    data = ciphertext[16:]

    plaintext = []
    prev = iv

    for i in range(0, len(data), 16):
        block = data[i:i+16]
        dec = decrypt(block, key)
        dec = xor_bytes(dec, prev)
        plaintext.extend(dec)
        prev = block
    
    plaintext = unpad(plaintext)
    return bytes_to_text(plaintext)

if __name__ == "__main__":
    # example usage
    key = [
    0x2b,0x7e,0x15,0x16,
    0x28,0xae,0xd2,0xa6,
    0xab,0xf7,0x15,0x88,
    0x09,0xcf,0x4f,0x3c
    ]

    user_input = "Hello AES"
    ciphertext = encrypt_text(user_input, key)
    print("Ciphertext:", ciphertext)

    plaintext = decrypt_text(ciphertext, key)
    print("Decrypted: ", plaintext)
