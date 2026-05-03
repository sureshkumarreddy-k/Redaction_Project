**Redaction API**

A FastAPI-based REST API that redacts sensitive information like emails and mobile numbers from text input.


**Overview**

This service accepts a text message and returns a redacted version by masking sensitive data.
It is designed to demonstrate API development, data masking techniques, and automated testing.


**Features**

Email masking (username hidden, domain preserved)
Example: abc@gmail.com → ***@gmail.com

Mobile number masking (partial masking)
Example: 9876543210 → 98******10

Handles invalid inputs gracefully

Automated API testing using pytest

Interactive API documentation using Swagger UI


**Running the Application**

Start the FastAPI server:
uvicorn main:app --reload

Server will run on:
http://127.0.0.1:8000

**Running the Client Script**

The client.py file can be used to send requests to the API from the command line.

1. Make sure server is running

Start the FastAPI server first: uvicorn main:app --reload

2. Run the client script

python client.py

3. Provide input

Enter the message when prompted:

Enter your message: Contact me at abc@gmail.com or call 9876543210

4. Output

The client will display the API response:

{
  "redacted": "Contact me at ***@gmail.com or call 98******10"
}



**API Documentation (Swagger UI)**

Open in browser:
http://127.0.0.1:8000/docs

You can test the API directly from this UI.

**Sample Request**

POST /redact
{
  "message": "Contact me at abc@gmail.com or call 9876543210"
}

**Sample Response**

{
  "redacted": "Contact me at ***@gmail.com or call 98******10"
}


**Running Tests**

Run all automated test cases: pytest -v

Expected output: 11 passed


**Test Coverage**

The test suite includes:
* Valid email masking
* Valid mobile number masking
* Combined scenarios (email + mobile)
* Invalid inputs (incorrect email, short numbers)
* Edge cases (empty input, special characters)
* Multiple sensitive values in a single message

