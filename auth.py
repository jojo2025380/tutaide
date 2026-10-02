import sqlite3
import bcrypt


def hash_password(password):

    password_bytes = password.encode("utf-8")

    hashed = bcrypt.hashpw(
        password_bytes,
        bcrypt.gensalt()
    )

    return hashed.decode("utf-8")

def create_user(name, email, password):

    conn = sqlite3.connect("lessons.db")
    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO users(name, email, password)
            VALUES(?, ?, ?)
            """,
            (
                name,
                email,
                hash_password(password)
            )
        )

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()


def login_user(email, password):

    conn = sqlite3.connect("lessons.db")
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM users
        WHERE email=?
        """,
        (email,)
    )

    user = cursor.fetchone()

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