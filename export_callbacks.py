import pandas as pd
from datetime import datetime
from database import SessionLocal
import models
from sqlalchemy import desc


def export_callbacks_to_excel():
    """Exports all callback requests to Excel and prints them to the terminal."""
    db = SessionLocal()

    timestamp_str = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"VidyaSaarthi_Callbacks_{timestamp_str}.xlsx"

    print("\n⏳ Extracting callback requests from the database...", flush=True)

    try:
        callback_records = db.query(models.Message, models.Student) \
            .join(models.Student, models.Message.phone_number == models.Student.phone_number) \
            .filter(models.Message.message_text == "Request Callback" or models.Message.message_text.ilike("%call%")) \
            .order_by(desc(models.Message.timestamp)) \
            .all()

        if not callback_records:
            print("✅ All caught up! No pending callback requests to export.")
            return

        export_data = []
        for message, student in callback_records:
            req_time = message.timestamp.strftime('%Y-%m-%d %I:%M %p') if message.timestamp else "Unknown"

            export_data.append({
                "Student Name": student.name if student.name else "Not Provided",
                "Phone Number": student.phone_number,
                "Request Time": req_time,
                "Counselor Notes": "",
                "Status": "Pending"
            })

        # Convert to a Pandas DataFrame
        df = pd.DataFrame(export_data)

        # 🚨 NEW: Print the DataFrame cleanly to the terminal
        print("\n📊 Live Data Preview:")
        print("=" * 70)
        print(df.to_string(index=False))
        print("=" * 70 + "\n")

        # Generate the Excel file
        df.to_excel(filename, index=False, engine='openpyxl')

        print(f"🎉 Success! Exported {len(export_data)} hot leads.")
        print(f"📁 File saved as: {filename}\n")

    except ImportError:
        print("❌ Error: You need the 'openpyxl' library to write Excel files.")
        print("👉 Run this in your terminal: pip install openpyxl")
    except Exception as e:
        print(f"❌ Error generating Excel export: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    export_callbacks_to_excel()