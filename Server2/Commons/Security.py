import hashlib
import uuid


def encrypt(target):
    target = str(target)
    salt = str(uuid.uuid4()).replace('-','')
    target = target+salt
    print(target)
    hashSHA = hashlib.sha256(target.encode()).hexdigest()
    print(hashSHA)
    return hashSHA