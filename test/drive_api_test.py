import os
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def get_credentials():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    SCOPES = [
        "https://www.googleapis.com/auth/drive.readonly",
        "https://www.googleapis.com/auth/drive.metadata.readonly",
    ]
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "adktest-desktop-credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return creds


def list_files(creds):
    """
    모든 파일 리스트(10개씩)
    """
    try:
        service = build("drive", "v3", credentials=creds)

        # Call the Drive v3 API
        results = (
            service.files()
            .list(
                pageSize=10,
                fields="nextPageToken, files(id, name, kind, mimeType, resourceKey)",
                q="trashed = false",
            )
            .execute()  # call
        )
        print(results)
        items = results.get("files", [])

        if not items:
            print("No files found.")
            return

        return [(item["name"], item["id"]) for item in items]
    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f"An error occurred: {error}")
        return


def list_files_folder(creds):
    """
    폴더만 리스트(10개씩)
    """
    try:
        service = build("drive", "v3", credentials=creds)

        # Call the Drive v3 API
        results = (
            service.files()
            .list(
                pageSize=10,
                fields="nextPageToken, files(id, name, kind, mimeType)",
                q="mimeType = 'application/vnd.google-apps.folder'",
            )
            .execute()  # call
        )
        items = results.get("files", [])

        if not items:
            print("No files found.")
            return

        return [(item["name"], item["id"]) for item in items]
    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f"An error occurred: {error}")
        return


def list_files_in_specific_folder(creds, directory_id):
    """
    특정 디렉토리 내의 파일 리스트
    """
    try:
        service = build("drive", "v3", credentials=creds)
        results = (
            service.files()
            .list(
                pageSize=10,
                fields="nextPageToken, files(id, name, kind, mimeType)",
                q=f"'{directory_id}' in parents",
            )
            .execute()  # call
        )
        items = results.get("files", [])

        if not items:
            print("No files found.")
            return

        return [(item["name"], item["id"], item["mimeType"]) for item in items]
    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f"An error occurred: {error}")
        return


def find_file_id(creds, file_name):
    """
    파일(혹은 폴더) 이름으로 파일 ID 찾기
    """
    try:
        service = build("drive", "v3", credentials=creds)
        results = (
            service.files()
            .list(
                pageSize=10,
                fields="nextPageToken, files(id, name, kind, mimeType)",
                q=f"name contains '{file_name}'",
            )
            .execute()  # call
        )
        items = results.get("files", [])

        if not items:
            print("No files found.")
            return

        return [(item["name"], item["id"], item["mimeType"]) for item in items]

    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f"An error occurred: {error}")
        return


if __name__ == "__main__":
    # desktop app credential로 테스트
    creds = get_credentials()
    if creds is None:
        get_credentials()

    # res = list_files(creds)
    # print(res)

    folder_id = ""
    res = list_files_in_specific_folder(creds, folder_id)
    print(res)
