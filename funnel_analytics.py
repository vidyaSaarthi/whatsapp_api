from database import SessionLocal
import models
from sqlalchemy import asc


def analyze_chatbot_funnel():
    db = SessionLocal()

    print("\n==================================================")
    print(" 📊 VidyaSaarthi Interaction Lifecycle & Call List")
    print("==================================================\n")

    try:
        students = db.query(models.Student).all()

        # We changed these from integers to lists so we can store the actual student data
        funnel = {
            0: [],  # Opted_Out_Immediately
            1: [],  # Read_Only_No_Action
            2: [],  # Explored_Menu
            3: []  # High_Intent
        }

        for student in students:
            messages = db.query(models.Message).filter(
                models.Message.phone_number == student.phone_number,
                models.Message.direction == "inbound"
            ).order_by(asc(models.Message.timestamp)).all()

            if not messages:
                continue

            deepest_stage = 1

            for msg in messages:
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

            # Store the student's formatted details in the correct bucket
            display_name = student.name if student.name else "Unknown Name"
            student_info = f"👤 {display_name} (📱 {student.phone_number})"
            funnel[deepest_stage].append(student_info)

        # --- Print the Detailed Output ---

        print(f"🔥 STAGE 3: HIGH INTENT LEADS ({len(funnel[3])} students)")
        print("-" * 50)
        if funnel[3]:
            for s in funnel[3]: print(f"  • {s}")
        else:
            print("  [No students in this stage yet]")
        print("\n")

        print(f"🧭 STAGE 2: EXPLORED MENU ({len(funnel[2])} students)")
        print("-" * 50)
        if funnel[2]:
            for s in funnel[2]: print(f"  • {s}")
        else:
            print("  [No students in this stage yet]")
        print("\n")

        print(f"👀 STAGE 1: READ ONLY / NO CLICKS ({len(funnel[1])} students)")
        print("-" * 50)
        if funnel[1]:
            for s in funnel[1]: print(f"  • {s}")
        else:
            print("  [No students in this stage yet]")
        print("\n")

        print(f"🛑 STAGE 0: OPTED OUT ({len(funnel[0])} students)")
        print("-" * 50)
        if funnel[0]:
            for s in funnel[0]: print(f"  • {s}")
        else:
            print("  [No students in this stage yet]")
        print("\n==================================================\n")

    except Exception as e:
        print(f"❌ Error generating detailed funnel report: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    analyze_chatbot_funnel()