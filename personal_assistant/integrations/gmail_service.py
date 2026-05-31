import base64
from email.utils import parsedate_to_datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
]


def get_gmail_service():
    creds = None

    if __import__("os").path.exists("gmail_token.json"):
        creds = Credentials.from_authorized_user_file("gmail_token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json",
                SCOPES,
            )
            creds = flow.run_local_server(port=0)

        with open("gmail_token.json", "w") as token:
            token.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)


def get_recent_emails(max_results: int = 5) -> dict:
    service = get_gmail_service()

    result = (
        service.users()
        .messages()
        .list(userId="me", maxResults=max_results, labelIds=["INBOX"])
        .execute()
    )

    messages = result.get("messages", [])
    emails = []

    for message in messages:
        msg = (
            service.users()
            .messages()
            .get(userId="me", id=message["id"], format="metadata")
            .execute()
        )

        headers = msg.get("payload", {}).get("headers", [])

        def get_header(name: str) -> str:
            for header in headers:
                if header.get("name", "").lower() == name.lower():
                    return header.get("value", "")
            return ""

        emails.append(
            {
                "id": msg.get("id"),
                "from": get_header("From"),
                "subject": get_header("Subject"),
                "date": get_header("Date"),
                "snippet": msg.get("snippet", ""),
            }
        )

    return {
        "status": "success",
        "count": len(emails),
        "emails": emails,
    }