import typing as tp


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    if len(plaintext) == 0:
        return plaintext
    list = []
    for i in range(len(plaintext)):
        a = ord(plaintext[i]) + shift
        if (65 <= a <= 90) or (97 <= a <= 122):
            list.append(a)
        elif 32 <= a <= 64:
            list.append(a - shift)
        else:
            list.append(a - 26)
    ciphertext = ''.join([chr(i) for i in list])
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    if len(ciphertext) == 0:
        return ciphertext
    list = []
    for i in range(len(ciphertext)):
        a = ord(ciphertext[i]) - shift
        if (65 <= a <= 90) or (97 <= a <= 122):
            list.append(a)
        elif 32 <= a <= 61:
            list.append(a + shift)
        else:
            list.append(a + 26)
    plaintext = ''.join([chr(i) for i in list])
    return plaintext



def caesar_breaker_brute_force(ciphertext: str, dictionary: tp.Set[str]) -> int:
    best_shift = 0
    return best_shift

print(decrypt_caesar("SBWKRQ", 3))
print(encrypt_caesar("PYTHON", 3))