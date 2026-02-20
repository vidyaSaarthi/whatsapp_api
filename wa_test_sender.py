import requests

# temp_token = 'EAAS2xeH0744BQwmjodAC1RCmH78fYjvGhQk0DDmnqbOT0nbE0jWZB4spU2cPJbEq12R9VDIZCmsIlPZC64EjD3qJrXZBARzGNWfBv3GZBZACoMXi2irA8b7EmL373v7E9H4uKUFg8ZAefVaeghnNutnWnSdQTsuCYITkE8Gst6IVSwSEdj7v09nB63s5PNCsO7ZCfMRko1NvvSNEyjGbQge7ENpUkm5I7P4zvy7zlaRaYN0CawrZAPZAWNCKGzNGhV0TGTZC1ZBzF3eeZCR5OpdsymIKI6rkiWgLvYvC9VQZDZD'
temp_token = "EAAS2xeH0744BQ8ewTOUZC47NZCFqngjAOE2ipwHxZAQsQQtaR5lu7I5a9gWQnZBxKoZClhKGXRke7CH8iRzX1DBD9kEvPOiV1rogHXf2jlYtc3SspRtrSZC31YIafbZCMnyeO6Xd4qVAU3OpB8u3ZAhquI5viOGuwjrVOvkQFAuJvK7fmX8ILAzMQGnbZAEjllZCZCPPLWFPvcZCTvssCVz0IPL8BYRnZAlshVQuCkHlLL57mkhgX65Rn34yLGTsQWZCsI42ZB4otCAxxOjAlXRE9YK9pxmtJZB6YkJVWKoVrrMZD"

def send_hello_world():
    # 1. Configuration variables
    # Replace these with the exact values from your Meta Dashboard
    phone_number_id = "950042731533532"  # E.g., 9500...
    access_token = temp_token  # Starts with EAAS...
    recipient_number = "919896490308"  # Your verified personal number

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