import requests

ACCESS_TOKEN = "EAAS2xeH0744BRBoNhcZC94wyZBu4OhmlJIEQYABHyIdH6TQNl7g0baEaA9ZAUF6f3o1IHVWOX9ZAbOVpSdnTp4As3HfWZAkikknXsKWR0DQorzlZAPq2GjUxSJOnRhEZCX6FWp2twbhP82agte87c63eU4dkXwnsnS8ZBYoWPkPCmtHsDrF46Yba7PGqgteDbZAJLuvHdgPvpiBUGahictNRyOuzB2gRCtxVnMZCbGsPCw1nMgGpz2VlETDnmIvBUFsTlyHBuuaxkfwZB5hP0eY2fa8olaQFJKgQZBxdO5EZD"
PHONE_NUMBER_ID = "987112257823129"  # The +1 555 Test Number ID

#vs_jee_missed_exams
import requests

def send_template_message_without_image_id(recipient_phone: str, template_name: str, student_name: str):
    """Sends an approved Meta template message containing ONLY a text variable {{1}}."""
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
            "language": {"code": "en"},
            "components": [
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

    try:
        response = requests.post(url, headers=headers, json=payload)
        return response
    except Exception as e:
        print(f"❌ Error sending template without image: {e}")
        return None


def send_template_message_with_image_id(recipient_phone: str, template_name: str, student_name: str, image_id: str):
    """Sends an approved Meta template message containing an Image Header and a text variable {{1}}."""
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
            "language": {"code": "en"},
            "components": [
                {
                    "type": "header",
                    "parameters": [
                        {
                            "type": "image",
                            "image": {
                                "id": image_id  # 🆕 Now dynamic so you can reuse this function
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

    try:
        response = requests.post(url, headers=headers, json=payload)
        return response
    except Exception as e:
        print(f"❌ Error sending template with image: {e}")
        return None


def send_template_message_with_no_parameters(recipient_phone: str, template_name: str):
    """Sends a purely static approved Meta template message."""
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
            "language": {"code": "en"},
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        return response
    except Exception as e:
        print(f"❌ Error sending static template: {e}")
        return None
'''
To get media id:-

ACCESS_TOKEN = "EAAS2xeH0744BQzEfVRxxISAkZAueH1SJGyioTvZB2332HaPwWsXziAbRep3nYHGA4U6ZBGKP9VsBZCbN3IkEXzjNyvCN277ETqjdDf3vYkkrlcL9EL1947PQ4Vri6XhEdiDr6Qn7ZAw7egstZCapGNs2nptayxZCfeBmdsowpAHcujxKn3VGFlMBF8yBYbuYC4QbKqs3NlaKZBfOAKHRTo7QNeSX8oqgkzkUZAcmDU6R8ZCjsipnYgDbVYgggORjEI8SNJ8KnEGcHt0RqD355yIjBa3bDtZAy8hqpnFGwZDZD"  # Update if your 24hr token expired
PHONE_NUMBER_ID = "987112257823129"  # The +1 555 Test Number ID

run below in cmd
curl -X POST "https://graph.facebook.com/v18.0/987112257823129/media" -H @{ "Authorization: Bearer EAAS2xeH0744BRG1K05rPZASSurVQILom4Jdl6cPyWZANbZBqaLlITQC0ZBn7T085J48Mj8K9f02SUMK6SiPDep44ORVE8oMZAX2fTSIUQiGorMNZAhNA4vfZAQrZBjDZCEaMA1LgM9yfV5QZATSH0EvfTybjYZBVNVZA9lLUO9DUFOHpvaoZAak5BQxAMgnp9jhOMtZCrzTkDSkpfVtqKYwr5UxkYqiqZAfLQsc6hOjz2oOO4LC8dAugb6goQHWRWZB9npxkiuZBZAm7Sauye01KC2IeBaU1zjbSzsmArCDlpaRwZDZD" }  -F "file=@C:/Users/Shubham Aggarwal/Downloads/jee_exams_pic_for_whtsapp_api.jpeg" -F "type=image/jpeg" -F "messaging_product=whatsapp"

'''

