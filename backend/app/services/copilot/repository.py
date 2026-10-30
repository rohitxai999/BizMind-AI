import json
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional

from app.core.config import settings
from app.schemas.copilot import AuditLogEntry


class CopilotAuditRepository:
    """
    Persistence repository for BizMind AI Copilot queries and multi-agent interactions.
    Provides audit trails, session histories, and decision tracking using SQLite.
    """

    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            base_dir = Path(__file__).resolve().parent.parent.parent.parent
            resolved_db = base_dir / settings.COPILOT_DB_PATH
            resolved_db.parent.mkdir(parents=True, exist_ok=True)
            self.db_path = str(resolved_db)
        else:
            self.db_path = db_path


        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        """Create tables if they do not exist."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS copilot_audit_logs (
                    id TEXT PRIMARY KEY,
                    session_id TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    query TEXT NOT NULL,
                    intent TEXT NOT NULL,
                    summary TEXT NOT NULL,
                    tools_called TEXT NOT NULL
                )
                """
            )
            cursor.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_copilot_session ON copilot_audit_logs(session_id)
                """
            )
            cursor.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_copilot_timestamp ON copilot_audit_logs(timestamp)
                """
            )
            conn.commit()

    def save_interaction(
        self,
        session_id: str,
        query: str,
        intent: str,
        summary: str,
        tools_called: List[str],
    ) -> AuditLogEntry:
        """Persist a query, response summary, and tool calls into audit log."""
        record_id = str(uuid.uuid4())
        now_iso = datetime.now(timezone.utc).isoformat()
        tools_json = json.dumps(tools_called)

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO copilot_audit_logs (id, session_id, timestamp, query, intent, summary, tools_called)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (record_id, session_id, now_iso, query, intent, summary, tools_json),
            )
            conn.commit()

        return AuditLogEntry(
            id=record_id,
            session_id=session_id,
            timestamp=now_iso,
            query=query,
            intent=intent,
            summary=summary,
            tools_called=tools_called,
        )

    def get_history(
        self, session_id: Optional[str] = None, limit: int = 50
    ) -> List[AuditLogEntry]:
        """Retrieve recent interaction audit history, optionally filtered by session ID."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if session_id:
                cursor.execute(
                    """
                    SELECT id, session_id, timestamp, query, intent, summary, tools_called
                    FROM copilot_audit_logs
                    WHERE session_id = ?
                    ORDER BY timestamp DESC
                    LIMIT ?
                    """,
                    (session_id, limit),
                )
            else:
                cursor.execute(
                    """
                    SELECT id, session_id, timestamp, query, intent, summary, tools_called
                    FROM copilot_audit_logs
                    ORDER BY timestamp DESC
                    LIMIT ?
                    """,
                    (limit,),
                )
            rows = cursor.fetchall()

        results = []
        for r in rows:
            try:
                tools = json.loads(r["tools_called"])
            except Exception:
                tools = []
            results.append(
                AuditLogEntry(
                    id=r["id"],
                    session_id=r["session_id"],
                    timestamp=r["timestamp"],
                    query=r["query"],
                    intent=r["intent"],
                    summary=r["summary"],
                    tools_called=tools,
                )
            )
        return results

    def clear_history(self, session_id: Optional[str] = None) -> int:
        """Clear audit history, either for a specific session or completely."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if session_id:
                cursor.execute(
                    "DELETE FROM copilot_audit_logs WHERE session_id = ?",
                    (session_id,),
                )
            else:
                cursor.execute("DELETE FROM copilot_audit_logs")
            count = cursor.rowcount
            conn.commit()
        return count
