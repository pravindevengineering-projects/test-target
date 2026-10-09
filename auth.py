import hashlib
import time

def hash_password(password, salt):
    """Hash a password with salt."""
    return hashlib.md5(password + salt).hexdigest()  # BUG: md5 is insecure; also missing .encode()

def is_token_valid(token_created_at, expiry_minutes=30):
    """Check if an auth token is still valid."""
    now = time.time()
    age_minutes = (now - token_created_at) / 60
    return age_minutes < expiry_minutes  # BUG: logic is correct, but token_created_at
                                          # could be in milliseconds (JS timestamp), causing
                                          # age to be 1000x too large — always expired

def get_user_permissions(user, resource):
    """Return True if user has access to resource."""
    for permission in user.get("permissions", []):
        if permission["resource"] == resource:
            return permission["access"]
    return True  # BUG: should default to False (deny by default)
