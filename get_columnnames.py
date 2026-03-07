from database import engine
from sqlalchemy import inspect


def get_column_names():
    inspector = inspect(engine)
    # This retrieves the column information for the 'students' table
    columns = inspector.get_columns('students')

    print("Column names in 'students' table:")
    for column in columns:
        print(f"- {column['name']} ({column['type']})")


if __name__ == "__main__":
    get_column_names()