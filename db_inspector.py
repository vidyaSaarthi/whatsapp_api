from sqlalchemy import inspect, text
from database import engine, SessionLocal
from tabulate import tabulate


def show_all_tables():
    inspector = inspect(engine)
    db = SessionLocal()

    # 1. Get all table names
    tables = inspector.get_table_names()
    print(f"📊 Database Tables Found: {', '.join(tables)}\n")

    for table_name in tables:
        print(f"--- Table: {table_name} ---")
        try:
            # 2. Fetch column names
            columns = [col['name'] for col in inspector.get_columns(table_name)]

            # 3. Fetch data (limit to 10 for quick preview)
            result = db.execute(text(f"SELECT * FROM {table_name}"))
            data = result.fetchall()

            if data:
                print(tabulate(data, headers=columns, tablefmt="grid"))
            else:
                print(f"Empty table: {table_name}")
            print("\n")

        except Exception as e:
            print(f"Error reading table {table_name}: {e}")

    db.close()


if __name__ == "__main__":
    show_all_tables()