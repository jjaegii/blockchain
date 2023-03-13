from fernet import Fernet
import base64

key = Fernet(Fernet.generate_key())

datatxt = open("data.txt", "r")
data = bytes(datatxt.read(), 'utf-8')
encrypted = key.encrypt(data)
datatxt.close()

encryptedtxt = open("encrypted.txt", "w")
encryptedtxt.write(encrypted.decode('utf-8'))
encryptedtxt.close()

encryptedtxt = open("encrypted.txt", "r")
data = bytes(encryptedtxt.read(), 'utf-8')
decrypted = key.decrypt(data)
encryptedtxt.close()

decryptedtxt = open("decrypted.txt", "w")
decryptedtxt.write(decrypted.decode('utf-8'))