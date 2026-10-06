import sys
import bcrypt

if len(sys.argv) != 2:
    raise SystemExit("usage: python scripts/hash_password.py <password>")
print(bcrypt.hashpw(sys.argv[1].encode(), bcrypt.gensalt()).decode())
