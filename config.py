import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(__file__)
load_dotenv(os.path.join(BASE_DIR, ".env"))

class Config:
    SECRET_KEY= os.getenv("SECRET_KEY", "dev")

    MYSQL_USER= os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD= os.getenv("MYSQL_PASSWORD", "")
    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_PORT= os.getenv("MYSQL_PORT", "3306")  
    MYSQL_DB = os.getenv("MYSQL_DB", "tarea2")

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}"
        f"@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
print("DEBUG 1  >>  Archivo .env leído  :", os.path.join(BASE_DIR, ".env"))
print("DEBUG 2  >>  MYSQL_PORT en memoria:", os.getenv("MYSQL_PORT"))
print("DEBUG 3  >>  URI resultante       :", Config.SQLALCHEMY_DATABASE_URI)
