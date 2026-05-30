from personal_assistant.db.database import get_connection, initialize_database
from personal_assistant.extraction.notes_extractor import extract_note_fields

initialize_database()

def save_note_from_message(message: str) -> dict:
    """
    Save a note from a natural language user message.

    Args:
        message: Natural language note request, such as
        "Remember that my insurance renewal is due next month".
    """
    fields = extract_note_fields(message)

    return save_note(
        topic=fields["topic"],
        content=fields["content"],
    )

def save_note(topic: str, content: str) -> dict:
    """
    Save a note under a topic.

    Args:
        topic: Short topic or category for the note.
        content: The note content to save.
    """
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO notes (topic, content)
            VALUES (?, ?)
            """,
            (topic, content),
        )
        connection.commit()

        return {
            "status": "success",
            "message": "Note saved successfully.",
            "note": {
                "id": cursor.lastrowid,
                "topic": topic,
                "content": content,
            },
        }


def list_recent_notes(limit: int = 5) -> dict:
    """
    List recent notes.

    Args:
        limit: Maximum number of recent notes to return.
    """
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT id, topic, content, created_at
            FROM notes
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

        notes = [dict(row) for row in rows]

        return {
            "status": "success",
            "count": len(notes),
            "notes": notes,
        }


def search_notes(query: str) -> dict:
    """
    Search notes by topic or content.

    Args:
        query: Search text to find in note topic or content.
    """
    search_text = f"%{query}%"

    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT id, topic, content, created_at
            FROM notes
            WHERE topic LIKE ? OR content LIKE ?
            ORDER BY id DESC
            """,
            (search_text, search_text),
        ).fetchall()

        notes = [dict(row) for row in rows]

        return {
            "status": "success",
            "count": len(notes),
            "notes": notes,
        }