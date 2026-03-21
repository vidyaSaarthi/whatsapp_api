import requests

ACCESS_TOKEN = "EAAS2xeH0744BQ0W5u5gw1ULPCJqAnsNTEICJPQxl3dJrDjE8VqZARWgL6DsPrtVEIB1T88rbPAeO26ukXRCxP0NV8AU0T3Kl1IJeeGZCwasZC9ZCoizWHxDvhIqZCmWsBxZCzIlIZBTtAi6N0iM00P55izHFk5dnf8CpenxEjvq6eqWRLIYbfV6WwVcA3J23e5hyZBPB55PYm2UstXhljagl260WsqpWWrTR98RCpCGwYSL5V3D6uVGkmPvkk1umYdgZA5JNPzv0XneGqDE8OVgMBpek2OcrhF0JWkgZDZD"
PHONE_NUMBER_ID = "987112257823129"  # The +1 555 Test Number ID

#vs_jee_missed_exams
def send_template_message_with_image_id(recipient_phone: str, template_name: str, student_name: str):
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


def send_template_message_without_image_id(recipient_phone: str, template_name: str, student_name: str):
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
                                "id": "1261148812127631"  # The ID you just generated
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

'''
To get media id:-

ACCESS_TOKEN = "EAAS2xeH0744BQzEfVRxxISAkZAueH1SJGyioTvZB2332HaPwWsXziAbRep3nYHGA4U6ZBGKP9VsBZCbN3IkEXzjNyvCN277ETqjdDf3vYkkrlcL9EL1947PQ4Vri6XhEdiDr6Qn7ZAw7egstZCapGNs2nptayxZCfeBmdsowpAHcujxKn3VGFlMBF8yBYbuYC4QbKqs3NlaKZBfOAKHRTo7QNeSX8oqgkzkUZAcmDU6R8ZCjsipnYgDbVYgggORjEI8SNJ8KnEGcHt0RqD355yIjBa3bDtZAy8hqpnFGwZDZD"  # Update if your 24hr token expired
PHONE_NUMBER_ID = "987112257823129"  # The +1 555 Test Number ID

run below in cmd
curl -X POST "https://graph.facebook.com/v18.0/987112257823129/media" -H "Authorization: Bearer EAAS2xeH0744BQ0bFoDSfdCdEle3jkzc5ZAdyVavL0Vvboze0AmhlQvxJM5cKgPjZBaPsjGN70uiLrT7EGirORG92EX5DNOmHlPq12uq7Do5PgPyTmZAygcg7xsFgkqoM2BYckLWdyLZBtcIc69FMmZBEXTILCGMlVX0zQ9OZBA7I5Bc6nC0y5ZCQVu2fXixQP9aH495TXhrSSlR6oVzEt2m5iF4Dal3ZCcHLaFQTKiB0bZBBS2gtV3P7PPjKl36oAn2lcf2nnEYheaYQmK9rYWymMAue2MAIB7QOHdJMZD"  -F "file=@C:/Users/Shubham Aggarwal/Downloads/jee_exams_pic_for_whtsapp_api.jpeg" -F "type=image/jpeg" -F "messaging_product=whatsapp"

'''

