import requests

ACCESS_TOKEN = "EAAS2xeH0744BQzEfVRxxISAkZAueH1SJGyioTvZB2332HaPwWsXziAbRep3nYHGA4U6ZBGKP9VsBZCbN3IkEXzjNyvCN277ETqjdDf3vYkkrlcL9EL1947PQ4Vri6XhEdiDr6Qn7ZAw7egstZCapGNs2nptayxZCfeBmdsowpAHcujxKn3VGFlMBF8yBYbuYC4QbKqs3NlaKZBfOAKHRTo7QNeSX8oqgkzkUZAcmDU6R8ZCjsipnYgDbVYgggORjEI8SNJ8KnEGcHt0RqD355yIjBa3bDtZAy8hqpnFGwZDZD"  # Update if your 24hr token expired
PHONE_NUMBER_ID = "987112257823129"  # The +1 555 Test Number ID

#vs_jee_missed_exams
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


def send_template_message_with_no_parameters(recipient_phone: str, template_name: str):
    """Sends an approved Meta template message."""
    url = f"https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages"

    print(recipient_phone,template_name)
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
        }
    }


    response = requests.post(url, headers=headers, json=payload)
    return response