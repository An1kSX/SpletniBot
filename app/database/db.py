import os
import asyncio
import aiomysql
from pymysql.err import IntegrityError
from app.core.logger import ModuleLogger

logger = ModuleLogger(__name__).get_logger()


class Database:
	def __init__(self):
		self.host = os.getenv("MYSQL_HOST")
		self.port = int(os.getenv("MYSQL_PORT", "3306"))
		self.user = os.getenv("MYSQL_USER")
		self.password = os.getenv("MYSQL_PASSWORD")
		self.dbname = os.getenv("MYSQL_DBNAME")

		missing = [n for n, v in [
			("HOST", self.host),
			("USER", self.user),
			("PASSWORD", self.password),
			("DATABASE", self.dbname),
		] if not v]

		if missing:
			raise ValueError(f"Missing required env vars: {', '.join(missing)}")

		self.db = None

	async def __aenter__(self):
		self.db = await aiomysql.connect(
			host=self.host,
			port=self.port,
			user=self.user,
			password=self.password,
			db=self.dbname,
			autocommit=True,
		)
		return self.db

	async def __aexit__(self, exc_type, exc_value, traceback):
		try:
			if exc_type is not None:
				try:
					await self.db.rollback()

				except Exception:
					pass
		finally:
			if self.db is not None:
				self.db.close()
				self.db = None

	async def execute_query(self, query: str, params: tuple = ()):
		try:
			logger.info(f"query: {query}, params: {params}")

			async with Database() as db:
				async with db.cursor(aiomysql.DictCursor) as cursor:
					await cursor.execute(query, params)

					if cursor.description is not None:
						rows = await cursor.fetchall()
						return rows

					info = {"rowcount": cursor.rowcount, "lastrowid": cursor.lastrowid}
					
					return info

		except IntegrityError as e:
			logger.error(f'IntegrityError: {e}, query: {query}, params: {params}')
			raise

		except Exception as e:
			logger.error(f'aiomysql error: {e}, query: {query}, params: {params}')
			raise


database = Database()