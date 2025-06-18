import random
import string

def genRanPass(length=10):
    all_chars = string.ascii_letters + string.digits + string.punctuation
    if length <= 0:
        raise ValueError("Password length must be positive.")
    return ''.join(random.choices(all_chars, k=length))