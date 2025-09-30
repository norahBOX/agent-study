#!/bin/bash

# 가상환경 실행
source .venv/bin/activate

# uv를 절대 경로로 실행
UV_PATH="$HOME/.local/bin/uv"
"$UV_PATH" run weather.py

# 서버 실행 후 가상환경 종료
deactivate