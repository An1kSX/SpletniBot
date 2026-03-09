import asyncpg

from app.core.config import settings


async def create_database_if_not_exists() -> None:
	conn = await asyncpg.connect(
		host=settings.postgres_host,
		port=settings.postgres_port,
		user=settings.postgres_user,
		password=settings.postgres_password or None,
		database="postgres",
	)

	try:
		exists = await conn.fetchval(
			"SELECT 1 FROM pg_database WHERE datname = $1",
			settings.postgres_db
		)

		if not exists:
			await conn.execute(f'CREATE DATABASE "{settings.postgres_db}"')
	finally:
		await conn.close()