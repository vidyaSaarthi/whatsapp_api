from database import SessionLocal
import models
from sqlalchemy import func


def generate_report():
    db = SessionLocal()

    print("\n========================================")
    print("   📊 VidyaSaarthi Broadcast Report")
    print("========================================\n")

    try:
        # 1. Get the total counts for each status
        status_counts = db.query(models.Message.status, func.count(models.Message.id)) \
            .filter(models.Message.direction == "outbound") \
            .group_by(models.Message.status).all()

        # Convert list of tuples into a dictionary for easy reading
        counts = {status: count for status, count in status_counts}

        print(f"📤 Total Sent:      {counts.get('sent', 0)}")
        print(f"📥 Delivered:       {counts.get('delivered', 0)}")
        print(f"👀 Read (Opened):   {counts.get('read', 0)}")
        print(f"❌ Failed:          {counts.get('failed', 0)}\n")

        # 2. List the specific numbers that failed and why
        failures = db.query(models.Message).filter(models.Message.status == "failed").all()

        if failures:
            print("🚨 DETAILED FAILURES:")
            print("----------------------------------------")
            for msg in failures:
                reason = msg.error_message or "Unknown Error"
                # If it's the specific "Not on WhatsApp" error, highlight it
                if "131030" in str(msg.error_message) or "not on WhatsApp" in str(reason):
                    reason = "Number is NOT on WhatsApp"

                print(f" - {msg.phone_number}: {reason}")
        else:
            print("✅ Zero delivery failures so far!")

    except Exception as e:
        print(f"❌ Error generating report: {e}")
    finally:
        db.close()
        print("\n========================================")


if __name__ == "__main__":
    generate_report()