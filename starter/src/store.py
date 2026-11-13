"""Store and search vectors using PostgreSQL + pgvector (exact cosine search)."""
import hashlib
import json
from typing import Any

import psycopg

from .models import Chunk

# Only these metadata columns may be used in filters (never interpolated from user input).
FILTERABLE = {"chapter": "chapter", "document_id": "document_id", "page": "page"}


def content_hash(text: str, model: str) -> str:
    return hashlib.sha256(f"{model}\n{text}".encode("utf-8")).hexdigest()


def _vec(values: list[float]) -> str:
    return "[" + ",".join(repr(float(v)) for v in values) + "]"


class PgVectorStore:
    def __init__(self, database_url: str, dimensions: int) -> None:
        if dimensions <= 0:
            raise ValueError("dimensions must be positive")
        self.database_url = database_url
        self.dimensions = dimensions

    def _connect(self) -> psycopg.Connection:
        return psycopg.connect(self.database_url, connect_timeout=5)

    def create_schema(self) -> None:
        with self._connect() as conn:
            conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
            conn.execute(f"""
                CREATE TABLE IF NOT EXISTS day6_chunks (
                    strategy        text    NOT NULL,
                    chunk_id        text    NOT NULL,
                    document_id     text    NOT NULL,
                    source          text    NOT NULL,
                    page            integer NOT NULL,
                    chapter         integer NOT NULL,
                    text            text    NOT NULL,
                    content_hash    text    NOT NULL,
                    embedding_model text    NOT NULL,
                    metadata        jsonb   NOT NULL,
                    embedding       vector({self.dimensions}) NOT NULL,
                    PRIMARY KEY (strategy, chunk_id)
                )""")
            row = conn.execute("""
                SELECT format_type(a.atttypid, a.atttypmod) FROM pg_attribute a
                WHERE a.attrelid = 'day6_chunks'::regclass AND a.attname = 'embedding'""").fetchone()
            if row and row[0] != f"vector({self.dimensions})":
                raise RuntimeError(f"Existing day6_chunks.embedding is {row[0]}, model gives {self.dimensions} dims")
            conn.execute("CREATE INDEX IF NOT EXISTS day6_chunks_strategy_chapter ON day6_chunks (strategy, chapter)")

    def existing_hashes(self, strategy: str) -> dict[str, str]:
        with self._connect() as conn:
            rows = conn.execute("SELECT chunk_id, content_hash FROM day6_chunks WHERE strategy = %s",
                                (strategy,)).fetchall()
        return dict(rows)

    def count(self, strategy: str) -> int:
        with self._connect() as conn:
            return conn.execute("SELECT count(*) FROM day6_chunks WHERE strategy = %s", (strategy,)).fetchone()[0]

    def upsert(self, strategy: str, chunks: list[Chunk], vectors: list[list[float]],
               model: str, document_ids: set[str], keep_ids: list[str]) -> dict[str, int]:
        """Insert/update by stable (strategy, chunk_id); delete obsolete chunks of re-ingested documents.

        `chunks` may be only the new/changed chunks; `keep_ids` is the full current chunk set,
        so unchanged chunks are kept without re-embedding and stale ones are removed.
        """
        if len(chunks) != len(vectors):
            raise ValueError(f"{len(chunks)} chunks but {len(vectors)} vectors")
        for vector in vectors:
            if len(vector) != self.dimensions:
                raise ValueError(f"vector has {len(vector)} dims, expected {self.dimensions}")
        ids = [c.chunk_id for c in chunks]
        if len(set(ids)) != len(ids):
            raise ValueError("duplicate chunk_id in batch")
        with self._connect() as conn, conn.cursor() as cur:
            cur.executemany("""
                INSERT INTO day6_chunks (strategy, chunk_id, document_id, source, page, chapter, text,
                                    content_hash, embedding_model, metadata, embedding)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s::vector)
                ON CONFLICT (strategy, chunk_id) DO UPDATE SET
                    document_id = EXCLUDED.document_id, source = EXCLUDED.source, page = EXCLUDED.page,
                    chapter = EXCLUDED.chapter, text = EXCLUDED.text, content_hash = EXCLUDED.content_hash,
                    embedding_model = EXCLUDED.embedding_model, metadata = EXCLUDED.metadata,
                    embedding = EXCLUDED.embedding""",
                [(strategy, c.chunk_id, c.document_id, c.source, c.page, c.metadata["chapter"], c.text,
                  content_hash(c.text, model), model, json.dumps(c.metadata), _vec(v))
                 for c, v in zip(chunks, vectors)])
            cur.execute("""DELETE FROM day6_chunks WHERE strategy = %s AND document_id = ANY(%s)
                           AND NOT (chunk_id = ANY(%s))""",
                        (strategy, list(document_ids), keep_ids))
            deleted = cur.rowcount
        return {"upserted": len(chunks), "deleted_obsolete": deleted}

    def search(self, strategy: str, query_vector: list[float], top_k: int = 3,
               filters: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        """Exact cosine search (no ANN index), with SQL-side metadata filtering."""
        if len(query_vector) != self.dimensions:
            raise ValueError("query vector dimension mismatch")
        where, params = ["strategy = %s"], [strategy]
        for key, value in (filters or {}).items():
            if key not in FILTERABLE:
                raise ValueError(f"filter field {key!r} is not allowed")
            where.append(f"{FILTERABLE[key]} = %s")
            params.append(value)
        sql = f"""SELECT chunk_id, document_id, source, page, chapter, text, metadata,
                         1 - (embedding <=> %s::vector) AS score
                  FROM day6_chunks WHERE {' AND '.join(where)}
                  ORDER BY embedding <=> %s::vector, chunk_id LIMIT %s"""
        qv = _vec(query_vector)
        with self._connect() as conn:
            rows = conn.execute(sql, [qv, *params, qv, top_k]).fetchall()
        return [{"rank": i + 1, "chunk_id": r[0], "document_id": r[1], "source": r[2], "page": r[3],
                 "chapter": r[4], "text": r[5], "metadata": r[6], "score": round(float(r[7]), 6)}
                for i, r in enumerate(rows)]
