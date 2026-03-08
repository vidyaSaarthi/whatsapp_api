import requests
import json

def get_media_id(file_path, access_token, phone_number_id):
    # API URL for media upload
    url = f"https://graph.facebook.com/v21.0/{phone_number_id}/media"

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    # 🆕 FIX: messaging_product must be in 'data', not 'files'
    payload_data = {
        "messaging_product": "whatsapp"
    }

    files = {
        "file": ("logo.png", open(file_path, "rb"), "image/png")
    }

    # We send both 'data' and 'files' now
    response = requests.post(url, headers=headers, data=payload_data, files=files)
    data = response.json()

    if "id" in data:
        print(f"✅ Success! Media ID: {data['id']}")
        return data["id"]
    else:
        print("❌ Upload Failed!")
        print(json.dumps(data, indent=2))
        return None


# --- CONFIGURATION ---
ACCESS_TOKEN = "EAAS2xeH0744BQ7uiyZAhDBfxKHJZBZCPZBnlwFOOGynZAkl12kIbiI2dvkZAsgeBLYLr6ZB1ryvApeZBWqEvpfhDXNuMf9A2BI6fU99el9pmloXy3zsvpazyD2BLgr46ELcxgOoOcK8TC8H4xuBK4ZAjj8NAJJlQkrIninZCkN2wLqXEUiLWx51ypTFjvxZAYJ8u9vZAz8RDcUNCOah5FhzKWrk6FP6VFD3ngBi60F6CJ0SycV2AyKumDKfONtfTY0eZCiVD4BjEVw2VmZC9UVtP9MuDMqx9ZCXbdzinX4J1MtvMAZDZD"  # Update if your 24hr token expired
PHONE_NUMBER_ID = "987112257823129"  # The +1 555 Test Number ID
FILE = "VidyaSaarthi Logo 30-11-2025.png"  # Ensure this file is in the same folder as this script


media_id = get_media_id(FILE, ACCESS_TOKEN, PHONE_NUMBER_ID)
#merdoa id returned - 958645420044903