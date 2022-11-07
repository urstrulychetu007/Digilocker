from cryptography.fernet import Fernet
import sqlite3


key = b'zOd0B6F4FAojtmPwHZcdUzxlmeHnrwEswci-d3kDjuY='
# db = sqlite3

def decrypt_file(encMessage):
    fernet = Fernet(key)
    decMessage = fernet.decrypt(encMessage)
    return decMessage


def encrypt_file(message):
    fernet = Fernet(key)

    encMessage = fernet.encrypt(message) 
    return encMessage

# msg = 'gAAAAABjMUKDJH3fWDXVNrR4U_RvLiLzQNY1FJO4ku3lFDNSzLq1XT6xjH2NMJ4JDOyktsujVR4qEwWp0ONDLjJk61ChZ_wxyA=='
# print(decrypt_file(msg.encode()).decode())


