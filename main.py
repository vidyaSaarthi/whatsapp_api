import requests
from fastapi import FastAPI, Request, Query, HTTPException, Depends
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session
import uvicorn
from templates_library import send_template_message_with_image_id, send_template_message_without_image_id, send_template_message_with_no_parameters,ACCESS_TOKEN, PHONE_NUMBER_ID
from database import engine, get_db
import models

# Automatically create the tables in PostgreSQL if they don't exist
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="VidyaSaarthi WhatsApp Webhook")

VERIFY_TOKEN = "vidyasaarthi_secret_token_123"
# ACCESS_TOKEN = "EAAS2xeH0744BQ13wuJbefNR7e9QKLx1nYlSRFOWMeK8nB5lSr0Q4yCZCeWbpizXpRnWqLJLLYZB4jSRZBjYYM6JCPSxx8oDZBNIgHEc9IcBVTBSZAydDYbqBiVFYAMGr04gZCyS8zKsn6zEik98aZB2fwF0k6qqjM9HDatcXJjbbsoO1q1lpkYL02oyWS7YVekWPPmbtlRAgCZBQRg2xcWwQSQQ2xlusPzhQMERyN6YHPJ48xpFm0p9rg2Pi6ur7JzYW6ZBHIniYDQ83VPdwZChUUdmihJxxtMqswrTQZDZD"
# PHONE_NUMBER_ID = "950042731533532"


def send_whatsapp_reply(recipient_phone: str, reply_text: str):
    # ... (Keep your existing send_whatsapp_reply function exactly the same) ...
    url = f"https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": recipient_phone,
        "type": "text",
        "text": {"preview_url": False, "body": reply_text}
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        return response
    except Exception as e:
        print(f"❌ Error sending text reply: {e}", flush=True)
        return None
    #
    # print(f"--- Meta API Debug ---", flush=True)
    # print(f"Status Code: {response.status_code}", flush=True)
    # print(f"Full Response: {response.text}", flush=True) # This tells you the TRUTH



@app.get("/webhook")
async def verify_webhook(
        hub_mode: str = Query(None, alias="hub.mode"),
        hub_challenge: str = Query(None, alias="hub.challenge"),
        hub_verify_token: str = Query(None, alias="hub.verify_token")
):
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return PlainTextResponse(content=hub_challenge, status_code=200)
    raise HTTPException(status_code=403, detail="Verification failed")


# Note the addition of the db dependency here
@app.post("/webhook")
async def receive_message(request: Request, db: Session = Depends(get_db)):
    payload = await request.json()

    value = payload.get("entry", [])[0].get("changes", [])[0].get("value", {})

    # 🛠️ STEP 1: Detect Status Updates (Sent, Delivered, Read, Failed)
    if "statuses" in value:
        status_update = value["statuses"][0]
        msg_id = status_update["id"]
        status = status_update["status"]

        # Look for the message in your DB using the wamid
        db_msg = db.query(models.Message).filter(models.Message.message_id == msg_id).first()

        if db_msg:
            db_msg.status = status

            # 🛠️ STEP 2: Handle Failures (e.g., Not on WhatsApp)
            if status == "failed":
                error = status_update.get("errors", [{}])[0]
                error_code = error.get("code")
                error_msg = error.get("message", "Unknown Error")
                db_msg.error_message = error.get("title", "Unknown Error")

                if error_code == 131030:  # Specific code for "Recipient not on WhatsApp"
                    print(f"❌ {db_msg.phone_number} is NOT on WhatsApp.", flush=True)
                elif "ecosystem" in error_msg.lower() or "spam" in error_msg.lower():
                    print(f"⚠️ Ecosystem Block! Deactivating student: {db_msg.phone_number}", flush=True)
                    student = db.query(models.Student).filter(
                        models.Student.phone_number == db_msg.phone_number).first()
                    if student:
                        student.opt_in_status = False

            db.commit()
            print(f"📈 Status Updated: {db_msg.phone_number} is now {status}", flush=True)

        return {"status": "success"}


    # inbound_log = models.Message(phone_number='hi', message_text='hello', direction="inbound")
    # db.add(inbound_log)
    # db.commit()

    try:
        entry = payload.get("entry", [])[0]
        changes = entry.get("changes", [])[0]
        value = changes.get("value", {})


        # inbound_log = models.Message(phone_number=entry, message_text=value, direction="inbound")
        # db.add(inbound_log)
        # db.commit()


        if "messages" in value:
            message = value["messages"][0]
            student_phone = message["from"]
            msg_type = message["type"]

            # 🛠️ STEP 1: Extract the unique Message ID (wamid)
            wamid = message["id"]

            # 🛠️ FIX 1: Ensure student exists REGARDLESS of message type
            student = db.query(models.Student).filter(models.Student.phone_number == student_phone).first()
            if not student:
                print(f"👤 Adding new student: {student_phone}", flush=True)
                student = models.Student(phone_number=student_phone, opt_in_status=True)
                db.add(student)
                db.commit()

            if msg_type == "text":
                text_body = message["text"]["body"]
            elif msg_type == "button":
                text_body = message["button"]["text"]
            else:
                text_body = f"Unsupported type: {msg_type}"

            # 🛠️ FIX 2: Unified INBOUND logging (Works for text AND buttons)
            inbound_log = models.Message(
                message_id=wamid,
                phone_number=student_phone,
                message_text=text_body,
                direction="inbound",
                status="received"
            )

            # Prevent duplicate logging
            existing = db.query(models.Message).filter(models.Message.message_id == wamid).first()
            if not existing:
                db.add(inbound_log)
                db.commit()

            # --- DECISION LOGIC ---
            text_lower = text_body.lower()
            api_response = None
            template_sent = ""

            if text_lower == "stop":
                student.opt_in_status = False
                db.commit()
                print(f"🛑 {student_phone} opted out.", flush=True)
                # Optional: Send an opt-out confirmation template here
            elif msg_type == "text":
                if "call" in text_lower:
                    print(f"📞 {student_phone} requested a callback!", flush=True)
                    # 1. Send the confirmation to the student
                    reply_text = "Thank you! A VidyaSaarthi expert will call you shortly to assist with your admission journey."
                    api_response = send_whatsapp_reply(student_phone, reply_text)
                    template_sent = "Freeform: Callback Confirmation"

                    # send_team_alert(student_phone, "URGENT 📞: Student explicitly requested a CALL back right now!")
                else:
                    # print("I am in else",student_phone,template_sent)
                    template_sent = "vs_welcome_message_marketing"
                    api_response = send_template_message_with_no_parameters(student_phone, template_sent)

            elif msg_type == "button":
                print(f"🔘 Student clicked: {text_body}", flush=True)

                if text_body.lower() == "Shortlisted exams".lower():
                    api_response = send_template_message_with_no_parameters(student_phone, "vs_jee_shortlisted_exams")
                elif text_body.lower() == 'Find my best exam'.lower():
                    api_response = send_template_message_with_no_parameters(student_phone, "vs_jee_find_my_best_exam")
                elif text_body.lower() == 'Govt. Colleges'.lower():
                    api_response = send_template_message_with_no_parameters(student_phone, "vs_jee_govt_colleges")
                elif text_body.lower() == 'Private Colleges'.lower():
                    api_response = send_template_message_with_no_parameters(student_phone, "vs_jee_private_colleges")
                elif text_body.lower() == 'Back up options'.lower():
                    api_response = send_template_message_with_no_parameters(student_phone, "vs_jee_show_backup_options")
                elif text_body.lower() == 'Talk to expert'.lower():
                    api_response = send_template_message_with_no_parameters(student_phone, "vs_jee_talk_to_expert")
                    student.opt_in_status = False
                    db.commit()
                elif text_body.lower() == 'Stop'.lower():
                    api_response = send_template_message_with_no_parameters(student_phone, "vs_jee_stop")
                elif text_body.lower() == 'Apply with Guidance'.lower():
                    api_response = send_template_message_with_no_parameters(student_phone, "vs_jee_apply_with_guidance")
                elif text_body.lower() == 'Request Callback'.lower():
                    # pass #reply mesage should go , #telgram alert
                    reply_text = "Thank you! A VidyaSaarthi expert will call you shortly to assist with your admission journey."
                    api_response = send_whatsapp_reply(student_phone, reply_text)
                    template_sent = "Freeform: Callback Confirmation"

                else:
                    api_response = send_template_message_with_no_parameters(recipient_phone=student_phone,
                                                             template_name="vs_welcome_message_marketing")

            print(api_response,api_response.status_code,api_response.json(),api_response.json()['messages'][0]['id'])
            # 🛠️ FIX 3: Capture and log the OUTBOUND message
            if api_response and api_response.status_code == 200:
                outbound_data = api_response.json()
                outbound_wamid = outbound_data['messages'][0]['id']

                outbound_log = models.Message(
                    message_id=outbound_wamid,
                    phone_number=student_phone,
                    message_text=f"Template: {template_sent}",
                    direction="outbound",
                    status="sent"
                )
                db.add(outbound_log)
                db.commit()
                print(f"✅ Outbound logged for {student_phone} (ID: {outbound_wamid})", flush=True)

            return {"status": "success"}

    except Exception as e:
        print("Exception - {0}".format(e), flush=True)
        return {"status": "failure"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

# SOP
# change access token
# ./ngrok.exe http 8000
# python .\main.py
# http://127.0.0.1:4040/inspect/http