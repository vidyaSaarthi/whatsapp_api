import requests
import time
from database import SessionLocal
import models

# --- Configuration ---
ACCESS_TOKEN = "EAAS2xeH0744BQ13wuJbefNR7e9QKLx1nYlSRFOWMeK8nB5lSr0Q4yCZCeWbpizXpRnWqLJLLYZB4jSRZBjYYM6JCPSxx8oDZBNIgHEc9IcBVTBSZAydDYbqBiVFYAMGr04gZCyS8zKsn6zEik98aZB2fwF0k6qqjM9HDatcXJjbbsoO1q1lpkYL02oyWS7YVekWPPmbtlRAgCZBQRg2xcWwQSQQ2xlusPzhQMERyN6YHPJ48xpFm0p9rg2Pi6ur7JzYW6ZBHIniYDQ83VPdwZChUUdmihJxxtMqswrTQZDZD"  # Update if your 24hr token expired
PHONE_NUMBER_ID = "987112257823129"  # The +1 555 Test Number ID


def send_template_message(recipient_phone: str, template_name: str, student_name: str):
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
                "code": "en"
            },
            "components": [
                {
                    "type": "header",
                    "parameters": [
                        {
                            "type": "image",
                            "image": {
                                "id": "958645420044903"  # The ID you just generated
                            }
                        }
                    ]
                },
                {
                    "type": "body",
                    "parameters": [
                        {
                            "type": "text",
                            "text": student_name  # This fills the {{1}} variable
                        }
                    ]
                }
            ]
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
            res = send_template_message(target_number, "vs_jee_missed_exams", student.name)

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

# SOP
# change access token
# ngrok.exe http 8000
# python .\main.py
# http://127.0.0.1:4040/inspect/http