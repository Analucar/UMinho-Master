import cryptography
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.serialization import PublicFormat
from cryptography.hazmat.primitives.serialization import Encoding
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives.serialization import load_pem_parameters
from cryptography.hazmat.primitives.serialization import ParameterFormat
from cryptography.hazmat.primitives.serialization import KeySerializationEncryption 

#---- Geracao dos parametros ----
print("##### GERAÇÃO DE PARAMETROS #####\n\n")
g = 2
keySize = 1024

#Alice cria os parametros
alice_parameters = dh.generate_parameters(generator = g, key_size=keySize)
print("[ALICE] O valor de g é: " + str(g))

#Obtem o p
p = alice_parameters.parameter_numbers().p
print("[ALICE] O valor de p é: " + str(p))

#Alice envia p e g para o bob
print("[ALICE] Enviei os parametros p e g para o Bob")
bob_parameters = dh.DHParameterNumbers(p, g).parameters()

#----- Alice cria a e g^a ------

print("\n\n##### TROCA DAS CHAVES E OBTENÇÃO DO SEGREDO #####\n\n")
#Alice cria o parametro a (valor secreto e privado)
alice_a = alice_parameters.generate_private_key()
print("[ALICE] O valor de a foi gerado.")

#Alice cria o parametro g^a (valor que e enviado ao bob)
alice_ga = alice_a.public_key()
print("\n[ALICE] O valor de g^a foi gerado e é:\n " + str(alice_ga.public_bytes(encoding=Encoding.PEM, format=PublicFormat.SubjectPublicKeyInfo)))

#----- Bob cria b e g^b ------

#Bob cria o parametro b (valor secreto e privado)
bob_b = bob_parameters.generate_private_key()
print("\n[BOB] O valor de b foi gerado." )

#bob cria o parametro g^b (valor que e enviado a Alice)
bob_gb = bob_b.public_key()
print("\n[BOB] O valor de g^b é: \n" + str(bob_gb.public_bytes(encoding=Encoding.PEM, format=PublicFormat.SubjectPublicKeyInfo)))

#---- Bob envia g^b para a Alice e esta obtem o segredo partilhado -----#
print("\n[BOB] A enviar g^b para a Alice")
alice_sharedSecret = alice_a.exchange(bob_gb)
print("\n[ALICE] O segredo partilhado entre ambos é: \n" +  str(alice_sharedSecret))

#---- Alice envia g^a para o Bob e este obtem o segredo partilhado -----#

print("\n[ALICE] A enviar g^a para o Bob")
bob_sharedSecret = bob_b.exchange(alice_ga)
print("\n[BOB] O segredo partilhado entre ambos é: \n" +  str(bob_sharedSecret))


#----- Troca de mensagens -----

print("\n\n##### TROCA DE MENSAGENS #####\n\n")
#Utilza-se o AES no modo GCM para trocar as mensagens
#Logo e necessario criar chaves a partir dos segredos do Bob e Alice

bob_AesKey = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=None).derive(bob_sharedSecret)
print("\n[BOB] A chave derivada a partir do segredo é: \n" +  str(bob_AesKey))

alice_AesKey = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=None).derive(alice_sharedSecret)
print("\n[ALICE] A chave derivada a partir do segredo é: \n" +  str(alice_AesKey))

#Bob cifra a mensagem 'Ola eu sou o Bob'

bob_plaintext = "Ola eu sou o Bob."
print("\n[BOB] vou enviar a mensagem: " + str(bob_plaintext))
iv_Bob = os.urandom(16)
encryptor = Cipher(algorithms.AES(bob_AesKey), modes.GCM(iv_Bob)).encryptor()
bob_Ciphertext = encryptor.update(bob_plaintext.encode()) + encryptor.finalize()
bob_tag = encryptor.tag

print("\n[BOB] O ciphertext obtido é: \n" + str(bob_Ciphertext))

#Bob envia o criptograma para a alice

print("\n[BOB] A enviar o criptograma para o Bob...")

#Alice decifra a mensagem
print("\n[ALICE] O criptograma recebido foi: \n" + str(bob_Ciphertext))
decryptor = Cipher(algorithms.AES(bob_AesKey), modes.GCM(iv_Bob, bob_tag)).decryptor()
bob_Deciphered = decryptor.update(bob_Ciphertext) + decryptor.finalize()

print("\n[ALICE] Após decifrar o criptograma, a mensagem obtida foi: " + str(bob_Deciphered.decode()))


#Alice responde e cifra a mensagem 'Olá Bob! Eu sou a Alice.'
alice_plaintext = "Ola Bob! Eu sou a Alice."
print("\n[ALICE] vou enviar a mensagem: " + str(alice_plaintext))

iv_Alice = os.urandom(16)
encryptor = Cipher(algorithms.AES(alice_AesKey), modes.GCM(iv_Alice)).encryptor()
alice_Ciphertext = encryptor.update(alice_plaintext.encode()) + encryptor.finalize()
alice_tag = encryptor.tag

print("\n[ALICE] O ciphertext obtido é: \n" + str(alice_Ciphertext))

#Alice envia o criptograma para o Bob
print("\n[ALICE] A enviar o criptograma para o Bob...")

#Bob decifra a mensagem
print("\n[BOB] O criptograma recebido foi: \n" + str(alice_Ciphertext))

decryptor = Cipher(algorithms.AES(bob_AesKey), modes.GCM(iv_Alice, alice_tag)).decryptor()
alice_Deciphered = decryptor.update(alice_Ciphertext) + decryptor.finalize()

print("\n[BOB] Após decifrar o criptograma, a mensagem obtida foi: " + str(alice_Deciphered.decode()))

