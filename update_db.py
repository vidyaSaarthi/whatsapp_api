import models
from database import engine


def recreate_messages_only():
    print("\n🗑️ Dropping ONLY the 'messages' table...", flush=True)
    models.Message.__table__.drop(engine, checkfirst=True)

    print("🏗️ Recreating the 'messages' table...", flush=True)
    models.Message.__table__.create(engine, checkfirst=True)
    print("✅ 'messages' table is fresh and ready!\n", flush=True)


def recreate_students_only():
    print("\n⚠️ Note: Because messages are linked to students, resetting students requires resetting messages too.")
    confirm = input("Are you sure you want to wipe BOTH tables? (Type 'YES'): ")

    if confirm == "YES":
        print("\n🗑️ Dropping 'messages' table to release the foreign key...", flush=True)
        models.Message.__table__.drop(engine, checkfirst=True)

        print("🗑️ Dropping 'students' table...", flush=True)
        models.Student.__table__.drop(engine, checkfirst=True)

        print("🏗️ Recreating 'students' table...", flush=True)
        models.Student.__table__.create(engine, checkfirst=True)

        print("🏗️ Recreating 'messages' table...", flush=True)
        models.Message.__table__.create(engine, checkfirst=True)
        print("✅ Both tables have been reset!\n", flush=True)
    else:
        print("🛑 Operation cancelled. No tables were dropped.\n", flush=True)


def recreate_all():
    print("\n🚨 WARNING: Dropping ALL existing tables...", flush=True)
    models.Base.metadata.drop_all(bind=engine)

    print("🏗️ Rebuilding ALL tables from scratch...", flush=True)
    models.Base.metadata.create_all(bind=engine)
    print("✅ VidyaSaarthi database is completely fresh and structured!\n", flush=True)


def display_menu():
    while True:
        print("========================================")
        print("   VidyaSaarthi Database Manager")
        print("========================================")
        print("1. Reset ONLY the 'messages' table (Keep all students)")
        print("2. Reset the 'students' table (Will also reset messages)")
        print("3. Reset the ENTIRE database")
        print("4. Exit")
        print("========================================")

        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            recreate_messages_only()
        elif choice == '2':
            recreate_students_only()
        elif choice == '3':
            confirm = input("Type 'YES' to completely wipe and rebuild the database: ")
            if confirm == "YES":
                recreate_all()
            else:
                print("🛑 Operation cancelled.\n")
        elif choice == '4':
            print("Exiting Database Manager. Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter a number between 1 and 4.\n")


if __name__ == "__main__":
    display_menu()