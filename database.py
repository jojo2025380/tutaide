import os
import sqlite3
import json
from datetime import datetime

import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

DATABASE = "lessons.db"


def get_connection():
    database_url = os.getenv("DATABASE_URL")

    if database_url:
        return psycopg2.connect(
            database_url,
            sslmode="require",
            cursor_factory=RealDictCursor
        )

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def create_database():

    # Supabase/PostgreSQL tables are already created and migrated.
    # Do not run the SQLite-specific schema setup against PostgreSQL.
    if os.getenv("DATABASE_URL"):
        return

    conn = get_connection()
    cursor = conn.cursor()

    # ---------------- USERS TABLE ----------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            email TEXT UNIQUE NOT NULL,

            password TEXT NOT NULL,

            plan TEXT DEFAULT NULL,

            subscription_status TEXT DEFAULT 'inactive',

            subscription_start TEXT DEFAULT NULL,

            subscription_end TEXT DEFAULT NULL

        )
    """)

    # ---------------- LESSONS TABLE ----------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lessons (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER,

            title TEXT,
            age TEXT,
            duration TEXT,

            outcomes TEXT,
            materials TEXT,
            warmup TEXT,
            steps TEXT,

            tune TEXT,
            song TEXT,
            story TEXT,
            game TEXT,

            assessment TEXT,
            home TEXT,

            picture_cards TEXT,

            created_at TEXT,
            updated_at TEXT,

            FOREIGN KEY (user_id) REFERENCES users(id)

        )
    """)

    try:
        cursor.execute(
            "ALTER TABLE lessons ADD COLUMN topic TEXT"
        )
    except Exception:
        pass

    # ---------------- USAGE TABLE ----------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usage (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            month TEXT NOT NULL,

            lessons_used INTEGER DEFAULT 0,

            stories_used INTEGER DEFAULT 0,

            images_used INTEGER DEFAULT 0,

            picture_cards_used INTEGER DEFAULT 0,

            FOREIGN KEY (user_id) REFERENCES users(id),

            UNIQUE(user_id, month)

        )
    """)

    # ---------------- PAYMENTS TABLE ----------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS payments (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            amount REAL NOT NULL,

            reference TEXT,

            status TEXT DEFAULT 'pending',

            payment_date TEXT,

            FOREIGN KEY (user_id) REFERENCES users(id)

        )
    """)

    # ---------------- EXTENSION CREDITS TABLE ----------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS extension_credits (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            resource_type TEXT NOT NULL,

            credits INTEGER DEFAULT 0,

            created_at TEXT,

            updated_at TEXT,

            FOREIGN KEY (user_id) REFERENCES users(id)

        )
    """)

    # ---------------- LESSON MIGRATION ----------------

    cursor.execute("PRAGMA table_info(lessons)")
    lesson_columns = [
        column["name"]
        for column in cursor.fetchall()
    ]

    if "picture_cards" not in lesson_columns:

        cursor.execute("""
            ALTER TABLE lessons
            ADD COLUMN picture_cards TEXT
        """)

    if "picture_cards_colour" not in lesson_columns:

        cursor.execute("""
            ALTER TABLE lessons
            ADD COLUMN picture_cards_colour TEXT
        """)

    if "animated_story" not in lesson_columns:

        cursor.execute("""
            ALTER TABLE lessons
            ADD COLUMN animated_story TEXT
        """)

    conn.commit()
    cursor.close()
    conn.close()
    

# ==================================================
# LESSONS
# ==================================================

def save_lesson(user_id, lesson):

    conn = get_connection()
    cursor = conn.cursor()

    now = datetime.now().isoformat()

    cursor.execute(
        """
        INSERT INTO lessons (

            user_id,

            title,
            topic,
            age,
            duration,

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

            created_at,
            updated_at

        )

        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s)
        RETURNING id
        """,
        (

            user_id,

            lesson["title"],
            lesson.get("topic"),
            lesson["age"],
            lesson["duration"],

            json.dumps(lesson["outcomes"]),
            json.dumps(lesson["materials"]),
            lesson["warmup"],
            json.dumps(lesson["steps"]),

            lesson["tune"],
            lesson["song"],
            lesson["story"],
            lesson["game"],

            lesson["assessment"],
            lesson["home"],

            now,
            now

        )
    )

    lesson_id = cursor.fetchone()["id"]

    conn.commit()
    cursor.close()
    conn.close()

    return lesson_id


def get_all_lessons(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, title, age, duration, created_at, updated_at
        FROM lessons
        WHERE user_id = %s
        ORDER BY id DESC
        """,
        (user_id,)
    )

    lessons = cursor.fetchall()

    cursor.close()
    conn.close()

    return lessons


def get_lesson(user_id, lesson_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM lessons
        WHERE id = %s
        AND user_id = %s
        """,
        (lesson_id, user_id)
    )

    lesson = cursor.fetchone()

    cursor.close()
    conn.close()

    if lesson is None:
        return None

    return {

        "id": lesson["id"],

        "title": lesson["title"],
        "topic": lesson["topic"],
        "age": lesson["age"],
        "duration": lesson["duration"],

        "outcomes": json.loads(lesson["outcomes"]),
        "materials": json.loads(lesson["materials"]),
        "warmup": lesson["warmup"],
        "steps": json.loads(lesson["steps"]),

        "tune": lesson["tune"],
        "song": lesson["song"],
        "story": lesson["story"],
        "game": lesson["game"],

        "assessment": lesson["assessment"],
        "home": lesson["home"],

        "picture_cards": lesson["picture_cards"],
        "picture_cards_colour": lesson["picture_cards_colour"],
        "animated_story": lesson["animated_story"],

        "created_at": lesson["created_at"],
        "updated_at": lesson["updated_at"]

    }


def update_lesson(user_id, lesson_id, lesson):

    conn = get_connection()
    cursor = conn.cursor()

    now = datetime.now().isoformat()

    cursor.execute(
        """
        UPDATE lessons

        SET
            title = %s,
            age = %s,
            duration = %s,
            outcomes = %s,
            materials = %s,
            warmup = %s,
            steps = %s,
            tune = %s,
            song = %s,
            story = %s,
            game = %s,
            assessment = %s,
            home = %s,
            updated_at = %s

        WHERE id = %s
        AND user_id = %s
        """,
        (

            lesson["title"],
            lesson["age"],
            lesson["duration"],

            json.dumps(lesson["outcomes"]),
            json.dumps(lesson["materials"]),
            lesson["warmup"],
            json.dumps(lesson["steps"]),

            lesson["tune"],
            lesson["song"],
            lesson["story"],
            lesson["game"],

            lesson["assessment"],
            lesson["home"],

            now,

            lesson_id,
            user_id
        )
    )

    conn.commit()
    cursor.close()
    conn.close()

def save_picture_cards(user_id, lesson_id, picture_cards):

    conn = get_connection()
    cursor = conn.cursor()

    now = datetime.now().isoformat()

    cursor.execute(
        """
        UPDATE lessons

        SET
            picture_cards = %s,
            updated_at = %s

        WHERE id = %s
        AND user_id = %s
        """,
        (
            picture_cards,
            now,
            lesson_id,
            user_id
        )
    )

    conn.commit()
    cursor.close()
    conn.close()


def save_picture_cards_colour(user_id, lesson_id, picture_cards_colour):

    conn = get_connection()
    cursor = conn.cursor()

    now = datetime.now().isoformat()

    cursor.execute(
        """
        UPDATE lessons

        SET
            picture_cards_colour = %s,
            updated_at = %s

        WHERE id = %s
        AND user_id = %s
        """,
        (
            picture_cards_colour,
            now,
            lesson_id,
            user_id
        )
    )

    conn.commit()
    cursor.close()
    conn.close()


def save_animated_story(user_id, lesson_id, animated_story):

    conn = get_connection()
    cursor = conn.cursor()

    now = datetime.now().isoformat()

    cursor.execute(
        """
        UPDATE lessons

        SET
            animated_story = %s,
            updated_at = %s

        WHERE id = %s
        AND user_id = %s
        """,
        (
            animated_story,
            now,
            lesson_id,
            user_id
        )
    )

    conn.commit()
    cursor.close()
    conn.close()



def search_lessons(user_id, search):

    conn = get_connection()
    cursor = conn.cursor()

    search_pattern = f"%{search}%"

    cursor.execute(
        """
        SELECT id, title, age, duration, created_at, updated_at
        FROM lessons
        WHERE user_id = %s
        AND (
            title ILIKE %s
            OR topic ILIKE %s
        )
        ORDER BY id DESC
        """,
        (
            user_id,
            search_pattern,
            search_pattern
        )
    )

    lessons = cursor.fetchall()

    cursor.close()
    conn.close()

    return lessons


def delete_lesson(user_id, lesson_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM lessons
        WHERE id = %s
        AND user_id = %s
        """,
        (
            lesson_id,
            user_id
        )
    )

    conn.commit()
    cursor.close()
    conn.close()


def count_user_lessons(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*) AS count
        FROM lessons
        WHERE user_id = %s
        """,
        (user_id,)
    )

    total = cursor.fetchone()["count"]

    cursor.close()
    conn.close()

    return total


# ==================================================
# PAYMENTS
# ==================================================


def save_payment(user_id, amount, reference, status, plan=None):

    conn = get_connection()
    cursor = conn.cursor()

    now = datetime.now().isoformat()

    cursor.execute(
        """
        INSERT INTO payments (
            user_id,
            amount,
            reference,
            status,
            plan,
            payment_date
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id
        """,
        (
            user_id,
            amount,
            reference,
            status,
            plan,
            now
        )
    )

    payment_id = cursor.fetchone()["id"]

    conn.commit()
    cursor.close()
    conn.close()

    return payment_id


def update_payment_status(reference, status):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE payments
        SET status = %s
        WHERE reference = %s
        """,
        (
            status,
            reference
        )
    )

    conn.commit()
    cursor.close()
    conn.close()


def get_payment_by_reference(reference):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM payments
        WHERE reference = %s
        """,
        (reference,)
    )

    result = cursor.fetchone()

    conn.close()

    if result is None:
        return None

    return dict(result)


def get_user_payments(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM payments
        WHERE user_id = %s
        ORDER BY payment_date DESC
        """,
        (user_id,)
    )

    results = cursor.fetchall()

    conn.close()

    return [dict(row) for row in results]


# ==================================================
# SUBSCRIPTIONS
# ==================================================

def set_subscription(
    user_id,
    plan,
    status,
    start_date,
    end_date
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE users

        SET
            plan = %s,
            subscription_status = %s,
            subscription_start = %s,
            subscription_end = %s

        WHERE id = %s
        """,
        (
            plan,
            status,
            start_date,
            end_date,
            user_id
        )
    )

    conn.commit()
    conn.close()


def get_user_subscription(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            plan,
            subscription_status,
            subscription_start,
            subscription_end

        FROM users

        WHERE id = %s
        """,
        (user_id,)
    )

    result = cursor.fetchone()

    conn.close()

    if result is None:
        return None

    return dict(result)


# ==================================================
# USAGE
# ==================================================

def get_current_month():

    return datetime.now().strftime("%Y-%m")


def get_usage(user_id):

    month = get_current_month()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO usage (
            user_id,
            month
        )

        VALUES (%s, %s)

        ON CONFLICT (user_id, month)
        DO NOTHING
        """,
        (user_id, month)
    )

    conn.commit()

    cursor.execute(
        """
        SELECT *
        FROM usage
        WHERE user_id = %s
        AND month = %s
        """,
        (user_id, month)
    )

    result = cursor.fetchone()

    conn.close()

    return dict(result)


def increment_usage(
    user_id,
    resource_type,
    amount=1
):

    month = get_current_month()

    valid_resources = {
        "lessons_used",
        "stories_used",
        "images_used",
        "picture_cards_used"
    }

    if resource_type not in valid_resources:
        raise ValueError("Invalid resource type.")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO usage (
            user_id,
            month
        )

        VALUES (%s, %s)

        ON CONFLICT (user_id, month)
        DO NOTHING
        """,
        (user_id, month)
    )

    cursor.execute(
        f"""
        UPDATE usage

        SET {resource_type} =
            {resource_type} + %s

        WHERE user_id = %s
        AND month = %s
        """,
        (
            amount,
            user_id,
            month
        )
    )

    conn.commit()
    conn.close()

# ==================================================
# IMAGE USAGE
# ==================================================

def can_generate_image(user_id, image_limit):

    usage = get_usage(user_id)

    return usage["images_used"] < image_limit


def get_remaining_images(user_id, image_limit):

    usage = get_usage(user_id)

    remaining = (
        image_limit
        - usage["images_used"]
    )

    return max(remaining, 0)


# ==================================================
# SUBSCRIPTION PLAN LIMITS
# ==================================================

from config import PLANS


def get_plan_limits(user_id):

    subscription = get_user_subscription(user_id)

    plan = subscription.get("plan")
    status = subscription.get("subscription_status")
    end_date = subscription.get("subscription_end")

    is_active = (status == "active")

    if is_active and end_date:

        try:

            if datetime.fromisoformat(end_date) < datetime.now():
                is_active = False

        except (ValueError, TypeError):
            pass

    if not plan or not is_active:

        return {
            "name": "No Active Plan",
            "price": 0,
            "lesson_limit": 0,
            "story_limit": 0,
            "image_limit": 0,
            "picture_card_limit": 0,
            "key": "none"
        }

    plan = plan.lower()

    limits = PLANS.get(
        plan,
        PLANS["basic"]
    ).copy()

    limits["key"] = plan

    return limits
    
# ==================================================
# STORY USAGE
# ==================================================

def can_generate_story(user_id, story_limit):

    usage = get_usage(user_id)

    return usage["stories_used"] < story_limit


def get_remaining_stories(user_id, story_limit):

    usage = get_usage(user_id)

    remaining = (
        story_limit
        - usage["stories_used"]
    )

    return max(remaining, 0)

# ==================================================
# PICTURE CARD USAGE
# ==================================================

def can_generate_picture_cards(
    user_id,
    picture_card_limit
):

    usage = get_usage(user_id)

    return (
        usage["picture_cards_used"]
        < picture_card_limit
    )


def get_remaining_picture_cards(
    user_id,
    picture_card_limit
):

    usage = get_usage(user_id)

    remaining = (
        picture_card_limit
        - usage["picture_cards_used"]
    )

    return max(remaining, 0)

# ==================================================
# EXTENSION CREDITS
# ==================================================

def get_extension_credits(user_id, resource_type):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT credits
        FROM extension_credits
        WHERE user_id = %s
        AND resource_type = %s
        """,
        (
            user_id,
            resource_type
        )
    )

    result = cursor.fetchone()

    conn.close()

    if result is None:
        return 0

    return result["credits"]


def add_extension_credits(
    user_id,
    resource_type,
    credits
):

    conn = get_connection()
    cursor = conn.cursor()

    now = datetime.now().isoformat()

    cursor.execute(
        """
        SELECT id
        FROM extension_credits
        WHERE user_id = %s
        AND resource_type = %s
        """,
        (
            user_id,
            resource_type
        )
    )

    result = cursor.fetchone()

    if result:

        cursor.execute(
            """
            UPDATE extension_credits

            SET credits = credits + %s,
                updated_at = %s

            WHERE user_id = %s
            AND resource_type = %s
            """,
            (
                credits,
                now,
                user_id,
                resource_type
            )
        )

    else:

        cursor.execute(
            """
            INSERT INTO extension_credits (
                user_id,
                resource_type,
                credits,
                created_at,
                updated_at
            )

            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                user_id,
                resource_type,
                credits,
                now,
                now
            )
        )

    conn.commit()
    conn.close()


def use_extension_credit(
    user_id,
    resource_type
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT credits
        FROM extension_credits
        WHERE user_id = %s
        AND resource_type = %s
        """,
        (
            user_id,
            resource_type
        )
    )

    result = cursor.fetchone()

    if not result or result["credits"] <= 0:

        conn.close()

        return False

    cursor.execute(
        """
        UPDATE extension_credits

        SET credits = credits - 1,
            updated_at = %s

        WHERE user_id = %s
        AND resource_type = %s
        """,
        (
            datetime.now().isoformat(),
            user_id,
            resource_type
        )
    )

    conn.commit()
    conn.close()

    return True