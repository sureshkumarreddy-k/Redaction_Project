import requests

url = "http://127.0.0.1:8000/redact"

while True:
    message = input("Enter your message (type 'exit' to stop): ")

    if message.lower() == "exit":
        print("Exiting...")
        break

    data = {
        "message": message
    }

    response = requests.post(url, json=data)

    if response.status_code == 200:
        print("Redacted Output:", response.json()["redacted"])
    else:
        print("Error:", response.status_code)
        print("Message:", response.json()["detail"])