'''Imports'''
import string

'''Define Global Variables'''
ALPHA_l2n = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9, 'K': 10, 'L': 11, 'M': 12, 'N': 13, 'O': 14, 'P': 15, 'Q': 16, 'R': 17, 'S': 18, 'T': 19, 'U': 20, 'V': 21, 'W': 22, 'X': 23, 'Y': 24, 'Z': 25}
ALPHA_n2l = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J', 10: 'K', 11: 'L', 12: 'M', 13: 'N', 14: 'O', 15: 'P', 16: 'Q', 17: 'R', 18: 'S', 19: 'T', 20: 'U', 21: 'V', 22: 'W', 23: 'X', 24: 'Y', 25: 'Z'}
# i used the code below to print what i copied into ALPHA_n2l (switch n and l for ALPHA_l2n)
# uppercase_alpha = string.ascii_uppercase
# for n, l in enumerate(uppercase_alpha):
#     print(f'{n}: \'{l}\',', end=" ")

'''Define Vigenère Functions'''
def vig_encrypt(plaintext, key):
    # prepare and declare variables
    plaintext = plaintext.upper()
    key = key.upper()
    ciphertext = ""
    # shift each letter of the plaintext and add to ciphertext, keeping chars that aren't letters
    for n, c in enumerate(plaintext):
        if c in string.ascii_uppercase:
            cipher_l = (ALPHA_l2n[c] + ALPHA_l2n[key[n % len(key)]]) % 26
            ciphertext += ALPHA_n2l[cipher_l]
        else:
            ciphertext += c
    return ciphertext

def vig_decrypt(ciphertext, key):
    # prepare and declare variables
    ciphertext = ciphertext.upper()
    key = key.upper()
    plaintext = ""
    # shift each letter of the ciphertext and add to plaintext, keeping chars that aren't letters
    for n, c in enumerate(ciphertext):
        if c in string.ascii_uppercase:
            plain_l = (ALPHA_l2n[c] - ALPHA_l2n[key[n % len(key)]]) % 26
            plaintext += ALPHA_n2l[plain_l]
        else:
            plaintext += c
    return plaintext

'''Main Function (For Testing)'''
# if __name__ == '__main__':
#     print(vig_decrypt('TTEUMGQNDVEOIOLEDIREMQTGSDAFDRCDYOXIZGZPPTAAITUCSIXFBXYSUNFESQRHISAFHRTQRVSVQNBEEEAQGIBHDVSNARIDANSLEXESXEDSNJAWEXAODDHXEYPKSYEAESRYOETOXYZPPTAAITUCRYBETHXUFINR', 'AMAZE'))
#     print(vig_encrypt('thevigenerecipherisamethodofencryptingalphabetictextbyusingaseriesofinterwovencaesarciphersbasedonthelettersofakeyworditemploysaformofpolyalphabeticsubstitution','AMAZE'))