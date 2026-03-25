from database import SessionLocal
import models
from tabulate import tabulate


def show_student_list(limit=20):
    db = SessionLocal()
    try:
        # Fetch students from the database
        # We filter for active (opted-in) students by default
        students = db.query(models.Student).limit(limit).all()

        if not students:
            print("No students found in the database.")
            return

        # Format the data for the table
        table_data = []
        for s in students:
            status = "✅ Subscribed" if s.opt_in_status else "❌ Unsubscribed"
            table_data.append([s.name, s.phone_number, s.opt_in_status, s.created_at, s.campaign_tags])

        # Display using tabulate
        headers = ["Name","Phone Number", "Opt-in Status", "Created At"]
        print(f"\n--- VidyaSaarthi Student List (Showing top {limit}) ---")
        print(tabulate(table_data, headers=headers, tablefmt="grid"))

        total_count = db.query(models.Student).count()
        subscribed_count = db.query(models.Student).filter(models.Student.opt_in_status == True).count()
        print(f"\nTotal Students: {total_count} | Active Subscribers: {subscribed_count}")

    except Exception as e:
        print(f"Error fetching students: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    # You can change the limit to see more or fewer students
    show_student_list(limit=50)