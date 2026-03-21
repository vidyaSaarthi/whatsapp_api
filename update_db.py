import models
from database import engine


def recreate_messages_table():
    print("🗑️ Dropping the old messages table...")
    # This specifically drops ONLY the messages table, leaving the students table safe
    models.Message.__table__.drop(engine, checkfirst=True)

    print("🏗️ Rebuilding tables from models.py...")
    # This will see that 'messages' is missing and create it with the new message_id column
    models.Base.metadata.create_all(bind=engine)

    print("✅ Database updated successfully!")


if __name__ == "__main__":
    recreate_messages_table()