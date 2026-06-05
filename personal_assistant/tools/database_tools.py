from personal_assistant.db.database import get_connection


def inspect_database() -> dict:
    """
    Inspect the local SQLite database and return useful statistics.
    """
    with get_connection() as connection:
        total_tasks = connection.execute(
            "SELECT COUNT(*) AS count FROM tasks"
        ).fetchone()["count"]

        open_tasks = connection.execute(
            "SELECT COUNT(*) AS count FROM tasks WHERE status = 'open'"
        ).fetchone()["count"]

        completed_tasks = connection.execute(
            "SELECT COUNT(*) AS count FROM tasks WHERE status = 'completed'"
        ).fetchone()["count"]

        total_notes = connection.execute(
            "SELECT COUNT(*) AS count FROM notes"
        ).fetchone()["count"]

        recent_tasks = connection.execute(
            """
            SELECT id, title, due_date, priority, status, created_at
            FROM tasks
            ORDER BY id DESC
            LIMIT 5
            """
        ).fetchall()

        recent_notes = connection.execute(
            """
            SELECT id, topic, content, created_at
            FROM notes
            ORDER BY id DESC
            LIMIT 5
            """
        ).fetchall()

        return {
            "status": "success",
            "tasks": {
                "total": total_tasks,
                "open": open_tasks,
                "completed": completed_tasks,
                "recent": [dict(row) for row in recent_tasks],
            },
            "notes": {
                "total": total_notes,
                "recent": [dict(row) for row in recent_notes],
            },
        }