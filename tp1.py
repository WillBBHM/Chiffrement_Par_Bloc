#Reponse aux question lire "README TP1 REPONSE QUESTION.txt"
#Reponse aux question lire "README TP1 REPONSE QUESTION.txt"
#Reponse aux question lire "README TP1 REPONSE QUESTION.txt"

import random

sbox = [0xc, 5, 6, 0xb, 9, 0, 0xa, 0xd, 3, 0xe, 0xf, 8, 4, 7, 1, 2]
xbox = [sbox.index(i) for i in range(len(sbox))]

cles = (10, 4)

data = 14

def round(data, cles):
    return sbox[data ^ cles]

def back_round(data, cles):
    return xbox[data] ^ cles

def enc(data, cles):
    t = round(data, cles[0])
    p = round(t, cles[1])
    return p

def dec(data, cles):
    t = back_round(data, cles[1])
    p = back_round(t, cles[0])
    return p

def test_dechiffrage(data, data_dec):
    if(data == data_dec):
        print("Le message à bien été déchiffrer")
    else:
        print("Le déchiffrement à échouer")

def test_dechiffrage_file(filename):
    with open(filename, 'rb') as f:
        data1 = f.read()
        f.close()
    with open("decrypt_" + filename, 'rb') as f:
        data2 = f.read()
        f.close()
    if(data1 == data2):
        print("Le message à bien été déchiffrer")
    else:
        print("Le déchiffrement à échouer")

def test_ToyCipher():
    valid = 1
    for i in range(16):
        data_test = random.randint(0, 15)
        key = (random.randint(0, 15), random.randint(0, 15))
        test_enc = enc(data_test, key)
        test_dec = dec(test_enc, key)
        if(test_dec != data_test):
            valid = 0
            continue
    if(valid):
        print("ToyCipher est fonctionnelle d'après les test")
    else:
        print("ToyCipher n'est pas fonctionnelle d'après les test")

def enc_byte(byte, cles):
    nibble1 = byte & 0b1111
    nubble2 = byte >> 4
    enc_nibble1 = enc(nibble1, cles)
    enc_nibble2 = enc(nubble2, cles)
    octet = (enc_nibble2 << 4) | enc_nibble1
    return octet

def dec_byte(byte, cles):
    nibble1 = byte & 0b1111
    nubble2 = byte >> 4
    enc_nibble1 = dec(nibble1, cles)
    enc_nibble2 = dec(nubble2, cles)
    octet = (enc_nibble2 << 4) | enc_nibble1
    return octet

def enc_file(filename, cles):
    with open(filename, 'rb') as f:
        data = f.read()
        f.close()
    tmpData = list(data)
    for i in range(0, len(tmpData)):
        tmpData[i] = enc_byte(tmpData[i], cles)
    with open(filename + '.enc', 'wb') as f:
        f.write(bytearray(tmpData))
        f.close()

def dec_file(filename, cles):
    with open(filename, 'rb') as f:
        data = f.read()
        f.close()
    tmpData = list(data)
    for i in range(0, len(tmpData)):
        tmpData[i] = dec_byte(tmpData[i], cles)
    name = filename[:(len(filename)-4)]
    with open("decrypt_" + name, 'wb') as f:
        f.write(bytearray(tmpData))
        f.close()


def frequence(texte):
  freq = {}
  for caractere in texte:
    if caractere in freq:
      freq[caractere] += 1
    else:
      freq[caractere] = 1
  return freq

def attaque_frequence(texte_chifre, texte_original):
  freq_chifre = frequence(texte_chifre)
  freq_original = frequence(texte_original)
  correspondance = {}
  for caractere_original, nombre_occurences_original in freq_original.items():
    caractere_chifre = max(freq_chifre, key=lambda caractere_chifre: freq_chifre[caractere_chifre])
    correspondance[caractere_original] = caractere_chifre
    freq_chifre[caractere_chifre] = 0
  return correspondance


def enc_file_cfb(filename, cles, vecteur):
    with open(filename, 'rb') as f:
        data = f.read()
        f.close()
    tmpData = list(data)
    for i in range(0, len(tmpData)):
        tmpData[i] = enc_byte(tmpData[i] ^ vecteur, cles)
    with open(filename + '.cfb', 'wb') as f:
        f.write(bytearray(tmpData))
        f.close()

def dec_file_cfb(filename, cles, vecteur):
    with open(filename, 'rb') as f:
        data = f.read()
        f.close()
        tmpData = list(data)
    for i in range(0, len(tmpData)):
        tmpData[i] = dec_byte(tmpData[i], cles) ^ vecteur
    name = filename[:(len(filename)-4)]
    with open("decrypt_" + name, 'wb') as f:
        f.write(bytearray(tmpData))
        f.close()


print("--------------------ToyCipher---------------------\n")

print(f"Valeur originale: {data}")

data_enc = enc(data, cles)

print(f"Valeur chiffrer: {data_enc}")

data_dec = dec(data_enc, cles)

print(f"Valeur dechiffrer: {data_dec}")

test_dechiffrage(data, data_dec)

print("\n-------------------Test de la fonctionnalité de ToyCipher---------------\n")

test_ToyCipher()

print("\n--------------------------ToyCipher de caractère------------------------\n")

data = ord("Z")

print(f"Lettre originale: {chr(data)}")

data_enc = enc_byte(data, cles)

print(f"Lettre chiffrer: {chr(data_enc)}")

data_dec = dec_byte(data_enc, cles)

print(f"Lettre dechiffrer: {chr(data_dec)}")

test_dechiffrage(data, data_dec)

print("\n--------------------------ToyCipher de file------------------------\n")

enc_file("solCartoon.png", cles)
print("Encryption du fichier terminer\n")

dec_file("solCartoon.png.enc", cles)
print("Decryption du fichier terminer\n")

test_dechiffrage_file("solCartoon.png")

enc_file("test.txt", (9, 0))

print("---------------------Attaque par analyse de fréquence----------------------------\n")

with open("test.txt", 'rb') as f:
    data1 = f.read()
    f.close()

with open("test.txt.enc", 'rb') as f:
    data2 = f.read()
    f.close()
    
texte_original = data1
texte_chifre = data2

correspondance = attaque_frequence(texte_chifre, texte_original)

print("Correspondance :")
for caractere_original, caractere_chifre in correspondance.items():
    print("{} -> {}".format(chr(caractere_original), chr(caractere_chifre)))

print("\n--------------------Implementation de CFB---------------------\n")

vector = random.randint(0, 15)

print(f"Vecteur: {vector}\n")

enc_file_cfb("cfb_test.txt", cles, vector)
print("Encryption du fichier terminer\n")

dec_file_cfb("cfb_test.txt.cfb", cles, vector)
print("Decryption du fichier terminer\n")

#Reponse aux question lire "README TP1 REPONSE QUESTION.txt"
