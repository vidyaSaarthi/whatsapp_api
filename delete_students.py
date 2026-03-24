from database import SessionLocal
import models


def delete_students_by_phone(phone_numbers):
    """Deletes specific students and their message history."""
    db = SessionLocal()
    try:
        for phone in phone_numbers:
            # 1. Delete associated messages first (to avoid integrity errors)
            db.query(models.Message).filter(models.Message.phone_number == phone).delete()

            # 2. Delete the student record
            result = db.query(models.Student).filter(models.Student.phone_number == phone).delete()

            if result > 0:
                print(f"✅ Successfully deleted student: {phone}", flush=True)
            else:
                print(f"⚠️ Student {phone} not found in database.", flush=True)

        db.commit()
    except Exception as e:
        db.rollback()
        print(f"❌ Error during deletion: {e}", flush=True)
    finally:
        db.close()


def clear_all_test_data():
    """⚠️ WARNING: Deletes EVERY student and message for a fresh start."""
    db = SessionLocal()
    try:
        db.query(models.Message).delete()
        db.query(models.Student).delete()
        db.commit()
        print("🚨 ALL data has been cleared from 'students' and 'messages' tables.", flush=True)
    except Exception as e:
        db.rollback()
        print(f"❌ Error clearing database: {e}", flush=True)
    finally:
        db.close()


if __name__ == "__main__":
    # OPTION 1: Delete specific numbers
    numbers_to_remove = ["919205774007"]
    delete_students_by_phone(numbers_to_remove)

    # OPTION 2: Uncomment the line below if you want to wipe everything for a clean test
    # clear_all_test_data()