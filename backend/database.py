"""
Database module for SnapEat.
Handles food log storage and retrieval using SQLite.
Stores daily scan logs and provides weekly summary data.
"""

import sqlite3
import os
import json
from datetime import datetime, timedelta

# Detect if running on Vercel
IS_VERCEL = os.environ.get('VERCEL') == '1'

# Database file location
if IS_VERCEL:
    # Use /tmp for writable database on Vercel
    DB_PATH = "/tmp/snapeat.db"
else:
    # Local development path
    DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "snapeat.db")


def get_connection():
    """Get a database connection with row factory enabled."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize the database tables if they don't exist."""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS food_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL DEFAULT 'default',
                food_name TEXT NOT NULL,
                category TEXT,
                calories REAL,
                carbs REAL,
                sugars REAL,
                fiber REAL,
                protein REAL,
                fat REAL,
                health_status TEXT,
                health_score INTEGER,
                scanned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_profiles (
                user_id TEXT PRIMARY KEY,
                name TEXT,
                age_group TEXT DEFAULT 'adult',
                daily_calorie_goal REAL DEFAULT 2000,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                email TEXT PRIMARY KEY,
                password TEXT NOT NULL,
                name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        conn.close()
        print(f"Database initialized at: {DB_PATH}")
    except Exception as e:
        print(f"Database Error: {e}")

def maybe_init_db():
    """Initialize the database only if necessary."""
    if IS_VERCEL:
        # On Vercel, /tmp is wiped on cold start, so we always try to init if not exists
        if not os.path.exists(DB_PATH):
            init_db()
    else:
        # Local development: only init if DB file is missing
        if not os.path.exists(DB_PATH):
            init_db()


def register_user(name, email, password):
    """Register a new user in the database."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
        # Also create a default profile
        cursor.execute("INSERT INTO user_profiles (user_id, name) VALUES (?, ?)", (email, name))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def authenticate_user(email, password):
    """Check if user credentials are valid."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
    user = cursor.fetchone()
    conn.close()
    return dict(user) if user else None


def reset_password(email):
    """Mock function for password reset."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    return True if user else False


def save_food_log(user_id, food_details):
    """
    Store a scanned food item for the daily tracking feature.

    Args:
        user_id: Identifier for the user.
        food_details: dict with food data (name, nutrition, classification).

    Returns:
        int: The ID of the inserted log entry.
    """
    conn = get_connection()
    cursor = conn.cursor()

    nutrition = food_details.get("nutrition", {})

    cursor.execute("""
        INSERT INTO food_logs
            (user_id, food_name, category, calories, carbs, sugars,
             fiber, protein, fat, health_status, health_score)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        food_details.get("name", "Unknown"),
        food_details.get("category", ""),
        nutrition.get("calories", 0),
        nutrition.get("carbs", 0),
        nutrition.get("sugars", 0),
        nutrition.get("fiber", 0),
        nutrition.get("protein", 0),
        nutrition.get("fat", 0),
        food_details.get("health_status", ""),
        food_details.get("health_score", 0)
    ))

    log_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return log_id


def get_daily_log(user_id, date=None):
    """
    Get all food entries for a specific day.

    Args:
        user_id: Identifier for the user.
        date: Date string (YYYY-MM-DD). Defaults to today.

    Returns:
        list of dict entries for the day.
    """
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM food_logs
        WHERE user_id = ? AND DATE(scanned_at) = ?
        ORDER BY scanned_at DESC
    """, (user_id, date))

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def get_daily_totals(user_id, date=None):
    """
    Get total nutritional intake for a specific day.

    Args:
        user_id: Identifier for the user.
        date: Date string (YYYY-MM-DD). Defaults to today.

    Returns:
        dict with summed nutritional values.
    """
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            COALESCE(SUM(calories), 0) as total_calories,
            COALESCE(SUM(carbs), 0) as total_carbs,
            COALESCE(SUM(sugars), 0) as total_sugars,
            COALESCE(SUM(fiber), 0) as total_fiber,
            COALESCE(SUM(protein), 0) as total_protein,
            COALESCE(SUM(fat), 0) as total_fat,
            COUNT(*) as total_items
        FROM food_logs
        WHERE user_id = ? AND DATE(scanned_at) = ?
    """, (user_id, date))

    row = cursor.fetchone()
    conn.close()

    return dict(row) if row else {}


def get_weekly_summary(user_id):
    """
    Retrieve data for the weekly summary report.

    Args:
        user_id: Identifier for the user.

    Returns:
        dict with daily breakdowns for the past 7 days.
    """
    conn = get_connection()
    cursor = conn.cursor()

    seven_days_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

    cursor.execute("""
        SELECT
            DATE(scanned_at) as date,
            COALESCE(SUM(calories), 0) as total_calories,
            COALESCE(SUM(protein), 0) as total_protein,
            COALESCE(SUM(carbs), 0) as total_carbs,
            COALESCE(SUM(fat), 0) as total_fat,
            COUNT(*) as items_scanned
        FROM food_logs
        WHERE user_id = ? AND DATE(scanned_at) >= ?
        GROUP BY DATE(scanned_at)
        ORDER BY DATE(scanned_at) ASC
    """, (user_id, seven_days_ago))

    rows = cursor.fetchall()
    conn.close()

    daily_data = [dict(row) for row in rows]

    # Calculate averages
    if daily_data:
        avg_calories = sum(d["total_calories"] for d in daily_data) / len(daily_data)
        total_items = sum(d["items_scanned"] for d in daily_data)
    else:
        avg_calories = 0
        total_items = 0

    return {
        "daily_breakdown": daily_data,
        "average_daily_calories": round(avg_calories, 1),
        "total_items_scanned": total_items,
        "days_tracked": len(daily_data)
    }


def get_recent_scans(user_id, limit=10):
    """
    Get the most recent food scans for a user.

    Args:
        user_id: Identifier for the user.
        limit: Max number of results.

    Returns:
        list of recent scan entries.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM food_logs
        WHERE user_id = ?
        ORDER BY scanned_at DESC
        LIMIT ?
    """, (user_id, limit))

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


# Initialize database if needed on module import
maybe_init_db()
