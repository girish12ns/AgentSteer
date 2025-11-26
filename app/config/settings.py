from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str
    LOCAL_POSTGRES_URL: str  # keep only one field
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALGORITHM: str = "HS256"

    #Databse connection
    mongodb_uri:str
    mongodb_db_name:str
    data_collection_name:str
    law_collection_name:str

    #logging
    log_level:str

    #logging Dir
    LOG_DIR:str


    #auth
    SECRET_KEY:str
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    #openai api keys
    OPENAI_API_KEY:str
    
    LLM_MODEL:str
    TEMPERATURE:str
    MAX_TOKENS:int=None
    TIMEOUT:str=None
    MAX_RETRIES:int










    class Config:
        env_file = ".env.example"
        env_file_encoding = "utf-8"

settings = Settings()