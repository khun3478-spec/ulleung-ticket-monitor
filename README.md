# 울릉도 티켓 모니터 V2

GitHub Actions에서 10분마다 실행되는 한국해운조합(KSA) 울릉도 여객선 예약 모니터입니다.

예약은 수행하지 않으며 조회만 수행합니다.

예약 가능 상태(`ispossible == "1"`)가 되면 Telegram으로 알림을 전송합니다.

---

# 프로젝트 구조

```
.
├── .github
│   └── workflows
│       └── monitor.yml
├── config.py
├── ksa.py
├── telegram_bot.py
├── state.py
├── monitor.py
├── requirements.txt
└── README.md
```

---

# Python

Python 3.12

---

# 설치

```
pip install -r requirements.txt
```

---

# GitHub Secrets

Repository

Settings

↓

Secrets and variables

↓

Actions

다음 두 개를 등록합니다.

```
TELEGRAM_BOT_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxx

TELEGRAM_CHAT_ID=8622503258
```

---

# 로컬 실행

```
python monitor.py
```

---

# GitHub Actions

Workflow는

- 수동 실행
- 10분마다 자동 실행

두 가지 모두 지원합니다.

---

# Telegram 알림

예약 가능 시 아래와 같이 전송됩니다.

```
🚢 울릉도 예약 가능!

노선 : 묵호 → 울릉도 도동

출발일 : 2026-08-14

출발시간 : 12:40

선박 : 씨스타 1

예약 가능 : 1석

예약페이지
https://island.theksa.co.kr/page/booking
```

---

# 로그 예시

```
===== 울릉도 티켓 모니터 시작 =====

조회 : 묵호 → 울릉도 도동

예약 불가

조회 : 울릉도 도동 → 묵호

예약 가능

Telegram 발송 완료

===== 종료 =====
```

---

# License

Private Project
