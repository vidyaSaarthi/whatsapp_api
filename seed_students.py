import pandas as pd
from database import SessionLocal
import models



import pandas as pd
from database import SessionLocal
import models


def import_students_from_excel(file_path):
    db = SessionLocal()

    print(f"\n⏳ Starting VidyaSaarthi database import from: {file_path}")

    try:
        # 1. Read the Excel file
        df = pd.read_excel(file_path)

        new_count = 0
        updated_count = 0

        # 2. Iterate through rows
        for index, row in df.iterrows():
            # Safely handle empty name fields
            name = str(row['Name']).strip() if pd.notna(row.get('Name')) else None

            # Ensure phone is a string and remove any decimal points from Excel formatting
            try:
                phone = str(int(row['Phone'])).strip()
            except (ValueError, TypeError):
                print(f"  ⚠️ Skipping row {index + 2}: Invalid or missing phone number.")
                continue

            # 🚨 NEW: Safely grab the campaign tag if the column exists in the Excel file
            campaign_tag = ""
            if 'Campaign' in df.columns and pd.notna(row['Campaign']):
                campaign_tag = str(row['Campaign']).strip()
            elif 'Tags' in df.columns and pd.notna(row['Tags']):
                campaign_tag = str(row['Tags']).strip()

            # 3. Check if the student already exists in the database
            existing_student = db.query(models.Student).filter(models.Student.phone_number == phone).first()

            if not existing_student:
                # Create a brand new student profile
                new_student = models.Student(
                    name=name,
                    phone_number=phone,
                    opt_in_status=True,
                    campaign_tags=campaign_tag
                )
                db.add(new_student)
                new_count += 1
            else:
                # 💡 The Smart Update: Append the new tag to an existing student
                if campaign_tag:
                    current_tags = existing_student.campaign_tags or ""

                    # Only add the tag if they don't already have it
                    if campaign_tag.lower() not in current_tags.lower():
                        # If they have existing tags, add a comma first
                        if current_tags:
                            existing_student.campaign_tags = f"{current_tags}, {campaign_tag}"
                        else:
                            existing_student.campaign_tags = campaign_tag

                        updated_count += 1

        # 4. Commit all changes at once for efficiency
        db.commit()

        print("\n========================================")
        print(" 🎉 Import Complete!")
        print(f"  • New Students Added: {new_count}")
        print(f"  • Existing Students Updated: {updated_count}")
        print("========================================\n")

    except Exception as e:
        print(f"\n❌ Error during import: {e}")
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

    # add_new_student('918377837545', "Shubham", 'ORGANIC_INBOUND')
    # add_new_student("919896904939", "VidyaSaarthi Vivekam")

    file_path = r"H:\My Drive\Business\Vidya Saarthi\2026\WhatsApp API\Students Seed 2.xlsx"
    import_students_from_excel(file_path)