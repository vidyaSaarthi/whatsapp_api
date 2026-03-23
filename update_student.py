from database import SessionLocal
import models


def update_student_name(phone, new_name):
    db = SessionLocal()
    try:
        # 1. Find the student by their unique phone number
        student = db.query(models.Student).filter(models.Student.phone_number == phone).first()

        if student:
            old_name = student.name
            # 2. Update the name attribute
            student.name = new_name
            db.commit()
            print(f"✅ Success: Updated {phone} from '{old_name}' to '{new_name}'.")
        else:
            print(f"❌ Error: No student found with phone number {phone}.")

    except Exception as e:
        db.rollback()
        print(f"⚠️ An error occurred: {e}")
    finally:
        db.close()

def update_student_opt_in_status(phone, new_status):
    db = SessionLocal()
    try:
        # 1. Find the student by their unique phone number
        student = db.query(models.Student).filter(models.Student.phone_number == phone).first()

        if student:
            old_status = student.opt_in_status
            # 2. Update the name attribute
            student.opt_in_status = new_status
            db.commit()
            print(f"✅ Success: Updated {phone} from '{old_status}' to '{new_status}'.")
        else:
            print(f"❌ Error: No student found with phone number {phone}.")

    except Exception as e:
        db.rollback()
        print(f"⚠️ An error occurred: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    update_student_name("919896490308", "Vinay Singh Raghuvanshi")
    # update_student_opt_in_status("918377837545",True)