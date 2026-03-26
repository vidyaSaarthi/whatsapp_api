import time
from database import SessionLocal
import models
from templates_library import send_template_message_with_image_id, send_template_message_without_image_id, send_template_message_with_no_parameters

TEMPLATE_NAME = 'vs_seminar_29_march'
# TARGET_CAMPAIGN = "JEE" # Change this whenever you run a new campaign

def run_test_broadcast(ph_nbr, name):


    try:

        print(f"📢 Starting broadcast to {ph_nbr} student...", flush=True)

        send_template_message_with_image_id(ph_nbr, TEMPLATE_NAME, name, '1271782141717290')

        print("🎉 Broadcast complete!", flush=True)

    except Exception as global_e:
        print(f"🔥 A catastrophic global error occurred: {global_e}", flush=True)


if __name__ == "__main__":
    run_test_broadcast('918377837545', 'Shubham Aggarwal')

