
from app.config import env_variables

env_data = env_variables()

from jose import jwe, jwt
from passlib.hash import bcrypt
import secrets
import string


def create_access_token(data : dict):
    to_encode = data
    # never expire OTP
    encoded_jwt = jwt.encode(
        to_encode, key=env_data["SECRET_KEY"], algorithm=env_data["ALGORITHM"]
    )
    encoded_jwe = jwe.encrypt(
        encoded_jwt,
        "asecret128bitkey",
        algorithm="dir",
        encryption="A128GCM",
    )
    return encoded_jwe
    
def generate_random_password(length=12):
    # Define the characters to use in the password
    letters = string.ascii_letters  # a-z, A-Z
    digits = string.digits  # 0-9
    special_characters = string.punctuation  # Special characters like !, @, #, etc.

    # Combine all characters
    all_characters = letters + digits + special_characters

    # Ensure password has at least one letter, one digit, and one special character
    password = [
        secrets.choice(letters),
        secrets.choice(digits),
        secrets.choice(special_characters)
    ]

    # Fill the rest of the password length with random characters from the combined pool
    password += [secrets.choice(all_characters) for _ in range(length - 3)]

    # Shuffle the list to ensure randomness
    secrets.SystemRandom().shuffle(password)

    # Convert list to string
    return ''.join(password)