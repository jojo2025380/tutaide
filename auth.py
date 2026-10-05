import bcrypt
from database import get_connection


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

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM users
        WHERE email = %s
        """,
        (email,)
    )

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user is None:
        return None

    stored_password = user["password"].encode("utf-8")

    password_ok = bcrypt.checkpw(
        password.encode("utf-8"),
        stored_password
    )

    if password_ok:
        return dict(user)

    return None