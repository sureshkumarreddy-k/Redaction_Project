**Redaction Project**

A FastAPI-based web application that detects and redacts sensitive information such as email addresses and mobile numbers.

The application stores redacted messages in a SQLite database and provides a simple web UI to manage messages.

UI automation testing is implemented using Playwright and Pytest.

**Features**

Email masking (username hidden, domain preserved)
Example: abc@gmail.com → ***@gmail.com

Mobile number masking (partial masking)
Example: 9876543210 → 98******10

- SQLite database integration
- FastAPI backend
- HTML + CSS frontend
- Jinja2 templating
- Store messages in database
- Delete messages from UI
- REST API endpoints
- Playwright UI automation
- Data-driven testing using Excel

**Project Structure**
```text
RedactionProject/
│
├── main.py
├── database.py
├── models.py
├── client.py
├── messages.db
├── requirements.txt
├── README.md
│
├── templates/
│   └── index.html
│
├── static/
│   └── style.css
│
├── tests_ui/
│   └── test_ui.py
│
└── testdata.xlsx

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


**API Endpoints**

* Get Home Page: GET /
  Displays stored redacted messages.

* Submit Message: POST /submit
  Stores redacted message in database.

* Get Messages: GET /messages
  Returns all stored messages.

* Delete Message: POST /delete/{message_id}
  Deletes message from database.

**Running Tests**

Run all automated test cases: pytest tests_ui/test_ui.py -v

**Test Coverage**

The test suite includes:

* UI page load validation
* Email redaction validation
* Mobile redaction validation
* Multiple email validation
* Multiple mobile validation
* Email + mobile combination validation
* Delete message validation
* Data-driven testing using Excel
