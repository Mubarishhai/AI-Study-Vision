import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "studyvision.db")


def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # Explanations table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS explanations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Quiz results table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS quizzes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT NOT NULL,
            score INTEGER NOT NULL,
            total INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def save_explanation(question: str, answer: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO explanations (question, answer) VALUES (?, ?)",
        (question, answer),
    )
    conn.commit()
    conn.close()


def save_quiz_result(topic: str, score: int, total: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO quizzes (topic, score, total) VALUES (?, ?, ?)",
        (topic, score, total),
    )
    conn.commit()
    conn.close()


def get_stats():
    conn = get_connection()
    cur = conn.cursor()

    # Total explanations
    cur.execute("SELECT COUNT(*) FROM explanations")
    explanations_count = cur.fetchone()[0] or 0

    # Total quiz sessions
    cur.execute("SELECT COUNT(*) FROM quizzes")
    quiz_count = cur.fetchone()[0] or 0

    # Average accuracy
    cur.execute("SELECT AVG(CAST(score AS REAL) / total) FROM quizzes")
    avg = cur.fetchone()[0]
    avg_accuracy = avg if avg is not None else 0.0

    conn.close()
    return explanations_count, quiz_count, avg_accuracy


def get_recent_explanations(limit: int = 3):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT question, answer, created_at
        FROM explanations
        ORDER BY created_at DESC
        LIMIT ?
        """,
        (limit,),
    )
    rows = cur.fetchall()
    conn.close()
    return rows


def get_recent_quizzes(limit: int = 3):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT topic, score, total, created_at
        FROM quizzes
        ORDER BY created_at DESC
        LIMIT ?
        """,
        (limit,),
    )
    rows = cur.fetchall()
    conn.close()
    return rows


def save_explanation(question, answer):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO explanations (question, answer) VALUES (?, ?)",
        (question, answer)
    )
    conn.commit()
    conn.close()

    def save_quiz_result(topic, score, total):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO quizzes (topic, score, total) VALUES (?, ?, ?)",
            (topic, score, total)
        )
        conn.commit()
        conn.close()


