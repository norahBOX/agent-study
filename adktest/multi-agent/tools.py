import io
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload


# If modifying these scopes, delete the file token.json.
TOKEN_PATH = (
    Path(__file__).resolve().parent.parent.parent / "oauth2_flask" / "temp_token_repo"
)
print(TOKEN_PATH)
DOWNLOAD_PATH = Path(__file__).resolve().parent / "data"
FLASK_AUTH_URL = "http://localhost:8000/authorize"
SCOPES = [
    "https://www.googleapis.com/auth/drive.readonly",
]


class DriveAPI:
    def __init__(self):
        self.credentials = None

    def get_credentials(self):
        """
        Google 로그인이 완료 된 인증 정보 token 파일을 찾아 credentials 을 생성한다.
        """
        creds = None

        if (TOKEN_PATH / "token.json").exists():
            creds = Credentials.from_authorized_user_file(
                (TOKEN_PATH / "token.json"), SCOPES
            )

            # token이 있지만 못쓰는 상황이면 refresh
            if creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    print(f"Error refreshing token: {e}")
                    creds = None

        self.credentials = creds
        return self.credentials

    def get_auth_error_message(self):
        """
        Google 로그인 인증 상태를 확인하고, 유효하지 않으면 오류 메시지를 반환한다.
        """
        self.get_credentials()
        if self.credentials is None:
            return (
                f"ERROR: Google Drive 접근 권한이 필요합니다. "
                f"로그인 후 작업을 다시 시도해 주세요. [인증하기]({FLASK_AUTH_URL})"
            )
        return None

    def list_files(self):
        """
        Get files list in Google Drive.

        Args:
            credentials: Credentials from get_credentials() function.
        """
        auth_error = self.get_auth_error_message()
        if auth_error:
            return auth_error

        try:
            service = build("drive", "v3", credentials=self.credentials)

            # Call the Drive v3 API
            results = (
                service.files()
                .list(
                    pageSize=10,
                    fields="nextPageToken, files(kind, id, name)",
                    # q="mimeType = 'application/vnd.google-apps.folder'",
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

    def download_files(self, file_name: str, file_id: str):
        """
        Download a file from Google Drive and save it local directory.

        Args:
            file_name (str): A file name to download from Google Drive. Save the file at local directory with the same file name.
            file_id (str): File id of a file in Google Drive.
        """
        auth_error = self.get_auth_error_message()
        if auth_error:
            return auth_error

        try:
            service = build("drive", "v3", credentials=self.credentials)

            # Call the Drive v3 API
            request = service.files().get_media(fileId=file_id)
            file = io.BytesIO()
            downloader = MediaIoBaseDownload(file, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print(f"Download {int(status.progress() * 100)}.")

            downloaded = file.getvalue()
            with open(f"{DOWNLOAD_PATH}/{file_name}", "wb") as f:
                f.write(downloaded)
            return

        except HttpError as error:
            print(f"An error occurred: {error}")
            return
