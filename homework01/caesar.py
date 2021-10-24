def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    # """
    # Encrypts plaintext using a Caesar cipher.
    #
    # >>> encrypt_caesar("PYTHON")
    # 'SBWKRQ'
    # >>> encrypt_caesar("python")
    # 'sbwkrq'
    # >>> encrypt_caesar("Python3.6")
    # 'Sbwkrq3.6'
    # >>> encrypt_caesar("")
    # ''
    # """
    if len(plaintext) == 0:
        return plaintext
    list_ = []
    answ = []
    shift = shift % 26
    for i in range(len(plaintext)):
        notlow = 0 if plaintext[i].islower() else 1
        a = ord(plaintext[i]) + shift if notlow == 0 else ord(plaintext[i].lower()) + shift

        if 97 <= a <= 122:
            list_.append(a)
        elif a <= 61:
            list_.append(a - shift)
        else:
            list_.append(a - 26)

        if notlow == 0:
            answ.append(chr(list_[i]))
        else:
            b = chr(list_[i]).upper()
            answ.append(b)
    ciphertext = "".join([i for i in answ])
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    # """
    # Decrypts a ciphertext using a Caesar cipher.
    #
    # >>> decrypt_caesar("SBWKRQ")
    # 'PYTHON'
    # >>> decrypt_caesar("sbwkrq")
    # 'python'
    # >>> decrypt_caesar("Sbwkrq3.6")
    # 'Python3.6'
    # >>> decrypt_caesar("")
    # ''
    # """
    if len(ciphertext) == 0:
        return ciphertext
    list_ = []
    answ = []
    shift = shift % 26
    for i in range(len(ciphertext)):
        notlow = 0 if ciphertext[i].islower() else 1
        a = ord(ciphertext[i]) - shift if notlow == 0 else ord(ciphertext[i].lower()) - shift

        if 97 <= a <= 122:
            list_.append(a)
        elif a <= 61:
            list_.append(a + shift)
        else:
            list_.append(a + 26)

        if notlow == 0:
            answ.append(chr(list_[i]))
        else:
            b = chr(list_[i]).upper()
            answ.append(b)
    plaintext = "".join([i for i in answ])
    return plaintext
