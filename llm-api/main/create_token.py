import string
import json
import random
import sys
from main import read_tokens_from_file

valid_users = read_tokens_from_file("tokens.json")

def generate_token(username):
    tokens = {"tokens" : valid_users}
    tokens["tokens"][username] = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    with open("tokens.json", "w") as file:
        json.dump(tokens, file, indent=4)
    print(f"Successfully created token for user {username} : {tokens['tokens'][username]}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python create_token.py <username>")
        sys.exit(1)
    generate_token(sys.argv[1])