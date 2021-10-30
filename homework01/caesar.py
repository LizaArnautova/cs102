def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    if len(plaintext) == 0:
        return plaintext
    list_ = []
    ciphertext = ""
    shift %= 26
    for i in range(len(plaintext)):
        if plaintext[i].islower():
            notlow = 0
        else:
            notlow = 1

        if notlow == 0:
            current_symbol = ord(plaintext[i]) + shift
        else:
            current_symbol = ord(plaintext[i].lower()) + shift

        if ord("a") <= current_symbol <= ord("z"):
            list_.append(current_symbol)
        elif current_symbol <= ord("A") - 1:
            list_.append(current_symbol - shift)
        else:
            list_.append(current_symbol - 26)

        if notlow == 0:
            ciphertext += chr(list_[i])
        else:
            b = chr(list_[i]).upper()
            ciphertext += b

    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    if len(ciphertext) == 0:
        return ciphertext
    list_ = []
    plaintext = ""
    shift %= 26
    for i in range(len(ciphertext)):
        if ciphertext[i].islower():
            notlow = 0
        else:
            notlow = 1

        if notlow == 0:
            current_symbol = ord(ciphertext[i]) - shift
        else:
            current_symbol = ord(ciphertext[i].lower()) - shift

        if ord("a") <= current_symbol <= ord("z"):
            list_.append(current_symbol)
        elif current_symbol <= ord("A") - 1:
            list_.append(current_symbol + shift)
        else:
            list_.append(current_symbol + 26)

        if notlow == 0:
            plaintext += chr(list_[i])
        else:
            b = chr(list_[i]).upper()
            plaintext += b

    return plaintext
