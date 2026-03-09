from pathlib import Path

from app.core.config import settings
from app.core.logger import ModuleLogger
from app.database.db import database


logger = ModuleLogger(
	module_name=__name__,
	log_level=settings.log_level
).get_logger()


async def init_db() -> None:
	schema_path = Path(__file__).resolve().parent / "schema.sql"
	schema_sql = schema_path.read_text(encoding="utf-8")

	await database.execute_script(schema_sql)

	logger.info("Database initialized")