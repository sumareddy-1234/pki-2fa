import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

# Paths to your keys
STUDENT_PRIVATE_KEY_PATH = "app/student_private.pem"
INSTRUCTOR_PUBLIC_KEY_PATH = "app/instructor_public.pem"

# Step 1: Load your student private key
with open(STUDENT_PRIVATE_KEY_PATH, "rb") as f:
    student_private_key = serialization.load_pem_private_key(
        f.read(),
        password=None
    )

# Step 2: Load instructor public key
with open(INSTRUCTOR_PUBLIC_KEY_PATH, "rb") as f:
    instructor_public_key = serialization.load_pem_public_key(f.read())

# Step 3: Get latest commit hash from your repo
import subprocess
commit_hash = subprocess.check_output(
    ["git", "log", "-1", "--format=%H"]
).decode().strip()
print(f"Latest commit hash: {commit_hash}")

# Step 4: Sign commit hash with your student private key
signature = student_private_key.sign(
    commit_hash.encode(),
    padding.PKCS1v15(),
    hashes.SHA256()
)

# Step 5: Encrypt the signature with instructor's public key
encrypted_signature = instructor_public_key.encrypt(
    signature,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# Step 6: Base64 encode the final encrypted signature (single line)
encoded_signature = base64.b64encode(encrypted_signature).decode('utf-8')
print("\nEncrypted Commit Signature (copy this single line for submission):")
print(encoded_signature)
