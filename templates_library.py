import requests

ACCESS_TOKEN = "EAAS2xeH0744BRGJamgZAsDAwn9Fm4gBZC3CvoKSpkmnluxD3XD7ssPgzMzor8oZCMaS0Og614AdIqYWzTFVEWXDnFKMyNTefZBD5KPqZAp97lYqXwVil7ufIlaDYw6Bv1iA2VKqVsUy7RdZCWzudDbj6woPhI9hKsS79zZACgVr5pSIdcahxmwh0NhCvCWnGT11F6pi9P6tIc3N3gYHZApJXzQlVkSPJgDgSObGN"
PHONE_NUMBER_ID = "987112257823129"

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


