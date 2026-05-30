from personal_assistant.db.database import get_connection, initialize_database
from personal_assistant.extraction.task_extractor import extract_task_fields

initialize_database()

def create_task_from_message(message: str) -> dict:
    """
    Create a task from a natural language user message.

    Args:
        message: Natural language task request, such as
        "Add a high priority task to renew insurance tomorrow".
    """
    fields = extract_task_fields(message)

    return create_task(
        title=fields["title"],
        due_date=fields["due_date"],
        priority=fields["priority"],
    )


def create_task(title: str, due_date: str = "", priority: str = "medium") -> dict:
    """
    Create a new task.

    Args:
        title: The task title or description.
        due_date: Optional due date, such as today, tomorrow, Friday, or 2026-06-01.
        priority: Task priority. Use low, medium, or high.
    """
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO tasks (title, due_date, priority, status)
            VALUES (?, ?, ?, 'open')
            """,
            (title, due_date, priority),
        )
        connection.commit()

        return {
            "status": "success",
            "message": "Task created successfully.",
            "task": {
                "id": cursor.lastrowid,
                "title": title,
                "due_date": due_date,
                "priority": priority,
                "status": "open",
            },
        }


def list_tasks(status: str = "open") -> dict:
    """
    List tasks by status.

    Args:
        status: Task status to filter by. Use open, completed, or all.
    """
    with get_connection() as connection:
        if status == "all":
            rows = connection.execute(
                """
                SELECT id, title, due_date, priority, status, created_at, completed_at
                FROM tasks
                ORDER BY id DESC
                """
            ).fetchall()
        else:
            rows = connection.execute(
                """
                SELECT id, title, due_date, priority, status, created_at, completed_at
                FROM tasks
                WHERE status = ?
                ORDER BY id DESC
                """,
                (status,),
            ).fetchall()

        tasks = [dict(row) for row in rows]

        return {
            "status": "success",
            "count": len(tasks),
            "tasks": tasks,
        }


def complete_task(task_id: int) -> dict:
    """
    Mark a task as completed.

    Args:
        task_id: The numeric ID of the task to complete.
    """
    with get_connection() as connection:
        row = connection.execute(
            "SELECT id, title, status FROM tasks WHERE id = ?",
            (task_id,),
        ).fetchone()

        if row is None:
            return {
                "status": "not_found",
                "message": f"No task found with id {task_id}.",
            }

        connection.execute(
            """
            UPDATE tasks
            SET status = 'completed',
                completed_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (task_id,),
        )
        connection.commit()

        return {
            "status": "success",
            "message": f"Task {task_id} marked as completed.",
            "task": {
                "id": row["id"],
                "title": row["title"],
                "status": "completed",
            },
        }