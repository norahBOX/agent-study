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
DOWNLOAD_PATH = Path(__file__).resolve().parent / "data"
FLASK_AUTH_URL = "http://localhost:8000/authorize"
SCOPES = [
    "https://www.googleapis.com/auth/drive.readonly",
    "https://www.googleapis.com/auth/drive.metadata.readonly",
]


class DriveAPI:
    def __init__(self):
        self.credentials = None

    def get_credentials(self):
        """
        Google 로그인이 완료된 인증 정보 token.json 파일을 찾아 credentials을 생성한다.
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
        return

    def check_auth_status(self):
        """
        Google 로그인 인증 상태를 확인하고, 로그인이 되어 있지 않으면 사용자에게 로그인 할 수 있는 링크를 제공한다.
        """
        self.get_credentials()
        if self.credentials is None:
            return (
                f"ERROR: Google Drive 접근 권한이 필요합니다. "
                f"로그인 후 작업을 다시 시도해 주세요. [로그인 url]({FLASK_AUTH_URL})"
            )
        return None

    def get_files_and_folders_list(self):
        """
        Get files and folders list in Google Drive.

        Returns:
            list: A list containing (id, name, mimeType)
        """
        auth_error = self.check_auth_status()
        if auth_error:
            return auth_error

        try:
            service = build("drive", "v3", credentials=self.credentials)

            # Call the Drive v3 API
            results = (
                service.files()
                .list(
                    pageSize=10,
                    fields="nextPageToken, files(id, name, kind, mimeType)",
                )
                .execute()
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

    def download_files(self, file_name: str, file_id: str):
        """
        Download a file from Google Drive and save it local directory.

        Args:
            file_name (str): A file or folder name to download from Google Drive. Save the file at local directory with the same file name.
            file_id (str): File id of a file in Google Drive.
        Returns:
            str: success or fail(error) result message
        """
        auth_error = self.check_auth_status()
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
            return "file download complete."

        except HttpError as error:
            # print(f"An error occurred: {error}")
            return f"An error occurred while file download: {error}"

    def list_files_in_specific_folder(self, folder_id: str):
        """
        특정 폴더 내의 파일 리스트를 반환한다.
        Args:
            folder_id: 특정 폴더의 ID
        Returns:
            list: A list containing (id, name, mimeType)
        """
        auth_error = self.check_auth_status()
        if auth_error:
            return auth_error

        try:
            service = build("drive", "v3", credentials=self.credentials)
            results = (
                service.files()
                .list(
                    pageSize=10,
                    fields="nextPageToken, files(id, name, kind, mimeType)",
                    q=f"{folder_id} in parents",
                )
                .execute()
            )
            items = results.get("files", [])

            if not items:
                print("No files found.")
                return

            return [(item["name"], item["id"], item["mimeType"]) for item in items]
        except HttpError as error:
            print(f"An error occurred: {error}")
            return

    def find_file_id(self, file_name: str):
        """
        Retrieve file or folders which name contains specific strings.
        Args:
            file_name: specific strings to find files or folders

        Returns:
            list: A list containing (id, name, mimeType)
        """
        try:
            service = build("drive", "v3", credentials=self.credentials)
            results = (
                service.files()
                .list(
                    pageSize=10,
                    fields="nextPageToken, files(id, name, kind, mimeType)",
                    q=f"name contains '{file_name}'",
                )
                .execute()
            )
            items = results.get("files", [])

            if not items:
                print("No files found.")
                return

            return [(item["name"], item["id"], item["mimeType"]) for item in items]

        except HttpError as error:
            print(f"An error occurred: {error}")
            return
