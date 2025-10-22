import os
import asyncio
import sqlite3
from google.adk import Agent
from google.adk.runners import Runner
from google.adk.sessions import Session, DatabaseSessionService
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
google_cloud_project = os.getenv("GOOGLE_CLOUD_PROJECT")
google_cloud_location = os.getenv("GOOGLE_CLOUD_LOCATION")
google_genai_use_vertexai = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "1")
model_name = os.getenv("MODEL")

DB_PATH = "../adktest/session.db"


def test_connection():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    # res = cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    res = cur.execute("SELECT * FROM sessions")
    print(res.fetchall())


async def test_dbsession_state():
    app_name = "multi-agent"
    user_id_1 = "user"
    session_id = "SESSION ID HERE"
    db_url = f"sqlite:///{DB_PATH}"

    db_session_service = DatabaseSessionService(db_url=db_url)

    root_agent = Agent(
        model="gemini-2.0-flash",
        name="Google_Drive_agent",
        instruction="Answer questions.",
    )

    runner = Runner(
        agent=root_agent,
        app_name=app_name,
        session_service=db_session_service,
    )

    ## 1. db session service로 할 수 있는 것들

    # 기존 세션 리스트업
    # existing_sessions = await db_session_service.list_sessions(
    #     app_name=app_name, user_id=user_id_1
    # )
    # print(existing_sessions)

    # 새로운 세션 만들기
    # new_session = await db_session_service.create_session(
    #     app_name=app_name, user_id=user_id_1, session_id="newsession2025", state={}
    # )
    # print(new_session)

    # id로 특정 세션 찾기
    specific_session = await db_session_service.get_session(
        app_name=app_name, user_id=user_id_1, session_id=session_id
    )
    print(specific_session)

    ## 2. 세션 서비스를 runner에 붙이기
    async def run_prompt(session: Session, new_message: str):
        content = types.Content(
            role="user", parts=[types.Part.from_text(text=new_message)]
        )
        print("** User says:", content.model_dump(exclude_none=True))

        async for event in runner.run_async(
            user_id=user_id_1,
            session_id=session.id,
            new_message=content,
        ):
            if event.content.parts and event.content.parts[0].text:
                print(f"** {event.author}: {event.content.parts[0].text}")

    query = "What is the capital of Korea?"
    await run_prompt(session=specific_session, new_message=query)


if __name__ == "__main__":
    asyncio.run(test_dbsession_state())
