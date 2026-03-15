from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
	model_config = SettingsConfigDict(
		extra="ignore"
	)

	bot_token: str = Field(..., alias="BOT_TOKEN")

	spletni_channel_id: int = Field(..., alias="SPLETNI_CHANNEL_ID")
	secret_channel_id: int = Field(..., alias="SECRET_CHANNEL_ID")
	admin_group_id: int = Field(..., alias="ADMIN_GROUP_ID")

	postgres_host: str = Field("db", alias="POSTGRES_HOST")
	postgres_port: int = Field(5432, alias="POSTGRES_PORT")
	postgres_db: str = Field("spletni", alias="POSTGRES_DB")
	postgres_user: str = Field("bot", alias="POSTGRES_USER")
	postgres_password: str = Field("", alias="POSTGRES_PASSWORD")

	redis_host: str = Field("redis", alias="REDIS_HOST")
	redis_port: int = Field(6379, alias="REDIS_PORT")

	log_level: str = Field("INFO", alias="LOG_LEVEL")

	@property
	def postgres_dsn(self) -> str:
		if self.postgres_password:
			return (
				f"postgresql://{self.postgres_user}:{self.postgres_password}"
				f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
			)

		return (
			f"postgresql://{self.postgres_user}"
			f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
		)

	@property
	def redis_dsn(self) -> str:
		return f"redis://{self.redis_host}:{self.redis_port}/0"

	@property
	def reply_url(self) -> str:
		channel_id = int(
				str(spletni_channel_id).replace("-100", "")
				)
		return f"https://t.me/c/{channel_id}/"


settings = Settings()