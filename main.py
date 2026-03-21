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
    response = requests.post(url, headers=headers, json=payload)

    print(f"--- Meta API Debug ---", flush=True)
    print(f"Status Code: {response.status_code}", flush=True)
    print(f"Full Response: {response.text}", flush=True) # This tells you the TRUTH



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
                db_msg.error_message = error.get("title", "Unknown Error")

                if error_code == 131030:  # Specific code for "Recipient not on WhatsApp"
                    print(f"❌ {db_msg.phone_number} is NOT on WhatsApp.", flush=True)

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

            # # 2. Log the INBOUND message
            # inbound_log = models.Message(phone_number=student_phone, message_text=msg_type, direction="inbound")
            # db.add(inbound_log)
            # db.commit()
            reply_message = ''

            if msg_type == "text":
                text_body = message["text"]["body"]

                # 1. Check if this is a new student; if so, add them to the DB
                student = db.query(models.Student).filter(models.Student.phone_number == student_phone).first()
                print(student, student_phone)

                if not student:
                    print("I am in not student condition")
                    student = models.Student(phone_number=student_phone)
                    db.add(student)
                    db.commit()

                # 🆕 3. HANDLE OPT-OUT (STOP)
                text_lower = text_body.lower()
                if text_lower == "stop":
                    if student:
                        student.opt_in_status = False
                        db.commit()

                else:
                    print("I am in new template")
                    send_template_message_with_no_parameters(recipient_phone=student_phone,template_name="vs_welcome_message_marketing")

                    # reply_message = "Welcome! How can we help you with your admission journey today?"

            elif msg_type == "button":
                text_body = message["button"]["text"]
                print(f"Student clicked button: {text_body}", flush=True)

                # 2. Log the INBOUND message
                inbound_log = models.Message(message_id=wamid, phone_number=student_phone, message_text=text_body,
                                             direction="inbound", status="received")
                db.add(inbound_log)
                db.commit()


                if text_body.lower() == "Shortlisted exams".lower():
                    send_template_message_with_no_parameters(student_phone, "vs_jee_shortlisted_exams")
                elif text_body.lower() == 'Find my best exam'.lower():
                    send_template_message_with_no_parameters(student_phone, "vs_jee_shortlisted_exams")
                elif text_body.lower() == 'Govt. Colleges'.lower():
                    send_template_message_with_no_parameters(student_phone, "vs_jee_shortlisted_exams")
                elif text_body.lower() == 'Private Colleges'.lower():
                    send_template_message_with_no_parameters(student_phone, "vs_jee_shortlisted_exams")
                elif text_body.lower() == 'Back up options'.lower():
                    send_template_message_with_no_parameters(student_phone, "vs_jee_shortlisted_exams")
                elif text_body.lower() == 'Talk to expert'.lower():
                    send_template_message_with_no_parameters(student_phone, "vs_jee_shortlisted_exams")
                elif text_body.lower() == 'Stop'.lower():
                    send_template_message_with_no_parameters(student_phone, "vs_jee_shortlisted_exams")
                elif text_body.lower() == 'Apply with Guidance'.lower():
                    send_template_message_with_no_parameters(student_phone, "vs_jee_shortlisted_exams")



            # 4. Fire the API call
            # send_whatsapp_reply(student_phone, reply_message)

            # 5. Log the OUTBOUND message
            # outbound_log = models.Message(phone_number=student_phone, message_text=reply_message,
            #                               direction="outbound")
            # db.add(outbound_log)
            # db.commit()

            print(f"✅ Transaction complete and logged for {student_phone}", flush=True)

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