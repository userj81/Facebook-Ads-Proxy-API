import sqlite3
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Dict

DB_PATH = Path(__file__).parent.parent.parent / "data" / "history.db"


class HistoryService:
    """Serviço para gerenciar histórico de chamadas em SQLite"""

    def __init__(self):
        self._init_db()

    def _init_db(self):
        """Cria tabela se não existir"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS calls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                request_id TEXT UNIQUE,
                timestamp TEXT,
                endpoint TEXT,
                method TEXT,
                body_summary TEXT,
                response_status INTEGER,
                duration_ms REAL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """
        )
        conn.commit()
        conn.close()

    def save_call(
        self,
        endpoint: str,
        method: str,
        response_status: int,
        duration_ms: float,
        body_summary: str = None,
    ) -> str:
        """
        Salva uma chamada no histórico

        Args:
            endpoint: Endpoint da API
            method: Método HTTP
            response_status: Status code da resposta
            duration_ms: Duração em milissegundos
            body_summary: Resumo do body (opcional)

        Returns:
            Request ID gerado
        """
        request_id = f"req_{str(uuid.uuid4())[:8]}"
        timestamp = datetime.now().isoformat()

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO calls (request_id, timestamp, endpoint, method, body_summary, response_status, duration_ms)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            (request_id, timestamp, endpoint, method, body_summary, response_status, duration_ms),
        )
        conn.commit()
        conn.close()

        return request_id

    def get_history(self, limit: int = 50) -> List[Dict]:
        """
        Retorna histórico de chamadas

        Args:
            limit: Número máximo de registros

        Returns:
            Lista de chamadas
        """
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * FROM calls
            ORDER BY id DESC
            LIMIT ?
        """,
            (limit,),
        )
        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]

    def get_stats(self) -> Dict:
        """
        Retorna estatísticas do histórico

        Returns:
            Dicionário com estatísticas
        """
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM calls")
        total = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM calls WHERE response_status >= 400")
        errors = cursor.fetchone()[0]

        cursor.execute("SELECT AVG(duration_ms) FROM calls")
        avg_duration = cursor.fetchone()[0] or 0

        conn.close()

        return {
            "total_calls": total,
            "errors": errors,
            "avg_duration_ms": round(avg_duration, 2),
        }
