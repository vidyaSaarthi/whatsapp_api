import os
from datetime import datetime
from database import SessionLocal
import models
from sqlalchemy import asc


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


if __name__ == "__main__":
    analyze_chatbot_funnel()