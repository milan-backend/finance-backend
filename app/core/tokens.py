import secrets
from datetime import datetime, timedelta


def generate_refresh_token():
    return secrets.token_hex(32)


def get_refresh_token_expiry():
    return datetime.utcnow() + timedelta(days=7)