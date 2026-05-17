from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


# 1. Email redaction (partial masking)
def test_email_redaction():
    response = client.post(
        "/redact",
        json={"message": "Email me at suresh@gmail.com"}
    )

    result = response.json()["redacted"]

    assert response.status_code == 200
    assert "@gmail.com" in result
    assert "@" in result
    assert "suresh" not in result   # username should be masked


# 2. Mobile redaction (partial)
def test_mobile_redaction():
    response = client.post("/redact", json={
        "message": "Call me at 9876543210"
    })

    assert response.status_code == 200
    assert "98******10" in response.json()["redacted"]


# 3. Email + Mobile together
def test_email_and_mobile():
    response = client.post("/redact", json={
        "message": "Email test@gmail.com phone 9876543210"
    })

    result = response.json()["redacted"]

    assert "@gmail.com" in result
    assert "test" not in result
    assert "******" in result


# 4. No sensitive data
def test_no_sensitive_data():
    response = client.post("/redact", json={
        "message": "I am Suresh"
    })

    assert response.json()["redacted"] == "I am Suresh"


# 5. Empty input
def test_empty_message():
    response = client.post("/redact", json={
        "message": ""
    })

    assert response.status_code == 400
    assert response.json()["detail"] == "Message cannot be empty"


# 6. Invalid mobile (should NOT mask)
def test_invalid_mobile():
    response = client.post("/redact", json={
        "message": "Number 12345"
    })

    assert "12345" in response.json()["redacted"]


# 7. Invalid email (should NOT mask)
def test_invalid_email():
    response = client.post("/redact", json={
        "message": "asdfg@asdfg"
    })

    assert response.json()["redacted"] == "asdfg@asdfg"


# 8. Multiple mobiles
def test_multiple_mobiles():
    response = client.post("/redact", json={
        "message": "9876543210 and 9123456780"
    })

    result = response.json()["redacted"]

    assert result.count("******") >= 2

def test_mixed_input():
    response = client.post("/redact", json={
        "message": "Hello!!! suresh@gmail.com is this your number 9876543210 ???"
    })

    result = response.json()["redacted"]

    assert "@gmail.com" in result
    assert "******" in result

def test_multiple_emails():
    response = client.post("/redact", json={
        "message": "suresh@gmail.com reddy@yahoo.com"
    })

    result = response.json()["redacted"]

    assert "@gmail.com" in result
    assert "@yahoo.com" in result
    assert "suresh" not in result
    assert "reddy" not in result

def test_uppercase_email():
    response = client.post("/redact", json={
        "message": "ABC@GMAIL.COM"
    })

    result = response.json()["redacted"]

    assert "@GMAIL.COM" in result

