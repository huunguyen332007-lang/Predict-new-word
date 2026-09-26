"""
Database connection layer.

FastAPI never talks to Postgres "directly" — it goes through a pool
that is created once at startup and closed once at shutdown.
"""
import sys
from pathlib import Path

from typing import AsyncGenerator

import asyncpg

# Thêm thư mục 'src' vào sys.path TRƯỚC KHI import module 'core'
sys.path.append(str(Path(__file__).resolve().parent.parent))

# Sau đó mới import từ 'core'
from core.config import settings

pool: asyncpg.Pool | None = None


async def init_pool() -> None:
    """Create the connection pool. Called once on app startup."""
    global pool
    pool = await asyncpg.create_pool(
        dsn=settings.database_url,
        min_size=2,
        max_size=10,
    )


async def close_pool() -> None:
    """Close the connection pool. Called once on app shutdown."""
    global pool
    if pool:
        await pool.close()
        pool = None


async def get_conn() -> AsyncGenerator[asyncpg.Connection, None]:
    """
    Dependency that hands a live connection from the pool to any
    endpoint that declares `conn=Depends(get_conn)`.
    """
    if pool is None:
        raise RuntimeError("Connection pool is not initialized.")

    async with pool.acquire() as connection:
        yield connection
