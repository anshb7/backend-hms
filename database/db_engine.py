from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import urllib


server = "hms-backend.database.windows.net"
database = "hms_backend"
username = "CloudSA5e0e194b"
password = "creta@5378"


odbc_str = (
    "Driver={ODBC Driver 17 for SQL Server};"
    f"Server=tcp:{server},1433;"
    f"Database={database};"
    f"Uid={username};"
    f"Pwd={password};"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)


connect_str = f"mssql+pyodbc:///?odbc_connect={urllib.parse.quote_plus(odbc_str)}"


engine = create_engine(connect_str, echo=True, fast_executemany=True)


SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
