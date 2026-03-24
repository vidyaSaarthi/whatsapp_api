import pandas as pd
from database import SessionLocal
import models


def import_students_from_excel(file_path):
    db = SessionLocal()

    try:
        # 1. Read the Excel file
        df = pd.read_excel(file_path)

        # 2. Iterate through rows
        for index, row in df.iterrows():
            name = str(row['Name']).strip()
            # Ensure phone is a string and remove any decimal points from Excel formatting
            phone = str(int(row['Phone'])).strip()

            # 3. Check for duplicates before adding
            exists = db.query(models.Student).filter(models.Student.phone_number == phone).first()

            if not exists:
                new_student = models.Student(
                    name=name,
                    phone_number=phone,
                    opt_in_status=True  # Default to True for new imports
                )
                db.add(new_student)

        # 4. Commit all changes at once for efficiency
        db.commit()
        print(f"Successfully imported students from {file_path}")

    except Exception as e:
        print(f"Error during import: {e}")
        db.rollback()
    finally:
        db.close()


def add_new_student(phone: str, name: str, campaign = ''):
    """Seeds a single new student into the database."""
    db = SessionLocal()

    try:
        # 1. Clean the inputs (removes accidental spaces from copy/pasting)
        clean_phone = str(phone).strip()
        clean_name = str(name).strip()

        # 2. Prevent Database Crashes: Check if the number already exists
        existing_student = db.query(models.Student).filter(models.Student.phone_number == clean_phone).first()

        if existing_student:
            print(f"⚠️ Notice: The number {clean_phone} is already registered to {existing_student.name}.")
            # Return the existing student so your code can still use it if needed
            return existing_student

        # 3. Create the new student profile
        new_student = models.Student(
            phone_number=clean_phone,
            name=clean_name,
            opt_in_status=True,  # We assume if you are manually seeding them, they are opted in
            campaign_tags=campaign
        )

        # 4. Save to the database
        db.add(new_student)
        db.commit()

        print(f"✅ Successfully seeded new student: {clean_name} ({clean_phone})")
        return new_student

    except Exception as e:
        # If anything goes wrong, rollback so the database doesn't lock up
        db.rollback()
        print(f"❌ Error seeding student: {e}")
        return None
    finally:
        db.close()


if __name__ == "__main__":
    # import_students_from_excel("students_list.xlsx")
    # add_new_student("918377837545", "Shubham Aggarwal")
    # add_new_student("919711598957", "Shruti Aggarwal")
    # add_new_student("918570068710", "Shruti Aggarwal JEE")

    add_new_student('919205774007', "Saanvi Singla", 'JEE')
    # add_new_student("919896904939", "VidyaSaarthi Vivekam")