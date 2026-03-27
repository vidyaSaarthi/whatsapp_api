import os, glob
from datetime import datetime
from database import SessionLocal
import models
from sqlalchemy import asc
import requests, time
from export_callbacks import export_callbacks_to_excel
from datetime import datetime, timedelta



# --- Telegram Configuration ---
TELEGRAM_BOT_TOKEN = "8526202388:AAG5bD6MSaHBh1Fzk042J5cYYmcC-PwgD84"
TELEGRAM_CHAT_ID = "@vs_whatsapp_api_alerts"  # Group IDs usually start with a minus sign (-)

def send_report_to_telegram(file_path: str):
    """Uploads the generated text file directly to a Telegram group."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument"

    print(f"\n⏳ Uploading report to Telegram group...")

    try:
        with open(file_path, "rb") as document:
            # We package the file and add a nice caption for the team
            files = {"document": document}
            data = {
                "chat_id": TELEGRAM_CHAT_ID,
                "caption": "📊 Here is the last 1 hour funnel report."
            }

            response = requests.post(url, data=data, files=files)

            if response.status_code == 200:
                print("✅ Success! The report is now in the Telegram group.")
            else:
                print(f"❌ Telegram Upload Failed: {response.text}")

    except Exception as e:
        print(f"❌ Error talking to Telegram API: {e}")


def generate_hourly_activity_report():
    """Generates a text file showing only the messages sent/received in the last 1 hour."""
    db = SessionLocal()

    timestamp_str = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"VidyaSaarthi_Last_1_Hourly_Activity_{timestamp_str}.txt"

    # Calculate the exact time 1 hour ago
    one_hour_ago = datetime.now() - timedelta(hours=1)

    try:
        # Fetch all messages from the last hour, in chronological order
        recent_messages = db.query(models.Message).filter(
            models.Message.timestamp >= one_hour_ago
        ).order_by(asc(models.Message.timestamp)).all()

        with open(filename, "w", encoding="utf-8") as file:
            def cprint(text=""):
                print(text)
                file.write(str(text) + "\n")

            cprint("\n===========================================================")
            cprint(" ⏱️ VidyaSaarthi Live Activity Ticker (Last 1 Hour)")
            cprint("===========================================================\n")

            if not recent_messages:
                cprint("  💤 No chatbot interactions occurred in the last hour.")
            else:
                for msg in recent_messages:
                    time_str = msg.timestamp.strftime('%I:%M %p') if msg.timestamp else "Unknown"

                    # Safely grab the student's name using the SQLAlchemy relationship
                    student_name = msg.student.name if msg.student and msg.student.name else "Unknown"
                    phone = msg.phone_number

                    # 🚨 NEW: Safely grab the campaign tag
                    campaign_tag = msg.student.campaign_tags if msg.student and msg.student.campaign_tags else "Unassigned / Organic"

                    if msg.direction == "inbound":
                        # 🚨 NEW: Added the tag to the printout
                        cprint(f"[{time_str}] 🧑 {student_name} ({phone}) | 🏷️ {campaign_tag}")
                        cprint(f"      💬 \"{msg.message_text}\"")
                    else:
                        # 🚨 NEW: Added the tag to the bot's printout as well
                        cprint(f"[{time_str}] 🤖 Bot -> {student_name} ({phone}) | 🏷️ {campaign_tag}")
                        cprint(f"      📤 {msg.message_text} (Status: {msg.status})")
                    cprint("        -")

            cprint(f"\n📁 Hourly activity saved to: {filename}")

            # Return the filename so the master script can send it to Telegram
            return filename

    except Exception as e:
        print(f"❌ Error generating hourly activity: {e}")
        return None
    finally:
        db.close()



def cleanup_old_reports(days_to_keep=7):
    """Scans the folder and deletes VidyaSaarthi reports older than 7 days."""
    print(f"\n🧹 Running Housekeeping: Checking for reports older than {days_to_keep} days...")

    # 1. Calculate the exact cutoff time in seconds
    now = time.time()
    cutoff_time = now - (days_to_keep * 86400)  # 86400 seconds in a day

    # 2. Define the exact file patterns so we don't accidentally delete code/DB files!
    patterns = [
        "VidyaSaarthi_Funnel_Report_*.txt",
        "VidyaSaarthi_Callbacks_*.xlsx"  # Make sure this matches your Excel export filename!
    ]

    deleted_count = 0

    # 3. Search and Destroy
    for pattern in patterns:
        for filepath in glob.glob(pattern):
            # Check the file's modification timestamp
            file_modified_time = os.path.getmtime(filepath)

            if file_modified_time < cutoff_time:
                try:
                    os.remove(filepath)
                    deleted_count += 1
                    print(f"  🗑️ Deleted: {os.path.basename(filepath)}")
                except Exception as e:
                    print(f"  ⚠️ Could not delete {filepath}: {e}")

    print(f"✅ Housekeeping complete. {deleted_count} old files removed.\n")





def analyze_chatbot_funnel():
    db = SessionLocal()

    # 1. Generate a dynamic filename with today's date and time
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"VidyaSaarthi_Funnel_Report_{timestamp}.txt"

    # 2. Open the file and create our custom dual-print function
    with open(filename, "w", encoding="utf-8") as file:

        def cprint(text=""):
            """Prints to the terminal AND saves to the text file at the same time."""
            print(text)
            file.write(str(text) + "\n")

        cprint("\n===========================================================")
        cprint(" 📊 VidyaSaarthi Interaction Lifecycle & Master Call List")
        cprint("===========================================================\n")

        try:
            students = db.query(models.Student).all()

            funnel = {
                0: [],  # Opted_Out_Immediately
                1: [],  # Read_Only_No_Action
                2: [],  # Explored_Menu
                3: []  # High_Intent
            }

            for student in students:
                inbound_messages = db.query(models.Message).filter(
                    models.Message.phone_number == student.phone_number,
                    models.Message.direction == "inbound"
                ).order_by(asc(models.Message.timestamp)).all()

                if not inbound_messages:
                    continue

                deepest_stage = 1

                for msg in inbound_messages:
                    text = msg.message_text.lower() if msg.message_text else ""

                    if text == "stop":
                        deepest_stage = 0
                    elif text in ["shortlisted exams", "find my best exam", "govt. colleges", "private colleges",
                                  "backup options"]:
                        if deepest_stage != 0:
                            deepest_stage = max(deepest_stage, 2)
                    elif text in ["talk to expert", "apply with guidance", "request callback"] or "call" in text:
                        if deepest_stage != 0:
                            deepest_stage = 3

                funnel[deepest_stage].append(student)

            # --- Helper function for printing individual student timelines ---
            def print_student_timeline(student):
                messages = db.query(models.Message).filter(
                    models.Message.phone_number == student.phone_number
                ).order_by(asc(models.Message.timestamp)).all()

                if not messages:
                    cprint("      [No conversation history found.]")
                    return

                for msg in messages:
                    time_str = msg.timestamp.strftime('%b %d, %I:%M %p') if msg.timestamp else "Unknown Time"

                    if msg.direction == "inbound":
                        cprint(f"      [{time_str}] 🧑: 💬 \"{msg.message_text}\"")
                    else:
                        cprint(f"      [{time_str}] 🤖: 📤 {msg.message_text} (Status: {msg.status})")
                    cprint("        ↓")

                cprint("      [End of History]")

            # --- Helper function to print a whole stage cleanly ---
            def print_stage(stage_title, student_list):
                cprint(f"{stage_title} ({len(student_list)} students)")
                cprint("=" * 60)
                if not student_list:
                    cprint("  [No students in this stage yet]\n")
                    return

                for student in student_list:
                    display_name = student.name if student.name else "Unknown Name"
                    cprint(f"\n👤 {display_name} (📱 {student.phone_number})")
                    cprint(f"🏷️ Tags: {student.campaign_tags if student.campaign_tags else 'None'}")
                    cprint("-" * 40)

                    print_student_timeline(student)
                    cprint("-" * 60)
                cprint("\n")

            # --- Execute the printing ---
            print_stage("🔥 STAGE 3: HIGH INTENT LEADS", funnel[3])
            print_stage("🧭 STAGE 2: EXPLORED MENU", funnel[2])
            print_stage("👀 STAGE 1: READ ONLY / NO CLICKS", funnel[1])
            print_stage("🛑 STAGE 0: OPTED OUT", funnel[0])

            cprint(f"\n📁 Report successfully saved to: {filename}")

        except Exception as e:
            cprint(f"❌ Error generating detailed funnel report: {e}")
        finally:
            db.close()

    send_report_to_telegram(filename)


if __name__ == "__main__":
    while 1:
        cleanup_old_reports()
        export_callbacks_to_excel()
        analyze_chatbot_funnel()
        send_report_to_telegram(generate_hourly_activity_report())
        print("Sleeping for 1 hour")
        time.sleep(3600)