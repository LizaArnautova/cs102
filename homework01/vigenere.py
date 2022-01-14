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
        if ord(keyword[i]) - ord("A") > 25:
            j = ord(keyword[i]) - ord("a")
        else:
            j = ord(keyword[i]) - ord("A")
        shift.append(j)

    list_ = []
    ciphertext = ""
    for i, letter in enumerate(plaintext):
        notlow = 0 if letter.islower() else 1
        if notlow == 0:
            current_symbol = ord(letter) + shift[i]
        else:
            current_symbol = ord(letter.lower()) + shift[i]

        if ord("a") <= current_symbol <= ord("z"):
            list_.append(current_symbol)
        elif current_symbol <= ord("A") - 1:
            list_.append(current_symbol - shift[i])
        else:
            list_.append(current_symbol - 26)

        if notlow == 0:
            ciphertext += chr(list_[i])
        else:
            b = chr(list_[i]).upper()
            ciphertext += b

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
        if ord(keyword[i]) - ord("A") > 25:
            j = ord(keyword[i]) - ord("a")
        else:
            j = ord(keyword[i]) - ord("A")
        shift.append(j)

    list_ = []
    plaintext = ""
    for i, letter in enumerate(ciphertext):
        notlow = 0 if letter.islower() else 1
        if notlow == 0:
            current_symbol = ord(letter) - shift[i]
        else:
            current_symbol = ord(letter.lower()) - shift[i]

        if ord("a") <= current_symbol <= ord("z"):
            list_.append(current_symbol)
        elif current_symbol <= ord("A") - 1:
            list_.append(current_symbol + shift[i])
        else:
            list_.append(current_symbol + 26)

        if notlow == 0:
            plaintext += chr(list_[i])
        else:
            b = chr(list_[i]).upper()
            plaintext += b

    return plaintext
