
import bcrypt
import json
import secrets
import pyotp
import time
from collections import defaultdict

from database import get_connection

# Temporary in-memory login-attempt tracking
_login_failures = defaultdict(list)
_LOGIN_MAX_ATTEMPTS = 5
_LOGIN_LOCKOUT_SECONDS = 900

def hash_password(password):

    password_bytes = password.encode("utf-8")

    hashed = bcrypt.hashpw(
        password_bytes,
        bcrypt.gensalt()
    )

    return hashed.decode("utf-8")


def create_user(name, email, password):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO users(name, email, password)
            VALUES(%s, %s, %s)
            """,
            (
                name,
                email,
                hash_password(password)
            )
        )

        conn.commit()
        return True

    except Exception:
        conn.rollback()
        return False

    finally:
        cursor.close()
        conn.close()



def login_user(email, password):
    """Verify credentials and temporarily lock out repeated failures."""
    now = time.time()
    key = (email or "").strip().lower()

    failures = _login_failures[key]
    failures[:] = [
        timestamp
        for timestamp in failures
        if now - timestamp < _LOGIN_LOCKOUT_SECONDS
    ]

    if len(failures) >= _LOGIN_MAX_ATTEMPTS:
        return None

    conn = get_connection()
    cursor = conn.cursor()

    placeholder = (
        "?"
        if conn.__class__.__module__ == "sqlite3"
        else "%s"
    )

    try:
        cursor.execute(
            f"""
            SELECT * FROM users
            WHERE LOWER(email) = {placeholder}
            """,
            (key,)
        )
        user = cursor.fetchone()
    finally:
        cursor.close()
        conn.close()

    if user is not None:
        stored_password = user["password"].encode("utf-8")
        password_ok = bcrypt.checkpw(
            password.encode("utf-8"),
            stored_password
        )

        if password_ok:
            _login_failures.pop(key, None)
            return dict(user)

    failures.append(now)
    return None



def generate_mfa_secret():
    """Generate a secret for an authenticator app."""
    return pyotp.random_base32()


def generate_mfa_uri(email, secret):
    """Generate the provisioning URI used for the QR code."""
    return pyotp.TOTP(secret).provisioning_uri(
        name=email,
        issuer_name="TutAide"
    )


def verify_mfa_code(secret, code):
    """Verify a time-based authenticator code."""
    if not secret or not code:
        return False

    code = str(code).strip().replace(" ", "")

    if not code.isdigit() or len(code) != 6:
        return False

    try:
        return pyotp.TOTP(secret).verify(
            code,
            valid_window=1
        )
    except (ValueError, TypeError):
        return False



def save_pending_mfa_secret(user_id, secret):
    """Save a pending MFA secret only if MFA is not already enabled."""
    conn = get_connection()
    cursor = conn.cursor()

    placeholder = (
        "?"
        if conn.__class__.__module__ == "sqlite3"
        else "%s"
    )

    try:
        cursor.execute(
            f"""
            UPDATE users
            SET mfa_secret = {placeholder}
            WHERE id = {placeholder}
              AND mfa_enabled = FALSE
            """,
            (secret, user_id)
        )

        saved = cursor.rowcount == 1
        conn.commit()
        return saved

    except Exception:
        conn.rollback()
        return False

    finally:
        cursor.close()
        conn.close()



def enable_mfa(user_id, code):
    """Enable MFA only after verifying the setup code."""
    conn = get_connection()
    cursor = conn.cursor()

    placeholder = (
        "?"
        if conn.__class__.__module__ == "sqlite3"
        else "%s"
    )

    try:
        cursor.execute(
            f"""
            SELECT mfa_secret
            FROM users
            WHERE id = {placeholder}
            """,
            (user_id,)
        )

        user = cursor.fetchone()

        if not user or not verify_mfa_code(
            user["mfa_secret"], code
        ):
            return False, []

        backup_codes = [
            secrets.token_hex(4).upper()
            for _ in range(8)
        ]

        hashed_codes = [
            hash_password(item)
            for item in backup_codes
        ]

        cursor.execute(
            """
            UPDATE users
            SET mfa_enabled = TRUE,
                mfa_backup_codes = %s
            WHERE id = %s
            """,
            (json.dumps(hashed_codes), user_id)
        )

        conn.commit()
        return True, backup_codes

    except Exception:
        conn.rollback()
        return False, []

    finally:
        cursor.close()
        conn.close()


def verify_mfa_backup_code(user_id, backup_code):
    """Verify a backup code and invalidate it after use."""
    if not backup_code:
        return False

    conn = get_connection()
    cursor = conn.cursor()

    placeholder = (
        "?"
        if conn.__class__.__module__ == "sqlite3"
        else "%s"
    )

    try:
        cursor.execute(
            f"""
            SELECT mfa_backup_codes
            FROM users
            WHERE id = {placeholder}
              AND mfa_enabled = TRUE
            """,
            (user_id,)
        )

        user = cursor.fetchone()

        if not user or not user["mfa_backup_codes"]:
            return False

        stored_codes = json.loads(user["mfa_backup_codes"])
        submitted_code = backup_code.strip().upper()

        matched_index = None

        for index, hashed_code in enumerate(stored_codes):
            if bcrypt.checkpw(
                submitted_code.encode("utf-8"),
                hashed_code.encode("utf-8"),
            ):
                matched_index = index
                break

        if matched_index is None:
            return False

        stored_codes.pop(matched_index)

        cursor.execute(
            """
            UPDATE users
            SET mfa_backup_codes = %s
            WHERE id = %s
            """,
            (json.dumps(stored_codes), user_id)
        )

        conn.commit()
        return True

    except Exception:
        conn.rollback()
        return False

    finally:
        cursor.close()
        conn.close()
