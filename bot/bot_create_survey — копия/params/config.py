from pydantic_settings import BaseSettings

class Config(BaseSettings):
    postgres_db: str
    postgres_user: str
    postgres_password: str
    db_host: str
    db_port: int
    bot_token: str

    class Config:
        env_file = '.env'
    @property
    def db_url(self) -> str:
        return f'postgresql://{self.postgres_user}:{self.postgres_password}@{self.db_host}:{self.db_port}/{self.postgres_db}'
    
config = Config(_env_file='.env', _env_file_encoding='utf-8')


