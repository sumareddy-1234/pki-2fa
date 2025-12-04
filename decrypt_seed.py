import base64
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization

# Load private key
with open("app/student_private.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(
        f.read(),
        password=None,
    )

# Read encrypted seed
with open("encrypted_seed.txt", "r") as f:
    encrypted_seed_b64 = f.read().strip()

encrypted_seed = base64.b64decode(encrypted_seed_b64)

# Decrypt using RSA OAEP
seed = private_key.decrypt(
    encrypted_seed,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None,
    )
)

# Save decrypted seed
with open("seed.txt", "wb") as f:
    f.write(seed)

print("Decrypted seed saved to seed.txt")
