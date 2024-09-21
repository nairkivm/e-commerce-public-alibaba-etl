from cryptography.fernet import Fernet

# Generate a Fernet key
fernet_key = Fernet.generate_key()
print(fernet_key.decode())  # Print the key as a string
