import os
from pathlib import Path
import flask
import json
import requests
from dotenv import load_dotenv
import google.oauth2.credentials
import google_auth_oauthlib.flow

load_dotenv()

CLIENT_SECRETS_FILENAME = os.getenv("CLIENT_SECRETS_FILENAME")
TOKEN_FILE_PATH = Path(__file__).resolve().parent / "temp_token_repo"
TOKEN_FILE_PATH.mkdir(exist_ok=True)

SCOPES = [
    "https://www.googleapis.com/auth/drive.readonly",
]
API_SERVICE_NAME = "drive"
API_VERSION = "v3"

# When running locally, disable OAuthlib's HTTPs verification.
# ACTION ITEM for developers:
#     When running in production *do not* leave this option enabled.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# This disables the requested scopes and granted scopes check.
# If users only grant partial request, the warning would not be thrown.
os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = "1"

app = flask.Flask(__name__)
# Note: A secret key is included in the sample so that it works.
# If you use this code in your application, replace this with a truly secret
# key. See https://flask.palletsprojects.com/quickstart/#sessions.
app.secret_key = os.getenv("FLASK_SESSION_SECRET")


@app.route("/")
def index():
    return "welcome"


@app.route("/login_success")
def login_success():
    return "Google Login이 완료되었습니다. 이 창을 닫고 기존 앱으로 돌아가세요."


@app.route("/authorize")
def authorize():
    # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILENAME, scopes=SCOPES
    )
    flow.redirect_uri = flask.url_for(
        "oauth2callback", _external=True
    )  # 사용자 로그인이 끝나면 리다이렉트(callback)할 곳

    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type="offline",
        prompt="consent",
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes="true",
    )
    # Store the state so the callback can verify the auth server response.
    flask.session["state"] = state

    return flask.redirect(
        authorization_url
    )  # 사용자 브라우저가 구글 로그인 창으로 이동


@app.route("/oauth2callback")
def oauth2callback():
    state = flask.session["state"]
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILENAME, scopes=SCOPES, state=state
    )
    flow.redirect_uri = flask.url_for("oauth2callback", _external=True)

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = flask.request.url
    flow.fetch_token(authorization_response=authorization_response)

    # local에 파일로 토큰 저장
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    credentials = flow.credentials
    token_data_json = credentials.to_json()
    with open(f"{TOKEN_FILE_PATH}/token.json", "w") as token_file:
        token_file.write(token_data_json)

    return flask.redirect("/login_success")


if __name__ == "__main__":
    app.run("localhost", 8000, debug=True)
