import requests

student_id = "YOUR_STUDENT_ID"   # replace with your actual student ID
github_repo_url = "https://github.com/sumareddy-1234/pki-2fa"
api_url = "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws"

# Read your student public key
with open("app/student_public.pem", "r") as f:
    pem = f.read()

payload = {
    "student_id": student_id,
    "github_repo_url": github_repo_url,
    "public_key": pem,
}

resp = requests.post(api_url, json=payload, timeout=30)
data = resp.json()
print(data)

if data.get("encrypted_seed"):
    with open("encrypted_seed.txt", "w") as f:
        f.write(data["encrypted_seed"])
    print("Saved encrypted_seed.txt")
