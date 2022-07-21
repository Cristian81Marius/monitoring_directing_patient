import bcrypt


def hash_password(text_password):
    hashed_bytes = bcrypt.hashpw(text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(text_password.encode('utf-8'), hashed_bytes_password)