def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    if len(plaintext) == 0:
        return plaintext
    while len(keyword) < len(plaintext):
        keyword += keyword
    shift = []
    for i in range(len(plaintext)):
        a = ord(keyword[i]) - 97 if ord(keyword[i]) - 65 > 25 else ord(keyword[i]) - 65
        shift.append(a)

    List = []
    answ = []
    for i in range(len(plaintext)):
        notlow = 0 if plaintext[i].islower() else 1
        a = ord(plaintext[i]) + shift[i] if notlow == 0 else ord(plaintext[i].lower()) + shift[i]
        if 97 <= a <= 122:
            List.append(a)
        elif a <= 64:
            List.append(a - shift[i])
        else:
            List.append(a - 26)

        if notlow == 0:
            answ.append(chr(List[i]))
        else:
            b = chr(List[i]).upper()
            answ.append(b)

    ciphertext = "".join([i for i in answ])

    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
        Decrypts a ciphertext using a Vigenere cipher.

        >>> decrypt_vigenere("PYTHON", "A")
        'PYTHON'
        >>> decrypt_vigenere("python", "a")
        'python'
        >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
        'ATTACKATDAWN'
        """
    if len(ciphertext) == 0:
        return ciphertext
    while len(keyword) < len(ciphertext):
        keyword += keyword
    shift = []
    for i in range(len(ciphertext)):
        a = ord(keyword[i]) - 97 if ord(keyword[i]) - 65 > 25 else ord(keyword[i]) - 65
        shift.append(a)

    List = []
    answ = []
    for i in range(len(ciphertext)):
        notlow = 0 if ciphertext[i].islower() else 1
        a = ord(ciphertext[i]) - shift[i] if notlow == 0 else ord(ciphertext[i].lower()) - shift[i]
        if 97 <= a <= 122:
            List.append(a)
        elif a <= 64:
            List.append(a + shift[i])
        else:
            List.append(a + 26)

        if notlow == 0:
            answ.append(chr(List[i]))
        else:
            b = chr(List[i]).upper()
            answ.append(b)

    plaintext = "".join([i for i in answ])
    return plaintext
