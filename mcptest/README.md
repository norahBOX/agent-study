## MCP 서버 만들기

### 환경
* Windows의 WSL(Ubuntu24.04) 환경
* uv 설치 및 uv를 통한 Python 3.12.11 설치 완료된 상태 ([문서](https://jungpark.notion.site/MCP-tutorial-27d0c02265d78029af5ff4688669563d?source=copy_link) 참조)

### 서버 및 클라이언트 실행 방법
1. mcptest 디렉토리 내에서 가상환경 구성 및 가상환경 실행
```
$ uv venv
$ uv sync
```

2. claude_desktop_config에 다음과 같이 입력
```
{
  "mcpServers": {
    "weather": {
      "command": "wsl.exe",
      "args": [
        "--cd", 
        "/home/.../mcptest", -> 이 부분엔 현재 디렉토리 절대경로를 입력한다. 
        "bash", 
        "start_server.sh"
      ]
    }
  }
}
```

3. Claude Desktop을 완전히 종료했다가 재실행

4. 채팅창에 사용 가능한 툴 `weather`가 떠 있는지 확인