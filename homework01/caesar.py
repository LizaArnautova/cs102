def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    if len(plaintext) == 0:
        return plaintext
    list_ = []
    for i in range(len(plaintext)):
        a = ord(plaintext[i]) + shift
        if (65 <= a <= 90) or (97 <= a <= 122):
            list_.append(a)
        elif 32 <= a <= 64:
            list_.append(a - shift)
        else:
            list_.append(a - 26)
    ciphertext = "".join([chr(i) for i in list_])
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    if len(ciphertext) == 0:
        return ciphertext
    list_ = []
    for i in range(len(ciphertext)):
        a = ord(ciphertext[i]) - shift
        if (65 <= a <= 90) or (97 <= a <= 122):
            list_.append(a)
        elif 32 <= a <= 61:
            list_.append(a + shift)
        else:
            list_.append(a + 26)
    plaintext = "".join([chr(i) for i in list_])
    return plaintext
