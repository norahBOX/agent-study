<Google OAuth2 로그인을 위하여 로컬 환경에 띄우는 간이 서버>

실행 방법
1) oauth2_flask 디렉토리로 이동 
```
cd oauth2_flask 
```
2) 환경변수 설정을 위한 .env 파일 생성, 아래 내용 작성
```
CLIENT_SECRETS_FILENAME=~~~~.json
FLASK_SESSION_SECRET=~~~
```
* CLIENT_SECRETS_FILENAME: oauth2 인증을 위한 웹 클라이언트 secret json 파일 
* FLASK_SESSION_SECRET: flask session 암호화를 위한 (아무)텍스트. [Flask Session secret](https://flask.palletsprojects.com/en/stable/quickstart/#sessions) 참조

3) Python 의존성 패키지 설치 및 가상환경 실행
```
$ uv sync
$ uv venv
$ source .venv/bin/activate
```
4) flask 실행으로 서버 켜기 
```
$ flask run --port 8000 --debug
```
