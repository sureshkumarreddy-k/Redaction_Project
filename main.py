from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
import re
from fastapi.responses import RedirectResponse
from database import SessionLocal, engine
from models import Message, Base
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Form
app = FastAPI(
    title="Data Redaction API",
    description="API to redact sensitive information",
    version="1.0.0"
)

app.mount("/static", StaticFiles(directory="static"), name="static")

Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")

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
def redact_text(request: MessageRequest):

    if not request.message.strip():
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty"
        )
    redacted_text = redact_data(request.message)

    db = SessionLocal()

    message = Message(
        original_message=request.message,
        redacted_message=redacted_text
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    db.close()

    return {"redacted": redacted_text}


@app.get("/messages")
def get_messages():

    db = SessionLocal()

    messages = db.query(Message).all()

    db.close()

    return messages

@app.delete("/messages/{message_id}")
def delete_message(message_id: int):

    db = SessionLocal()

    message = db.query(Message).filter(
        Message.id == message_id
    ).first()

    if not message:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Message not found"
        )

    db.delete(message)
    db.commit()
    db.close()

    return {"message": "Deleted successfully"}

@app.post("/delete/{message_id}")
def delete_message_ui(message_id: int):

    db = SessionLocal()

    message = db.query(Message).filter(
        Message.id == message_id
    ).first()

    if message:
        db.delete(message)
        db.commit()

    db.close()

    return RedirectResponse(
        url="/",
        status_code=303
    )
@app.get("/")
def home(request: Request):

    db = SessionLocal()

    messages = db.query(Message).all()

    db.close()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "messages": messages
        }
    )

@app.post("/submit")
def submit_message(
        message: str = Form(...)
):

    if not message.strip():

        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty"
        )

    redacted = redact_data(message)

    db = SessionLocal()

    new_message = Message(
        redacted_message=redacted
    )

    db.add(new_message)

    db.commit()

    db.close()

    return RedirectResponse(
        url="/",
        status_code=303
    )