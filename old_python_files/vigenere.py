import string

ALPHA_l2n = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9, 'k': 10, 'l': 11, 'm': 12, 'n': 13, 'o': 14, 'p': 15, 'q': 16, 'r': 17, 's': 18, 't': 19, 'u': 20, 'v': 21, 'w': 22, 'x': 23, 'y': 24, 'z': 25}
ALPHA_n2l = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h', 8: 'i', 9: 'j', 10: 'k', 11: 'l', 12: 'm', 13: 'n', 14: 'o', 15: 'p', 16: 'q', 17: 'r', 18: 's', 19: 't', 20: 'u', 21: 'v', 22: 'w', 23: 'x', 24: 'y', 25: 'z'}
# i used the code below to print what i copied into ALPHA_n2l (switch n and l for ALPHA_l2n)
# lowercase_alpha = string.ascii_lowercase
# for n, l in enumerate(lowercase_alpha):
#     print(f'{n}: \'{l}\',', end=" ")

def vig_encrypt(plaintext, key):
    # prepare and declare variables
    plaintext = plaintext.lower()
    key = key.lower()
    ciphertext = ""
    # shift each letter of the plaintext and add to ciphertext, keeping chars that aren't letters
    for n, c in enumerate(plaintext):
        if c in string.ascii_lowercase:
            cipher_l = (ALPHA_l2n[c] + ALPHA_l2n[key[n % len(key)]]) % 26
            ciphertext += ALPHA_n2l[cipher_l]
        else:
            ciphertext += c
    return ciphertext

def vig_decrypt(ciphertext, key):
    # prepare and declare variables
    ciphertext = ciphertext.lower()
    key = key.lower()
    plaintext = ""
    # shift each letter of the ciphertext and add to plaintext, keeping chars that aren't letters
    for n, c in enumerate(ciphertext):
        if c in string.ascii_lowercase:
            plain_l = (ALPHA_l2n[c] - ALPHA_l2n[key[n % len(key)]]) % 26
            plaintext += ALPHA_n2l[plain_l]
        else:
            plaintext += c
    return plaintext

# i used the code below for testing
# if __name__ == '__main__':
    # print(vig_decrypt('TTEUMGQNDVEOIOLEDIREMQTGSDAFDRCDYOXIZGZPPTAAITUCSIXFBXYSUNFESQRHISAFHRTQRVSVQNBEEEAQGIBHDVSNARIDANSLEXESXEDSNJAWEXAODDHXEYPKSYEAESRYOETOXYZPPTAAITUCRYBETHXUFINR', 'AMAZE'))
    # print(vig_encrypt('thevigenerecipherisamethodofencryptingalphabetictextbyusingaseriesofinterwovencaesarciphersbasedonthelettersofakeyworditemploysaformofpolyalphabeticsubstitution','AMAZE'))