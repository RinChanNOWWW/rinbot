from pydantic import BaseSettings


class Config(BaseSettings):
    # Your Config Here
    bupt_username: str = ""
    bupt_password: str = ""

    class Config:
        extra = "ignore"
