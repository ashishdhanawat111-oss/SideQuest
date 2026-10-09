
import sqlite3

DB_NAME = "sidequest.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS progress (
            id INTEGER PRIMARY KEY,
            xp INTEGER DEFAULT 0
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS completed_quests (
            quest TEXT PRIMARY KEY
        )
    """)

    cursor.execute(
        "INSERT OR IGNORE INTO progress (id, xp) VALUES (1, 0)"
    )

    conn.commit()
    conn.close()


def load_progress():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT xp FROM progress WHERE id = 1")
    xp = cursor.fetchone()[0]

    cursor.execute("SELECT quest FROM completed_quests")
    completed_quests = [row[0] for row in cursor.fetchall()]

    conn.close()
    return xp, completed_quests


def save_completed_quest(quest):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT OR IGNORE INTO completed_quests (quest) VALUES (?)",
        (quest,)
    )

    if cursor.rowcount == 1:
        cursor.execute(
            "UPDATE progress SET xp = xp + 100 WHERE id = 1"
        )

    conn.commit()
    conn.close()
