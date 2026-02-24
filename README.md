핫도그의 민족 (Hotdog Nation) 🌭
PyQt5와 MySQL로 만든 핫도그 메뉴 관리 및 주문 시스템입니다.

시작하기 전에
필요한 패키지 설치

pip install PyQt5 pymysql

데이터베이스 설정
로컬에 MySQL이 설치되어 있어야 합니다. 기본 설정값은 아래와 같으며, 변경이 필요하면
db_helper.py의 DB_CONFIG를 수정하세요.

항목                  값
HOST               localhost
User                 root
Password         (본인 설정값)
Database          sampledb


 
필요한 테이블
실행 전에 아래 두 테이블이 DB에 있어야 합니다.

users — 로그인용 (컬럼: username, password)
hotdogs — 메뉴용 (컬럼: id, menu_name, price, stock, category, kcal)


실행 방법
python app.py
```

---

## 주요 기능

- **관리자 로그인** — DB에 등록된 계정으로 로그인
- **메뉴 및 재고 관리** — 테이블 형태로 메뉴 조회, 추가, 수정, 삭제(CRUD)
- **장바구니** — 메뉴를 선택해 담고 수량 조절(+/-)
- **주문 및 결제** — 배송지 입력과 결제 수단 선택, 결제 완료 시 재고 자동 차감

---

## 파일 구성
```
├── app.py            # 진입점. 로그인 창 실행 후 메인 창 연결
├── db_helper.py      # DB 연결 및 쿼리 처리 (조회/추가/수정/삭제)
├── login_dialog.py   # 커스텀 디자인 로그인 다이얼로그 (타이틀바 없음)
└── main_window.py    # 메인 화면, 장바구니, 결제 다이얼로그 UI
