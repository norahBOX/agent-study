## ADK 서버 만들기

### 환경
* Windows의 WSL(Ubuntu24.04) 환경
* uv 설치 및 uv를 통한 Python 3.12.11 설치 완료된 상태 ([문서](https://www.notion.so/jungpark/MCP-tutorial-27d0c02265d78029af5ff4688669563d?source=copy_link#27a0c02265d7805ea118c5f0a5f4d2d4) 참조)

### 서버 및 클라이언트 실행 방법
1. adktest 디렉토리 내에서 가상환경 구성 및 가상환경 실행
```
$ uv venv
$ uv sync
```

2. adktest 디렉토리에서 다음과 같이 서버 실행
```
$ adk web --reload_agents
```

3. localhost:8000으로 접속하여 챗봇 웹 화면 확인

4. 웹 화면 좌측에서 'multi-agent' 선택 후 채팅으로 google drive 내 파일 관련 질의