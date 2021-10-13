def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    if len(plaintext) == 0:
        return plaintext
    while len(keyword) < len(plaintext):
        keyword += keyword
    key = []
    for i in range(len(plaintext)):
        a = ord(keyword[i]) - 97 if ord(keyword[i]) - 65 > 25 else ord(keyword[i]) - 65
        key.append(a)

    notupp = plaintext.islower()
    if notupp == 1:
        plaintext = plaintext.upper()

    list = []
    for i in range(len(plaintext)):
        a = ord(plaintext[i]) + key[i]
        if 65 <= a <= 90:
            list.append(a)
        elif 32 <= a <= 64:
            list.append(a - key[i])
        else:
            list.append(a - 26)

    ciphertext = "".join([chr(i) for i in list])
    if notupp == 1:
        ciphertext = ciphertext.lower()

    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    if len(ciphertext) == 0:
        return ciphertext
    while len(keyword) < len(ciphertext):
        keyword += keyword
    key = []
    for i in range(len(ciphertext)):
        a = ord(keyword[i]) - 97 if ord(keyword[i]) - 65 > 25 else ord(keyword[i]) - 65
        key.append(a)

    notupp = ciphertext.islower()
    if notupp == 1:
        ciphertext = ciphertext.upper()

    list = []
    for i in range(len(ciphertext)):
        a = ord(ciphertext[i]) - key[i]
        if 65 <= a <= 90:
            list.append(a)
        elif 32 <= a <= 64:
            list.append(a + 26)
        else:
            list.append(a + 26)

    plaintext = "".join([chr(i) for i in list])
    if notupp == 1:
        plaintext = plaintext.lower()
    return plaintext