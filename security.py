from email.mime import base
import bcrypt
import base64

from click import password_option


def encodeBase64(input):
    input = input.encode('utf-8')
    input = base64.b64encode(input)
    input = input.decode('utf-8')

def decodeBase64(input):
    return base64.b64decode(input)


def hash_password(password):
    password = password.encode('utf-8')
    password = bcrypt.hashpw(password, bcrypt.gensalt())
    return password

def check_password(password, password_hash):
    return bcrypt.checkpw(password.encode('utf-8'), password_hash)

if __name__ == '__main__':
    pw = "secret"
    print(hash_password(pw))
    print(check_password(pw,hash_password(pw)))

