from fastapi import FastAPI
from pydantic import BaseModel
import re

app = FastAPI(
    title="Data Redaction API",
    description="API to redact sensitive information",
    version="1.0.0"
)

class MessageRequest(BaseModel):
    message: str

def mask_email(match):
    email = match.group()
    username, domain = email.split("@")
    return "*" * len(username) + "@" + domain

def mask_mobile(match):
    number = match.group()
    return number[:2] + "******" + number[-2:]

def redact_data(text: str) -> str:
    # Email redaction
    text = re.sub(r'[\w\.-]+@[a-zA-Z]+\.[a-zA-Z]{2,}', mask_email, text)

    # Mobile number redaction (10-digit numbers)
    text = re.sub(r'\b\d{10}\b', mask_mobile, text)

    return text


@app.post("/redact")
def redact(data: MessageRequest):
    return {
        "original": data.message,
        "redacted": redact_data(data.message)
    }