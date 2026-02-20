import requests
from fastapi import FastAPI, Request, Query, HTTPException, Depends
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session
import uvicorn

from database import engine, get_db
import models

# Automatically create the tables in PostgreSQL if they don't exist
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="VidyaSaarthi WhatsApp Webhook")

VERIFY_TOKEN = "vidyasaarthi_secret_token_123"
ACCESS_TOKEN = "EAAS2xeH0744BQ2yLTnpFFZCVNSxnpbFXXZBZAV4ZAsBGPdZCoAtcHcof23KjpXZCSXh4EMxOfS4HuQyUnWdTq0XJxeZA5WnnvpaZCbtW3hutm4ZAgYmujvhmjSkagt6oBAraweYzEQuCgpEsGFhmZAqBKmMq0dAT8pUZC4n18nPiSrsj7qemKlQsbjqA3MyBOZBTCTDkfILIc1BAZARNtJrrA0zHC0GZAI1yh437GZB90mHudoWiHZCcifezJ3ZCvsU2fyx86Jg78yGO9UJuBJDjwMkJVYC5RqzYiOLtLOq67JSMZD"
PHONE_NUMBER_ID = "950042731533532"


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
    requests.post(url, headers=headers, json=payload)


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

    try:
        entry = payload.get("entry", [])[0]
        changes = entry.get("changes", [])[0]
        value = changes.get("value", {})

        if "messages" in value:
            message = value["messages"][0]
            student_phone = message["from"]
            msg_type = message["type"]

            if msg_type == "text":
                text_body = message["text"]["body"]

                # 1. Check if this is a new student; if so, add them to the DB
                student = db.query(models.Student).filter(models.Student.phone_number == student_phone).first()
                if not student:
                    student = models.Student(phone_number=student_phone)
                    db.add(student)
                    db.commit()

                # 2. Log the INBOUND message
                inbound_log = models.Message(phone_number=student_phone, message_text=text_body, direction="inbound")
                db.add(inbound_log)
                db.commit()

                # 3. Generate the reply
                reply_message = ""
                text_lower = text_body.lower()
                if "cutoff" in text_lower or "mcc" in text_lower:
                    reply_message = "Hi! We are fetching the detailed cutoffs of MCC 3rd round for NEET PG Counselling. A counselor will connect shortly."
                else:
                    reply_message = "Welcome! How can we help you with your admission journey today?"

                # 4. Fire the API call
                send_whatsapp_reply(student_phone, reply_message)

                # 5. Log the OUTBOUND message
                outbound_log = models.Message(phone_number=student_phone, message_text=reply_message,
                                              direction="outbound")
                db.add(outbound_log)
                db.commit()

                print(f"✅ Transaction complete and logged for {student_phone}")

    except Exception as e:
        pass

    return {"status": "success"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)