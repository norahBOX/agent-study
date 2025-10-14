from google.adk.agents import Agent
from .tools import DriveAPI

drive_api = DriveAPI()

root_agent = Agent(
    name="Google_Drive_agent",
    model="gemini-2.0-flash",
    description="You are helpful assitant",
    tools=[
        drive_api.get_auth_error_message,
        drive_api.list_files,
        drive_api.download_files,
    ],
    instruction="""
    You are an AI assistant with access to user's Google Drive files. 
    Your role is to find files in Google Drive and download it in local directory. 
    If you don't have access to user's Google Drive, you can use get_auth_error_message tool to make user login Google and get Google drive access. 
    """,
)
