'''Define Global Variables'''
left_shifts = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]
permuted_choice_1 = [
    57, 49, 41, 33, 25, 17, 9,
    1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27,
    19, 11, 3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29,
    21, 13, 5, 28, 20, 12, 4
    ]
permuted_choice_2 = [
    14, 17, 11, 24, 1, 5,
    3, 28, 15, 6, 21, 10,
    23, 19, 12, 4, 26, 8,
    16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
    ]
initial_permutation = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
    ]
e_bit_selection = [
    32, 1, 2, 3, 4, 5,
    4, 5, 6, 7, 8, 9,
    8, 9, 10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32, 1
    ]
s_boxes = [
    [ # S1
        [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
        [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
        [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
    ],
    [ # S2
        [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
        [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
        [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
        [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
    ],
    [ # S3
        [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
        [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
        [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
        [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
    ],
    [ # S4
        [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
        [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
        [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
        [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
    ],
    [ # S5
        [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
        [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
        [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
        [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
    ],
    [ # S6
        [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
        [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
        [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
        [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
    ],
    [ # S7
        [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
        [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
        [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
        [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
    ],
    [  # S8
        [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
        [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
        [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
        [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
    ]
]
f_func_permutation = [
    16, 7, 20, 21,
    29, 12, 28, 17,
    1, 15, 23, 26,
    5, 18, 31, 10,
    2, 8, 24, 14,
    32, 27, 3, 9,
    19, 13, 30, 6,
    22, 11, 4, 25
    ]
final_permutation = [
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9, 49, 17, 57, 25
    ]

'''Define DES Functions'''
def permute(bits, PCn):
    # permute the bits based on the permuted choice PCn
    return "".join(bits[i-1] for i in PCn)
def xor(b1, b2):
    # xor the bits in blocks b1 and b2
    return "".join("0" if b1[i] == b2[i] else "1" for i in range(len(b1)))
def f(Rn, Kn):
    # expand Rn from 32 bits to 48 bits
    E_Rn = permute(Rn, e_bit_selection)
    # XOR the output E(Rn) with the key Kn
    Kn_E_Rn = xor(Kn, E_Rn)
    # get the s box output
    S_Kn_E_Rn = sbox(Kn_E_Rn)
    return S_Kn_E_Rn
def sbox(Kn_E_Rn):
    S_Kn_E_Rn = ""
    for i in range(8):
        # split Kn_E_Rn into 8 blocks Bi, each having 6 bits
        B = Kn_E_Rn[i*6:(i+1)*6]
        # row is from the 1st and 6th bits
        row = int(B[0] + B[5], 2)
        # column is from the 2nd and 5th bits
        col = int(B[1:5], 2)
        # retrieve the s box output for the current block
        S_B = s_boxes[i][row][col]
        # add the current output to the final output in binary
        S_Kn_E_Rn += format(S_B, "04b")
    # apply the permutation P to S_Kn_E_Rn
    P_S_Kn_E_Rn = permute(S_Kn_E_Rn, f_func_permutation)
    return P_S_Kn_E_Rn
def generate_subkeys(K):
    # permutate the original 64-bit key to obtain the 56-bit permutation
    KPLUS = permute(K, permuted_choice_1)
    # split K+ into left and right halves, C_0 and D_0, where each half has 28 bits
    C0 = KPLUS[:28]
    D0 = KPLUS[28:]
    # generate the 16 blocks
    C = [None] * 17
    D = [None] * 17
    CD = [None] * 16
    C[0] = C0
    D[0] = D0
    for n in range(16):
        C[n+1] = C[n][left_shifts[n]:] + C[n][:left_shifts[n]]
        D[n+1] = D[n][left_shifts[n]:] + D[n][:left_shifts[n]]
        CD[n] = C[n+1] + D[n+1]
    subkeys = [None] * 16
    for n in range(16):
        subkeys[n] = permute(CD[n], permuted_choice_2)
    return subkeys
def des(block, subkeys):
    # encode each 64-bit block of data
    # apply the initial permutation to the ciphertext CT
    IP = permute(block, initial_permutation)
    # split the initial permutation into L0 and R0, each 32 bits
    L0 = IP[:32]
    R0 = IP[32:]
    # produce 32-bit blocks
    L = [None] * 17
    R = [None] * 17
    L[0] = L0
    R[0] = R0
    for n in range(16):
        # obtain the values for Li and Ri
        L[n+1] = R[n]
        f_output = f(R[n], subkeys[n])
        R[n+1] = xor(L[n], f_output)
    # reverse the order of the 16th block -> R16L16
    R16L16 = R[16] + L[16]
    # apply the final permutation IP^-1 to R16L16 to obtain the binary message
    M_bits = permute(R16L16, final_permutation)
    return M_bits

'''Define Helper Functions'''
def pad_text(text):
    # pad plaintext to ensure it is compatible with 3DES
    len_padding = 8 - (len(text) % 8)
    padded = text + bytes([len_padding] * len_padding)
    return padded
def unpad_text(text):
    # unpad decrypted text
    len_padding = text[-1]
    if (len_padding < 1) or (len_padding > 8):
        raise ValueError("Invalid Padding")
    return text[:-len_padding]
def bytes_to_bin(data):
    # convert bytes to binary
    converted = ''.join(format(byte, '08b') for byte in data)
    return converted
def bin_to_bytes(data):
    converted = bytes(int(data[i:i+8], 2) for i in range(0, len(data), 8))
    return converted
def validate_key(K):
    # ensure the keys are compatible with 3DES (64-bit binary keys)
    if (len(K) != 64) or not(all(c in '01' for c in K)):
        return False
    return True

'''Define 3DES Functions'''
def tripdes_encrypt(plaintext, K1, K2, K3):
    # validate the keys
    if (not validate_key(K1)) or (not validate_key(K2)) or (not validate_key(K3)):
        raise ValueError("Invalid Key")
    # if encrypting a string, read as bytes
    if isinstance(plaintext, str):
        plaintext = plaintext.encode('utf-8')
    # pad the plaintext to ensure it's compatible with 3DES
    padded = pad_text(plaintext)
    # divide the padded plaintext into blocks
    blocks = [bytes_to_bin(padded[i:i+8]) for i in range(0, len(padded), 8)]
    # generate the subkeys
    subK1 = generate_subkeys(K1)
    subK2 = generate_subkeys(K2)
    subK3 = generate_subkeys(K3)
    # apply EDE to each block
    ciphertext = []
    for block in blocks:
        apply_K1 = des(block, subK1)
        apply_K2 = des(apply_K1, subK2[::-1])
        apply_K3 = des(apply_K2, subK3)
        ciphertext.append(apply_K3)
    ciphertext = "".join(ciphertext)
    return ciphertext
def tripdes_decrypt(ciphertext, K1, K2, K3, is_file):
    # validate the keys
    if (not validate_key(K1)) or (not validate_key(K2)) or (not validate_key(K3)):
        raise ValueError("Invalid Key")
    # if decrypting bytes, read as a string
    if isinstance(ciphertext, bytes):
        ciphertext = ciphertext.decode('utf-8')
    # divide the ciphertext into blocks
    blocks = [ciphertext[i:i+64] for i in range(0, len(ciphertext), 64)]
    # generate the subkeys
    subK1 = generate_subkeys(K1)
    subK2 = generate_subkeys(K2)
    subK3 = generate_subkeys(K3)
    # apply DED to each block
    plaintext_bin = []
    for block in blocks:
        apply_K3 = des(block, subK3[::-1])
        apply_K2 = des(apply_K3, subK2)
        apply_K1 = des(apply_K2, subK1[::-1])
        plaintext_bin.append(apply_K1)
    plaintext_bin = "".join(plaintext_bin)
    # unpad the data to obtain the plaintext
    plaintext = unpad_text(bin_to_bytes(plaintext_bin))
    # if decrypting a file, return bytes; otherwise, decode
    if is_file:
        return plaintext
    return plaintext.decode('utf-8')

'''Main Function (For Testing)'''
# if __name__ == '__main__':
#     K1 = "0000000011111111000000001111111100000000111111110000000011111111"
#     K2 = "0000000000000000000000000000000000000000000000000000000000000000"
#     K3 = "1111111111111111111111111111111111111111111111111111111111111111"
#     plaintext = "hello world"

#     print(f'plaintext: {plaintext}')

#     ciphertext = tripdes_encrypt(plaintext, K1, K2, K3)
#     print(f'ciphertext: {ciphertext}')

#     decrypted = tripdes_decrypt(ciphertext, K1, K2, K3, False)
#     print(f'decrypted: {decrypted}')