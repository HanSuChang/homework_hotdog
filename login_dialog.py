from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QMessageBox
from db_helper import DB, DB_CONFIG


class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("핫도그의 민족 - 로그인")

        # db_helper에서 설정값 가져와서 DB 연결
        self.db = DB(**DB_CONFIG)

        self.username = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)

        # 'form' 레이아웃 설정
        form = QFormLayout()
        form.addRow("아이디", self.username)
        form.addRow("비밀번호", self.password)

        self.btn_login = QPushButton("핫도그 먹으러 가기")
        self.btn_login.clicked.connect(self.try_login)

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addWidget(self.btn_login)
        self.setLayout(layout)

    def try_login(self):
        uid = self.username.text().strip()
        pw = self.password.text().strip()

        if not uid or not pw:
            QMessageBox.warning(self, "알림", "아이디와 비밀번호를 입력해주세요!")
            return

        # DB에서 회원 확인
        if self.db.verify_user(uid, pw):
            self.accept()  # 성공 시 창 닫기
        else:
            QMessageBox.critical(self, "실패", "계정 정보가 틀립니다. 다시 확인해주세요.")