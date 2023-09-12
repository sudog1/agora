# 5조의 팀 프로젝트 Agora Feed

## 리포지토리 clone후 해야할 것
#### 1. 가상환경 생성
#### 2. requirements.txt 안의 패키지 설치(pip install -r requirements를 사용하세요.)
#### 3. branch 생성
#### 4. 데이터베이스 생성을 위해 migrate 명령을 실행(makemigrations는 하지 마세요!)

## ✨ 변경사항
#### - 🎨 code_app이 명확하지 않아서 code_feed로 이름을 변경했습니다.
#### - user_app을 accounts로 변경했습니다.
#### - 🆕 code_feed의 models.py에 likes, bookmarks, solved 관계를 추가했습니다. 주석을 읽어주세요.
#### - 문제 데이터를 추가했습니다. `python manage.py shell < problem_list.csv` 명령을 실행해주세요.

## ⚠️ 주의사항
### - 🚫 models.py 수정 및 makemigrations 명령을 하지 마세요. 그렇지 않으면 충돌이 일어날 수 있습니다.
### - 항상 작업하기 전, 가상환경에 진입해 주세요.
### - 🚫 반드시 commit, push 하기 전에는 현재 branch를 확인해 주세요.