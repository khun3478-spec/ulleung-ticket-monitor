울릉도 티켓 모니터 V1

개요

GitHub Actions에서 10분마다 실행되는 한국해운조합(KSA) 울릉도 여객선 예약 모니터입니다.

예약 가능 상태("ispossible == "1"")가 되면 Telegram으로 알림을 전송합니다.

예약은 수행하지 않으며 조회만 합니다.

---

감시 대상

1.

- 노선 : 묵호 → 울릉도 도동
- 출발일 : 2026-08-14
- 출발시간 : 12:00
- 선박 : 씨스타

2.

- 노선 : 울릉도 도동 → 묵호
- 출발일 : 2026-08-17
- 선박 : 씨스타

---

프로젝트 구조

.
├── .github
│   └── workflows
│       └── monitor.yml
├── config.py
├── ksa.py
├── monitor.py
├── requirements.txt
├── state.py
├── telegram_bot.py
└── README.md

---

GitHub Secrets

다음 Secrets를 등록합니다.

이름| 설명
TELEGRAM_BOT_TOKEN| Telegram Bot Token
TELEGRAM_CHAT_ID| Telegram Chat ID

예)

TELEGRAM_CHAT_ID=8622503258

---

실행

로컬

pip install -r requirements.txt
python monitor.py

GitHub Actions

- Actions 탭 활성화
- Workflow 실행
- 이후 10분마다 자동 실행

---

Telegram 알림

예약 가능 상태가 되면 아래 형식으로 전송됩니다.

🚢 울릉도 예약 가능!

노선

출발일

출발시간

선박

예약 가능

https://island.theksa.co.kr/page/booking

---

Python

- Python 3.12

---

License

Private Project
