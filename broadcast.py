import requests
import time
from database import SessionLocal
import models

# --- Configuration ---
ACCESS_TOKEN = "EAAS2xeH0744BQ76uT7dhqrZB7TrDBmZBovMR2ZAisp70MTtEiUuHKTit5gfrS89l2Ar0Jbu8EBLX8Aa4E0capGeGVhLdXj05lSfGaJxFgMbvbvGEHrnKHmSw3mQNkD8ZCnbVb4umDBHQLJ5uBAZA9t0l3DCpgqAOntvZBD1Tj3igYupnxz9JL4ZBHLSry1ZBLvYZBZAnVZBDaiVqZA7HxV5JU6ZBlZC1pjPnAng0LZAMbliSd6CTF2NCkjk5hB2OmVUvt3ytdWthu2tLsO1PVj1azAuYbLxFimU78Uoht09zgZDZD"  # Update if your 24hr token expired
PHONE_NUMBER_ID = "950042731533532"  # The +1 555 Test Number ID


def send_template_message(recipient_phone: str, template_name: str):
    """Sends an approved Meta template message."""
    url = f"https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": recipient_phone,
        "type": "template",
        "template": {
            "name": template_name,
            "language": {
                "code": "en_US"
            }
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    return response


def run_broadcast():
    # 1. Open database session
    db = SessionLocal()

    try:
        # 2. Query all active students
        # For testing, this will just find the personal number you messaged with earlier
        active_students = db.query(models.Student).filter(models.Student.opt_in_status == True).all()

        print(f"📢 Starting broadcast to {len(active_students)} students...")

        # 3. Loop and send
        for student in active_students:
            target_number = student.phone_number

            # Send the API request (Using the sandbox template)
            res = send_template_message(target_number, "hello_world")

            if res.status_code == 200:
                print(f"✅ Sent successfully to {target_number}")

                # 4. Log the broadcast in the database
                log_entry = models.Message(
                    phone_number=target_number,
                    message_text="[BROADCAST: hello_world]",
                    direction="outbound"
                )
                db.add(log_entry)
            else:
                print(f"❌ Failed to send to {target_number}: {res.text}")

            # 5. Rate Limiting Protection
            # Meta allows high throughput, but a slight delay prevents sudden spikes
            time.sleep(0.1)

            # Commit all the logs to the database at once
        db.commit()
        print("🎉 Broadcast complete and logged!")

    except Exception as e:
        print(f"An error occurred: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    run_broadcast()