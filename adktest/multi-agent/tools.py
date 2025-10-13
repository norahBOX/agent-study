import os
import json
from google.adk import Agent
from google.adk.auth.auth_credential import AuthCredential
from google.adk.auth.auth_credential import AuthCredentialTypes
from google.adk.auth.auth_credential import OAuth2Auth
from google.adk.tools.application_integration_tool.application_integration_toolset import (
    ApplicationIntegrationToolset,
)
from google.adk.tools import FunctionTool  # Tool을 만들 때 필요함
from google.adk.tools.openapi_tool.auth.auth_helpers import dict_to_auth_scheme
from google.genai import types

GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

with open(
    "service_account_credential_here.json", "r"
) as f:  # connector의 서비스 어카운트
    service_account_json = json.load(f)

oauth2_data_google_cloud = {
    "type": "oauth2",
    "flows": {
        "authorizationCode": {
            "authorizationUrl": "https://accounts.google.com/o/oauth2/auth",
            "tokenUrl": "https://oauth2.googleapis.com/token",
            "scopes": {
                "https://www.googleapis.com/auth/drive.metadata.readonly": (
                    "google drive metadata read"
                ),
            },
        }
    },
}
oauth2_scheme = dict_to_auth_scheme(oauth2_data_google_cloud)

auth_credential = AuthCredential(
    auth_type=AuthCredentialTypes.OAUTH2,
    oauth2=OAuth2Auth(
        client_id=client_id,
        client_secret=client_secret,
    ),
)

connector_tool = ApplicationIntegrationToolset(
    project=GOOGLE_CLOUD_PROJECT,
    location="us-central1",
    connection="adk-test",
    entity_operations={},
    actions=["GET_files"],
    tool_instructions="Use this tool to list google drive files.",
    service_account_json=json.dumps(service_account_json),
    auth_scheme=oauth2_scheme,
    auth_credential=auth_credential,
)
