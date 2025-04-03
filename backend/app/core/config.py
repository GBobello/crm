from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str
    secret_key: str
    sqlalchemy_database_url: str
    algorithm: str
    type_product: str
    upload_folder: str

    class Config:
        env_file = ".env"


settings = Settings()
