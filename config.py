
import os
from pydantic import BaseSettings
from pydantic.networks import stricturl



class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int


    # arquivo .env possui os valores de configuração acima. Agra podemos utilizar o arquivo 
    class Config:
        env_file=".env"


settings = Settings()