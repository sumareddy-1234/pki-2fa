import time
import pyotp
import os
from datetime import datetime

# Paths
SEED_FILE = os.path.join("data", "seed.txt")
OUTPUT_FILE = os.path.join("cron", "last_code.txt")

# Ensure folders exist
os.makedirs("data", exist_ok=True)
os.makedirs("cron", exist_ok=True)

def write_totp():
    if not os.path.exists(SEED_FILE):
        print("Seed not found. Run /decrypt-seed first.")
        return

    # Read the seed as UTF-8 text (base32 string)
    with open(SEED_FILE, "r", encoding="utf-8") as f:
        seed = f.read().strip()

    # Create TOTP object
    totp = pyotp.TOTP(seed)

    # Generate current valid code
    code = totp.now()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")

    # Save to file
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(f"{timestamp} - {code}\n")

    print(f"Wrote code {code} to {OUTPUT_FILE}")

# Run every 60 seconds
if __name__ == "__main__":
    while True:
        write_totp()
        time.sleep(60)
