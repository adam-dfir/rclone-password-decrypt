# Nov 24
# Decrypt encrypted passwords stored within the rclone configuration file. Will add b64 padding if needed to be %4
# Key (k) source https://github.com/rclone/rclone/blob/master/fs/config/obscure/obscure.go
# python decrypt_rclone.py -e [Encrypted Password]
import base64,argparse
from cryptography.hazmat.primitives.ciphers import Cipher,algorithms,modes
def rclone_decrypt(e):
    k=bytes([0x9c,0x93,0x5b,0x48,0x73,0x0a,0x55,0x4d,0x6b,0xfd,0x7c,0x63,0xc8,0x86,0xa9,0x2b,0xd3,0x90,0x19,0x8e,0xb8,0x12,0x8a,0xfb,0xf4,0xde,0x16,0x2b,0x8b,0x95,0xf6,0x38])
    b=bytearray(base64.urlsafe_b64decode(e)[16:])
    e=Cipher(algorithms.AES(k),modes.CTR(base64.urlsafe_b64decode(e)[:16])).encryptor()
    return e.update(b).decode('utf-8')
if __name__=="__main__":
    _A=argparse.ArgumentParser()
    _A.add_argument("--encrypted",metavar="[ENC_PASS]",help="Encrypted Password")
    _A=_A.parse_args()
    _A.encrypted+='='*(4-len(_A.encrypted)%4)
    print (f"Rclone Configuration Password: {rclone_decrypt(_A.encrypted)}")