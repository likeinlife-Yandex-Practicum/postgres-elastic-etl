from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = (
    'db_config',
    'redis_config',
    'mainloop_config',
    'elastic_config',
)


class DBConfig(BaseSettings):
    name: str = Field()
    user: str = Field()
    password: str = Field()
    host: str = Field('127.0.0.1')
    port: str = Field('5432')

    model_config = SettingsConfigDict(env_prefix='postgres_', env_file='.env')


class RedisConfig(BaseSettings):
    host: str = Field('127.0.0.1')
    port: int = Field(6379)
    password: str | None = None
    charset: str = 'utf-8'
    decode_responses: bool = True

    model_config = SettingsConfigDict(env_prefix='redis_', env_file='.env')


class ElasticConfig(BaseSettings):
    host: str = Field('127.0.0.1')
    port: str = Field(9200)

    def get_hosts(self) -> str:
        return f'http://{self.host}:{self.port}'

    model_config = SettingsConfigDict(env_prefix='es_', env_file='.env')


class MainLoopConfig(BaseSettings):
    retry_time: int = Field(15)


db_config = DBConfig()  # type: ignore
redis_config = RedisConfig()  # type: ignore
mainloop_config = MainLoopConfig()  # type: ignore
elastic_config = ElasticConfig()  # type: ignore
