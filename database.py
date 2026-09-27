import sqlite3
import hashlib
import secrets

DATABASE = "pocketsmart.db"


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


# =========================================================
# PASSWORD SECURITY
# =========================================================

def hash_password(password):
    salt = secrets.token_bytes(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        200000
    )

    return salt.hex() + ":" + password_hash.hex()


def verify_password(password, stored_password):
    salt_hex, hash_hex = stored_password.split(":")

    salt = bytes.fromhex(salt_hex)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        200000
    )

    return secrets.compare_digest(
        password_hash.hex(),
        hash_hex
    )


# =========================================================
# TABLES
# =========================================================

def create_users_table():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def create_history_table():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS recommendation_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            planner_type TEXT NOT NULL,
            user_input TEXT NOT NULL,
            recommendation TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT (datetime('now', 'localtime'))
        )
    """)

    connection.commit()
    connection.close()


# =========================================================
# REGISTER
# =========================================================

def register_user(username, password):
    connection = get_connection()

    try:
        secure_password = hash_password(password)

        connection.execute(
            """
            INSERT INTO users (username, password)
            VALUES (?, ?)
            """,
            (username, secure_password)
        )

        connection.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        connection.close()


# =========================================================
# LOGIN
# =========================================================

def check_user(username, password):
    connection = get_connection()

    user = connection.execute(
        """
        SELECT *
        FROM users
        WHERE username = ?
        """,
        (username,)
    ).fetchone()

    connection.close()

    if not user:
        return None

    try:
        if verify_password(
            password,
            user["password"]
        ):
            return user

    except (ValueError, AttributeError):
        return None

    return None


# =========================================================
# SAVE HISTORY
# =========================================================

def save_history(
    username,
    planner_type,
    user_input,
    recommendation
):

    connection = get_connection()

    connection.execute(
        """
        INSERT INTO recommendation_history
        (
            username,
            planner_type,
            user_input,
            recommendation
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            username,
            planner_type,
            user_input,
            recommendation
        )
    )

    connection.commit()
    connection.close()


# =========================================================
# GET HISTORY
# =========================================================

def get_history(username):

    connection = get_connection()

    history = connection.execute(
        """
        SELECT *
        FROM recommendation_history
        WHERE username = ?
        ORDER BY created_at DESC
        """,
        (username,)
    ).fetchall()

    connection.close()

    return history