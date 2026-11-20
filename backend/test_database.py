
from app.services.database_service import get_connection

with get_connection() as connection:
    with connection.cursor() as cursor:
        cursor.execute("SELECT current_database(), version()")
        result = cursor.fetchone()

        print("Database:", result[0])
        print("PostgreSQL version:", result[1].split(",")[0])

print("Database connection successful!")
