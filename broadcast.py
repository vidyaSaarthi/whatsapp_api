import time
from database import SessionLocal
import models
from templates_library import send_template_message_with_image_id, send_template_message_without_image_id, send_template_message_with_no_parameters

TEMPLATE_NAME = 'vs_jee_engg_forms_alert'


def run_broadcast():
    db = SessionLocal()

    try:
        active_students = db.query(models.Student).filter(models.Student.opt_in_status == True).all()
        print(f"📢 Starting broadcast to {len(active_students)} students...", flush=True)

        for student in active_students:
            target_number = student.phone_number

            # 🛠️ FIX 1: Safe Name Fallback
            # If the name is blank in the DB, default to "Student" so Meta doesn't reject it
            safe_name = getattr(student, 'name', None)
            if not safe_name:
                safe_name = "Student"

            # 🛠️ FIX 2: Inner Error Handling (Protects the Loop)
            try:
                # Send the API request
                res = send_template_message_with_image_id(target_number, TEMPLATE_NAME, safe_name, '1475964460909120')

                # 🛠️ FIX 3: Prevent crash if the function returned None due to a network error
                if res is None:
                    print(f"❌ Network error for {target_number}. Skipping...", flush=True)
                    continue

                data = res.json()

                if res.status_code == 200:
                    wamid = data['messages'][0]['id']

                    # Log the broadcast in the database
                    log_entry = models.Message(
                        message_id=wamid,
                        phone_number=target_number,
                        message_text=f"Template : {TEMPLATE_NAME}",
                        direction="outbound",
                        status="sent"
                    )
                    db.add(log_entry)
                    db.commit()  # Commit individually inside the loop
                    print(f"✅ Sent to {target_number} (ID: {wamid})", flush=True)
                else:
                    print(f"❌ Meta API Failed for {target_number}: {data}", flush=True)

            except Exception as inner_e:
                # If this specific student fails, log it, rollback their bad DB transaction, and continue the loop!
                print(f"⚠️ Unexpected error processing {target_number}: {inner_e}", flush=True)
                db.rollback()

            # Rate Limiting Protection
            time.sleep(0.1)

        print("🎉 Broadcast complete and logged!", flush=True)

    except Exception as global_e:
        print(f"🔥 A catastrophic global error occurred: {global_e}", flush=True)
        db.rollback()
    finally:
        db.close()

#
# # --- Configuration ---
#
# TEMPLATE_NAME ='vs_jee_engg_forms_alert'
#
# def run_broadcast():
#     # 1. Open database session
#     db = SessionLocal()
#
#     try:
#         # 2. Query all active students
#         # For testing, this will just find the personal number you messaged with earlier
#         active_students = db.query(models.Student).filter(models.Student.opt_in_status == True).all()
#
#         print(f"📢 Starting broadcast to {len(active_students)} students...")
#
#         # 3. Loop and send
#         for student in active_students:
#             target_number = student.phone_number
#
#             # 🛠️ FIX 1: Safe Name Fallback
#             # If the name is blank in the DB, default to "Student" so Meta doesn't reject it
#             safe_name = getattr(student, 'name', None)
#             if not safe_name:
#                 safe_name = "Student"
#
#
#             # Send the API request (Using the sandbox template)
#             res = send_template_message_without_image_id(target_number, TEMPLATE_NAME , student.name)
#             data = res.json()
#
#             if res.status_code == 200:
#                 print(f"✅ Sent successfully to {target_number}")
#
#                 # 🛠️ Extract the message ID from Meta's response
#                 wamid = data['messages'][0]['id']
#
#
#                 # 4. Log the broadcast in the database
#                 log_entry = models.Message(
#                     message_id=wamid,
#                     phone_number=target_number,
#                     message_text=f"Template : {TEMPLATE_NAME}",
#                     direction="outbound",
#                     status="sent"
#                 )
#                 db.add(log_entry)
#                 db.commit()
#                 print(f"✅ Sent to {student.phone_number} (ID: {wamid})", flush=True)
#             else:
#                 print(f"❌ Failed for {student.phone_number}: {data}", flush=True)
#
#             # 5. Rate Limiting Protection
#             # Meta allows high throughput, but a slight delay prevents sudden spikes
#             time.sleep(0.1)
#
#             # Commit all the logs to the database at once
#         db.commit()
#         print("🎉 Broadcast complete and logged!")
#
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         db.rollback()
#     finally:
#         db.close()


if __name__ == "__main__":
    run_broadcast()

# SOP
# change access token
# .\ngrok.exe http 8000
# python .\main.py
# http://127.0.0.1:4040/inspect/http