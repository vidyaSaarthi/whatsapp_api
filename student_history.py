from database import SessionLocal
import models
from sqlalchemy import asc


def print_student_timeline(phone: str):
    """Prints a visual, chronological timeline of a student's conversation."""
    db = SessionLocal()

    try:
        # 1. Clean the phone input and find the student
        clean_phone = str(phone).strip()
        student = db.query(models.Student).filter(models.Student.phone_number == clean_phone).first()

        if not student:
            print(f"\n❌ No student found matching Phone: '{clean_phone}'")
            return

        display_name = student.name if student.name else "Unknown Name"

        # 2. Fetch ALL messages (both inbound and outbound) in chronological order
        messages = db.query(models.Message).filter(
            models.Message.phone_number == clean_phone
        ).order_by(asc(models.Message.timestamp)).all()

        # 3. Print the header
        print(f"\n=======================================================")
        print(f" 📜 VidyaSaarthi Conversation Timeline")
        print(f"=======================================================")
        print(f" 👤 Name:  {display_name}")
        print(f" 📱 Phone: {clean_phone}")
        print(f" 🏷️ Tags:  {student.campaign_tags if student.campaign_tags else 'None'}")
        print(f"=======================================================\n")

        if not messages:
            print("   [No conversation history found.]\n")
            return

        # 4. Print the visual timeline
        for msg in messages:
            # Format time beautifully: "Mar 25, 02:30 PM"
            time_str = msg.timestamp.strftime('%b %d, %I:%M %p') if msg.timestamp else "Unknown Time"

            if msg.direction == "inbound":
                # What the student sent/clicked
                print(f"[{time_str}] 🧑 {display_name}:")
                print(f"      💬 \"{msg.message_text}\"")
            else:
                # What the bot sent
                print(f"[{time_str}] 🤖 VidyaSaarthi Bot:")
                print(f"      📤 {msg.message_text} (Status: {msg.status})")

            # Print a little arrow to connect the timeline
            print("        ↓")

        print("      [End of History]\n")

    except Exception as e:
        print(f"\n❌ Error generating timeline: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    # Test it by pasting a real number from your database here:
    ph_nbr = str(input("Enter the phone number to explore:-"))
    print_student_timeline("91"+ ph_nbr)
