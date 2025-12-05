#!/usr/bin/env bash
set -e
CODE=$(python - <<'PY'
import os, pyotp
seed_path = "/data/seed.txt"
if not os.path.exists(seed_path):
    print("")
    raise SystemExit(0)
with open(seed_path, "r") as f:
    seed = f.read().strip()
totp = pyotp.TOTP(seed)
print(totp.now())
PY
)
if [ -n "$CODE" ]; then
  echo "$(date -u +'%Y-%m-%dT%H:%M:%SZ') $CODE" > /cron/last_code.txt
fi
