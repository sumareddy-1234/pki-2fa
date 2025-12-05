from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import base64
import pyotp

app = FastAPI()

SEED_FILE = "data/seed.txt"

# Ensure data folder exists
os.makedirs("data", exist_ok=True)

class SeedRequest(BaseModel):
    encrypted_seed: str

@app.post("/decrypt-seed")
def decrypt_seed_endpoint(request: SeedRequest):
    encrypted_seed = request.encrypted_seed

    # Decode Base64 to bytes
    try:
        decoded_bytes = base64.b64decode(encrypted_seed)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to decode seed: {e}")

    # Convert bytes to Base32 string (TOTP expects Base32)
    try:
        decoded_seed = base64.b32encode(decoded_bytes).decode("utf-8")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to encode seed to Base32: {e}")

    # Save seed as UTF-8 text
    with open(SEED_FILE, "w", encoding="utf-8") as f:
        f.write(decoded_seed)

    return {"status": "success", "message": "Seed decrypted and saved"}

@app.get("/generate-2fa")
def generate_2fa():
    if not os.path.exists(SEED_FILE):
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")
    with open(SEED_FILE, "r", encoding="utf-8") as f:
        seed = f.read().strip()
    totp = pyotp.TOTP(seed)
    code = totp.now()
    return {"code": code, "valid_for": 30}

class CodeRequest(BaseModel):
    code: str

@app.post("/verify-2fa")
def verify_2fa(code_request: CodeRequest):
    if not os.path.exists(SEED_FILE):
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")
    with open(SEED_FILE, "r", encoding="utf-8") as f:
        seed = f.read().strip()
    totp = pyotp.TOTP(seed)
    valid = totp.verify(code_request.code)
    return {"valid": valid, "message": "Correct code" if valid else "Incorrect code"}
