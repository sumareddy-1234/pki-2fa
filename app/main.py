from fastapi import FastAPI
import pyotp

app = FastAPI()

import base64

with open("seed.txt", "rb") as f:
    seed_bytes = f.read()

# Convert raw seed into Base32 string
seed_b32 = base64.b32encode(seed_bytes).decode("utf-8")

totp = pyotp.TOTP(seed_b32)

@app.get("/generate-otp")
def generate_otp():
    """Generate a current TOTP code"""
    return {"otp": totp.now()}
