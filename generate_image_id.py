import requests
from templates_library import ACCESS_TOKEN, PHONE_NUMBER_ID


# Just type the name of the image file you want to upload
IMAGE_NAME = r"H:\My Drive\Business\Vidya Saarthi\2026\WhatsApp API\jee_exams_pic_for_whtsapp_api_3.jpg"


def generate_image_id():
    url = f"https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/media"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    data = {
        "messaging_product": "whatsapp"
    }

    try:
        # The "rb" means it reads the image file as raw binary data
        with open(IMAGE_NAME, "rb") as image_file:
            files = {
                "file": (IMAGE_NAME, image_file, "image/jpeg")
            }

            print(f"⏳ Uploading {IMAGE_NAME} to Meta...", flush=True)
            response = requests.post(url, headers=headers, data=data, files=files)
            result = response.json()

            if response.status_code == 200:
                print(f"\n✅ Success! Here is your Meta Media ID:")
                print(f"👉 {result['id']} 👈")
            else:
                print(f"\n❌ Upload Failed: {result}")

    except FileNotFoundError:
        print(f"❌ Could not find '{IMAGE_NAME}'. Make sure it is in the same folder as this script!")


if __name__ == "__main__":
    generate_image_id()

'''
jee_exams_pic_for_whtsapp_api.jpeg - 1475964460909120
jee_exams_pic_for_whtsapp_api_2.jpeg - 1644488673556980
jee_exams_pic_for_whtsapp_api_3.jpeg - 2666370707096324
'''