# LEC 13 / Drill 11: IDLE / SLEEP / RUN / AutoRun

`transitions.Machine`으로 구현한 소년 상태 머신 실습입니다.

## 실행

이 폴더에서 PowerShell 터미널을 열어 실행합니다.

```powershell
python -m pip install -r requirements.txt
python main.py
```

VS Code에서는 `main.py`를 실행합니다. 실행하는 Python 환경에 `pico2d`와
`transitions`가 설치되어 있어야 합니다.

## 조작

- IDLE에서 5초가 지나면 SLEEP으로 전환합니다.
- SLEEP에서 Space를 누르면 IDLE로 돌아가고 5초 타이머가 다시 시작됩니다.
- IDLE 또는 SLEEP에서 왼쪽/오른쪽 방향키를 누르면 RUN으로 전환합니다.
- 방향키를 놓으면 IDLE로 돌아갑니다. 두 방향키를 함께 누른 경우에는
  가장 최근에 누른 방향으로 달리고, 한쪽을 놓으면 남은 방향으로 달립니다.
- 소년은 화면 밖으로 나가지 않습니다.
- IDLE에서 A키를 누르면 별도의 `AutoRun` 상태 클래스로 전환합니다.
  키 입력 없이 자동 이동하며, 속도는 RUN의 2배(400 px/s), 크기는
  1.5배(150×150)입니다. 화면 양 끝에서 자동으로 방향을 바꿉니다.
- AutoRun 시작 후 5초가 지나면 원래 크기의 IDLE로 돌아옵니다.
- AutoRun 중 왼쪽/오른쪽 방향키를 누르면 자동 이동을 취소하고,
  누른 방향으로 원래 속도와 크기의 RUN 상태가 됩니다.
- A키를 계속 누르고 있어도 AutoRun 시간이 연장되거나 반복 시작되지 않습니다.
- Escape 또는 창 닫기로 종료합니다.

## 파일

- `boy.py`: 상태 머신, 애니메이션, 키 입력, 이동과 화면 경계 처리
- `auto_run.py`: 별도의 AutoRun 상태 클래스와 자동 이동·반사·크기·타이머 처리
- `grass.py`: 잔디 객체
- `main.py`: 게임 루프와 이벤트 전달
- `animation_sheet.png`, `grass.png`: 실행에 필요한 이미지
- `requirements.txt`: Python 의존성
- `idle_state.md`: 최종 상태 다이어그램
- `state_diagram.png`: 저장소에 포함하는 상태 다이어그램 이미지
- `tests/test_autorun.py`: AutoRun과 기존 상태 동작 검증
- `commit_history.md`: 이번 작업의 로컬 커밋 30개 목록

## 테스트

```powershell
python -m unittest discover -s tests -v
```

원본 저장소는 `C:\Users\tedu0\2DGP-2023180016`에 있습니다.
이 폴더에는 실행용 파일과 커밋 목록을 복사했습니다.
