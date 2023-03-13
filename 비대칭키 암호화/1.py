from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

# 암호화
with open("public_key.pem", "rb") as f:
    public_key = serialization.load_pem_public_key(
        f.read(),
        backend=default_backend()
    )

msg = input("평문 메시지 : ")
key = Fernet.generate_key()
fernet = Fernet(key)
enc_msg = fernet.encrypt(bytes(msg, 'utf-8'))
enc_key = public_key.encrypt(
    key,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

print('enc_msg =', enc_msg)
print('enc_key =', enc_key)


with open("private_key.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(
        f.read(),
        password=None,
        backend=default_backend()
    )

aes_key = private_key.decrypt(
    enc_key,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

decryptor = Fernet(aes_key)
message = decryptor.decrypt(enc_msg)
print('복호화 결과 :', message.decode('utf-8'))
