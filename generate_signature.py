from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import base64
import subprocess

# Step 1: Get the latest commit hash
commit_hash = subprocess.check_output(["git", "log", "-1", "--format=%H"]).decode().strip()
print("Latest commit hash:", commit_hash)

# Step 2: Load your private key
with open("app/student_private.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(f.read(), password=None)

# Step 3: Sign the commit hash using SHA256 and PKCS1v15
signature = private_key.sign(
    commit_hash.encode(),
    padding.PKCS1v15(),
    hashes.SHA256()
)

# Step 4: Load instructor public key
with open("app/instructor_public.pem", "rb") as f:
    instructor_public_key = serialization.load_pem_public_key(f.read())

# Step 5: Encrypt the signature using instructor's public key
encrypted_signature = instructor_public_key.encrypt(
    signature,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# Step 6: Encode to base64 and print single line
b64_encrypted = base64.b64encode(encrypted_signature).decode("utf-8")
print("\nEncrypted Commit Signature (copy this single line for submission):")
print(b64_encrypted)
