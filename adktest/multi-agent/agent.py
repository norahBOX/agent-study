import datetime
from google.adk.agents import Agent
from .tools import connector_tool

root_agent = Agent(
    name="driveagent",
    model="gemini-2.0-flash",
    description="You are helpful assitant",
    tools=[connector_tool],
    instruction="Use connector_tool to list up files in Google Drive.",
)
