import requests

# temp_token = 'EAAS2xeH0744BQwmjodAC1RCmH78fYjvGhQk0DDmnqbOT0nbE0jWZB4spU2cPJbEq12R9VDIZCmsIlPZC64EjD3qJrXZBARzGNWfBv3GZBZACoMXi2irA8b7EmL373v7E9H4uKUFg8ZAefVaeghnNutnWnSdQTsuCYITkE8Gst6IVSwSEdj7v09nB63s5PNCsO7ZCfMRko1NvvSNEyjGbQge7ENpUkm5I7P4zvy7zlaRaYN0CawrZAPZAWNCKGzNGhV0TGTZC1ZBzF3eeZCR5OpdsymIKI6rkiWgLvYvC9VQZDZD'
temp_token = "EAAS2xeH0744BQ2yLTnpFFZCVNSxnpbFXXZBZAV4ZAsBGPdZCoAtcHcof23KjpXZCSXh4EMxOfS4HuQyUnWdTq0XJxeZA5WnnvpaZCbtW3hutm4ZAgYmujvhmjSkagt6oBAraweYzEQuCgpEsGFhmZAqBKmMq0dAT8pUZC4n18nPiSrsj7qemKlQsbjqA3MyBOZBTCTDkfILIc1BAZARNtJrrA0zHC0GZAI1yh437GZB90mHudoWiHZCcifezJ3ZCvsU2fyx86Jg78yGO9UJuBJDjwMkJVYC5RqzYiOLtLOq67JSMZD"

def send_hello_world():
    # 1. Configuration variables
    # Replace these with the exact values from your Meta Dashboard
    phone_number_id = "950042731533532"  # E.g., 9500...
    access_token = temp_token  # Starts with EAAS...
    recipient_number = "918377837545"  # Your verified personal number

    # 2. Meta Graph API v22.0 Endpoint
    url = f"https://graph.facebook.com/v22.0/{phone_number_id}/messages"

    # 3. Required Headers
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # 4. JSON Payload for a Template Message
    payload = {
        "messaging_product": "whatsapp",
        "to": recipient_number,
        "type": "template",
        "template": {
            "name": "hello_world",
            "language": {
                "code": "en_US"
            }
        }
    }

    # 5. Execute the POST request
    try:
        response = requests.post(url, headers=headers, json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    send_hello_world()