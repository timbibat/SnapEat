"""
Database module for SnapEat.
Handles food log storage and retrieval using SQLite or PostgreSQL.
Stores daily scan logs and provides weekly summary data.
"""

import sqlite3
import os
import json
import ssl
from urllib.parse import urlparse
from datetime import datetime, timedelta

# Detect if running on Vercel or if a hosted database URL is provided
DB_URL = os.environ.get('DATABASE_URL')
IS_VERCEL = os.environ.get('VERCEL') == '1'

# Database file location (SQLite fallback)
if IS_VERCEL:
    # Use /tmp for writable database on Vercel
    DB_PATH = "/tmp/snapeat.db"
else:
    # Local development path
    DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "snapeat.db")


def get_connection():
    """Get a database connection (Postgres if DB_URL is set, otherwise SQLite)."""
    if DB_URL:
        import pg8000.dbapi
        url = urlparse(DB_URL)
        conn = pg8000.dbapi.connect(
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port or 5432,
            database=url.path[1:],  # remove leading slash
            ssl_context=ssl.create_default_context()
        )
        return conn
    else:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn


def format_query(query, is_pg):
    """Format query placeholders and SQLite-specific logic for Postgres if needed."""
    if is_pg:
        # SQLite uses '?', Postgres pg8000 uses '%s'
        query = query.replace('?', '%s')
        # SQLite DATE() extracts date from timestamp; Postgres uses CAST(x AS DATE) or x::date
        query = query.replace('DATE(scanned_at)', 'CAST(scanned_at AS DATE)')
    return query


def get_row_dict(cursor, row, is_pg):
    """Convert a row tuple to a dictionary."""
    if not row:
        return None
    if is_pg:
        columns = [col[0] for col in cursor.description]
        return dict(zip(columns, row))
    else:
        return dict(row)


def get_rows_dicts(cursor, rows, is_pg):
    """Convert multiple row tuples to a list of dictionaries."""
    if not rows:
        return []
    if is_pg:
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, r)) for r in rows]
    else:
        return [dict(r) for r in rows]


def init_db():
    """Initialize the database tables if they don't exist."""
    is_pg = DB_URL is not None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        if is_pg:
            # Postgres Schema
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS food_logs (
                    id SERIAL PRIMARY KEY,
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
        else:
            # SQLite Schema
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
        if is_pg:
            print("Postgres database initialized successfully.")
        else:
            print(f"SQLite database initialized at: {DB_PATH}")
    except Exception as e:
        print(f"Database Initialization Error: {e}")


def maybe_init_db():
    """Initialize the database only if necessary."""
    if DB_URL:
        # Postgres: run init_db to ensure tables exist
        init_db()
    else:
        # SQLite local fallback
        if not os.path.exists(DB_PATH):
            init_db()


def register_user(name, email, password):
    """Register a new user in the database."""
    is_pg = DB_URL is not None
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query1 = format_query("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", is_pg)
        query2 = format_query("INSERT INTO user_profiles (user_id, name) VALUES (?, ?)", is_pg)
        cursor.execute(query1, (name, email, password))
        cursor.execute(query2, (email, name))
        conn.commit()
        return True
    except Exception as e:
        print(f"Registration Error: {e}")
        return False
    finally:
        conn.close()


def authenticate_user(email, password):
    """Check if user credentials are valid."""
    is_pg = DB_URL is not None
    conn = get_connection()
    cursor = conn.cursor()
    
    query = format_query("SELECT * FROM users WHERE email = ? AND password = ?", is_pg)
    cursor.execute(query, (email, password))
    user = cursor.fetchone()
    
    result = get_row_dict(cursor, user, is_pg)
    conn.close()
    return result


def reset_password(email):
    """Mock function for password reset."""
    is_pg = DB_URL is not None
    conn = get_connection()
    cursor = conn.cursor()
    
    query = format_query("SELECT email FROM users WHERE email = ?", is_pg)
    cursor.execute(query, (email,))
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
    is_pg = DB_URL is not None
    conn = get_connection()
    cursor = conn.cursor()

    nutrition = food_details.get("nutrition", {})

    query = """
        INSERT INTO food_logs
            (user_id, food_name, category, calories, carbs, sugars,
             fiber, protein, fat, health_status, health_score)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    params = (
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
    )

    if is_pg:
        query = format_query(query, is_pg) + " RETURNING id"
        cursor.execute(query, params)
        log_id = cursor.fetchone()[0]
    else:
        cursor.execute(format_query(query, is_pg), params)
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

    is_pg = DB_URL is not None
    conn = get_connection()
    cursor = conn.cursor()

    query = format_query("""
        SELECT * FROM food_logs
        WHERE user_id = ? AND DATE(scanned_at) = ?
        ORDER BY scanned_at DESC
    """, is_pg)

    cursor.execute(query, (user_id, date))
    rows = cursor.fetchall()
    result = get_rows_dicts(cursor, rows, is_pg)
    conn.close()

    return result


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

    is_pg = DB_URL is not None
    conn = get_connection()
    cursor = conn.cursor()

    query = format_query("""
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
    """, is_pg)

    cursor.execute(query, (user_id, date))
    row = cursor.fetchone()
    result = get_row_dict(cursor, row, is_pg) if row else {}
    conn.close()

    return result


def get_weekly_summary(user_id):
    """
    Retrieve data for the weekly summary report.

    Args:
        user_id: Identifier for the user.

    Returns:
        dict with daily breakdowns for the past 7 days.
    """
    is_pg = DB_URL is not None
    conn = get_connection()
    cursor = conn.cursor()

    seven_days_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

    query = format_query("""
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
    """, is_pg)

    cursor.execute(query, (user_id, seven_days_ago))
    rows = cursor.fetchall()
    daily_data = get_rows_dicts(cursor, rows, is_pg)
    conn.close()

    # Calculate averages
    if daily_data:
        avg_calories = sum(float(d["total_calories"]) for d in daily_data) / len(daily_data)
        total_items = sum(int(d["items_scanned"]) for d in daily_data)
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
    is_pg = DB_URL is not None
    conn = get_connection()
    cursor = conn.cursor()

    query = format_query("""
        SELECT * FROM food_logs
        WHERE user_id = ?
        ORDER BY scanned_at DESC
        LIMIT ?
    """, is_pg)

    cursor.execute(query, (user_id, limit))
    rows = cursor.fetchall()
    result = get_rows_dicts(cursor, rows, is_pg)
    conn.close()

    return result


# Initialize database if needed on module import
maybe_init_db()
