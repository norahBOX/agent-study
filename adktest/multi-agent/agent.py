from google.adk.agents import Agent
from .tools import DriveAPI

drive_api = DriveAPI()

root_agent = Agent(
    name="Google_Drive_agent",
    model="gemini-2.0-flash",
    description="You are helpful assitant",
    tools=[
        drive_api.check_auth_status,
        drive_api.get_files_and_folders_list,
        drive_api.download_files,
        drive_api.list_files_in_specific_folder,
        drive_api.find_file_id,
    ],
    instruction="""
    You are an AI assistant with access to user's Google Drive files. 
    Your role is to find files and folders in Google Drive and download it in local directory. 

    1) If you don't have access to user's Google Drive, you can use get_auth_error_message tool to make user login Google and get Google drive access.
    2) You can user find_file_id to find file id which is needed to search and download files.
    3) You can find specific folder's file list with list_files_in_specific_folder tool. 
    """,
)
