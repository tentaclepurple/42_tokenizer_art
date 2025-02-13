import requests

DREAMSTUDIO_API = "sk-SRizgYNPJXkhEmUsKYuCbJNvKC5MkMQdIqUxHiEoRz8x1jIu"

response = requests.post(
    f"https://api.stability.ai/v2beta/stable-image/generate/ultra",
    headers={
        "authorization": f"Bearer {DREAMSTUDIO_API}",
        "accept": "image/*"
    },
    files={"none": ''},
    data={
        "prompt": "Lighthouse on a cliff overlooking the ocean",
        "output_format": "png",
        "width": 512,
        "height": 512,
    },
)

if response.status_code == 200:
    with open("./lighthouse.png", 'wb') as file:
        file.write(response.content)
else:
    raise Exception(str(response.json()))