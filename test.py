import pyodbc

password="creta@5378"
conn = pyodbc.connect(
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=tcp:hms-backend.database.windows.net,1433;"
    "Database=hms_backend;"
    "Uid=CloudSA5e0e194b;"
    f"Pwd={password};"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)
print("Connected!")


