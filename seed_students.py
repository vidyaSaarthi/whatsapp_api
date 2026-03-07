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


if __name__ == "__main__":
    import_students_from_excel("students_list.xlsx")