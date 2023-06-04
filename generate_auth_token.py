import sys

import jwt
import os

from datetime import datetime, timedelta

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
JWT_EXPIRATION_TIME_MINUTES = 30


def generate_token(username):
    """
    Generate a JWT token for a given username.
    :param username: str
    :return: str
    """
    expiration = datetime.utcnow() + timedelta(minutes=JWT_EXPIRATION_TIME_MINUTES)
    payload = {"username": username, "exp": expiration}
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token


if __name__ == "__main__":
    # Check if username is provided as a command line argument
    if len(sys.argv) < 2:
        print("Please provide a username as a command line argument.")
        sys.exit(1)

    username = sys.argv[1]
    token = generate_token(username)
    print("Generated Token:", token)
