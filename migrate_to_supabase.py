import os
import sqlite3

import psycopg2
from dotenv import load_dotenv

load_dotenv()

SQLITE_DATABASE = "lessons.db"


def get_sqlite_connection():
    conn = sqlite3.connect(SQLITE_DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def get_supabase_connection():
    password = input("Enter your Supabase database password: ")

    return psycopg2.connect(
        host="aws-0-eu-west-1.pooler.supabase.com",
        port=5432,
        dbname="postgres",
        user="postgres.elpipcpnuaxvkatrnpvk",
        password=password,
        sslmode="require"
    )


def migrate():
    sqlite_conn = get_sqlite_connection()
    postgres_conn = get_supabase_connection()

    sqlite_cursor = sqlite_conn.cursor()
    postgres_cursor = postgres_conn.cursor()

    try:
        # --------------------------------------------------
        # USERS
        # --------------------------------------------------

        sqlite_cursor.execute("SELECT * FROM users")
        users = sqlite_cursor.fetchall()

        for row in users:
            postgres_cursor.execute(
                """
                INSERT INTO public.users (
                    id,
                    name,
                    email,
                    password,
                    plan,
                    subscription_status,
                    subscription_start,
                    subscription_end
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
                """,
                (
                    row["id"],
                    row["name"],
                    row["email"],
                    row["password"],
                    row["plan"],
                    row["subscription_status"],
                    row["subscription_start"],
                    row["subscription_end"],
                )
            )

        print(f"Users migrated: {len(users)}")

        # --------------------------------------------------
        # LESSONS
        # --------------------------------------------------

        sqlite_cursor.execute("SELECT * FROM lessons")
        lessons = sqlite_cursor.fetchall()

        for row in lessons:
            postgres_cursor.execute(
                """
                INSERT INTO public.lessons (
                    id,
                    user_id,
                    title,
                    age,
                    duration,
                    topic,
                    outcomes,
                    materials,
                    warmup,
                    steps,
                    tune,
                    song,
                    story,
                    game,
                    assessment,
                    home,
                    picture_cards,
                    picture_cards_colour,
                    animated_story,
                    created_at,
                    updated_at
                )
                VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
                ON CONFLICT (id) DO NOTHING
                """,
                (
                    row["id"],
                    row["user_id"],
                    row["title"],
                    row["age"],
                    row["duration"],
                    row["topic"],
                    row["outcomes"],
                    row["materials"],
                    row["warmup"],
                    row["steps"],
                    row["tune"],
                    row["song"],
                    row["story"],
                    row["game"],
                    row["assessment"],
                    row["home"],
                    row["picture_cards"],
                    row["picture_cards_colour"],
                    row["animated_story"],
                    row["created_at"],
                    row["updated_at"],
                )
            )

        print(f"Lessons migrated: {len(lessons)}")

        # --------------------------------------------------
        # USAGE
        # --------------------------------------------------

        sqlite_cursor.execute("SELECT * FROM usage")
        usage_rows = sqlite_cursor.fetchall()

        for row in usage_rows:
            postgres_cursor.execute(
                """
                INSERT INTO public.usage (
                    id,
                    user_id,
                    month,
                    lessons_used,
                    stories_used,
                    images_used,
                    picture_cards_used
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
                """,
                (
                    row["id"],
                    row["user_id"],
                    row["month"],
                    row["lessons_used"],
                    row["stories_used"],
                    row["images_used"],
                    row["picture_cards_used"],
                )
            )

        print(f"Usage records migrated: {len(usage_rows)}")

        # --------------------------------------------------
        # PAYMENTS
        # --------------------------------------------------

        sqlite_cursor.execute("SELECT * FROM payments")
        payments = sqlite_cursor.fetchall()

        for row in payments:
            plan = None

            # Existing SQLite payments do not have a plan column.
            # The historical records are preserved with plan = NULL.
            postgres_cursor.execute(
                """
                INSERT INTO public.payments (
                    id,
                    user_id,
                    amount,
                    reference,
                    status,
                    payment_date,
                    mpesa_transaction_id,
                    plan
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
                """,
                (
                    row["id"],
                    row["user_id"],
                    row["amount"],
                    row["reference"],
                    row["status"],
                    row["payment_date"],
                    row["mpesa_transaction_id"],
                    plan,
                )
            )

        print(f"Payments migrated: {len(payments)}")

        # --------------------------------------------------
        # EXTENSION CREDITS
        # --------------------------------------------------

        sqlite_cursor.execute("SELECT * FROM extension_credits")
        extension_rows = sqlite_cursor.fetchall()

        for row in extension_rows:
            postgres_cursor.execute(
                """
                INSERT INTO public.extension_credits (
                    id,
                    user_id,
                    resource_type,
                    credits,
                    created_at,
                    updated_at
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
                """,
                (
                    row["id"],
                    row["user_id"],
                    row["resource_type"],
                    row["credits"],
                    row["created_at"],
                    row["updated_at"],
                )
            )

        print(
            f"Extension credits migrated: {len(extension_rows)}"
        )

        postgres_conn.commit()

        print()
        print("Migration completed successfully.")

    except Exception:
        postgres_conn.rollback()
        raise

    finally:
        sqlite_cursor.close()
        postgres_cursor.close()
        sqlite_conn.close()
        postgres_conn.close()


if __name__ == "__main__":
    migrate()