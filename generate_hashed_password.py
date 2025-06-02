import bcrypt

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    print(hashed.decode())  # Copy output ini langsung ke yaml

hash_password("admin123")
