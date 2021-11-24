from pydantic import BaseSettings


class Config(BaseSettings):
    # Your Config Here
    mysql_host: str = "localhost"
    mysql_user: str = "root"
    mysql_passwd: str = "123456"

    class Config:
        extra = "ignore"
