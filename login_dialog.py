import os
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QMessageBox, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from db_helper import DB, DB_CONFIG


class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("핫도그의 민족 - 로그인")
        self.setFixedSize(350, 520)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.db = DB(**DB_CONFIG)

        self.setStyleSheet("""
            QDialog { background-color: #FFFFFF; border: 1px solid #CCCCCC; }
            QLineEdit { background-color: transparent; border: none; border-bottom: 2px solid #CCCCCC; color: black; font-size: 16px; padding-bottom: 5px; }
            QLineEdit:focus { border-bottom: 2px solid #000000; }
            QPushButton#btn_close { background-color: transparent; color: black; font-weight: bold; border: none; font-size: 16px; }
            QPushButton#btn_close:hover { color: #FF0000; }
            QPushButton#btn_login { background-color: transparent; border: 2px solid #000000; color: black; font-size: 16px; padding: 12px; border-radius: 2px; }
            QPushButton#btn_login:hover { background-color: #000000; color: white; }
            QLabel#icon_user { color: black; font-size: 20px; padding-right: 10px; }
            QLabel#icon_lock { color: black; font-size: 20px; padding-right: 10px; }
        """)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(10, 10, 10, 0)
        self.btn_close = QPushButton("X")
        self.btn_close.setObjectName("btn_close")
        self.btn_close.setCursor(Qt.PointingHandCursor)
        self.btn_close.setAutoDefault(False)
        self.btn_close.clicked.connect(self.reject)
        top_layout.addStretch()
        top_layout.addWidget(self.btn_close)
        main_layout.addLayout(top_layout)

        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(40, 20, 40, 60)
        content_layout.setSpacing(25)

        self.logo_label = QLabel()
        img_path = "hotdog.png"

        if os.path.exists(img_path):
            pixmap = QPixmap(img_path).scaled(110, 110, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.logo_label.setPixmap(pixmap)
        else:
            self.logo_label.setText("🌭")
            self.logo_label.setStyleSheet("font-size: 80px; color: black;")

        self.logo_label.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(self.logo_label)
        content_layout.addSpacing(20)

        user_layout = QHBoxLayout()
        user_layout.setSpacing(0)
        user_icon = QLabel("👤")
        user_icon.setObjectName("icon_user")
        self.username = QLineEdit()
        user_layout.addWidget(user_icon)
        user_layout.addWidget(self.username)
        content_layout.addLayout(user_layout)

        pw_layout = QHBoxLayout()
        pw_layout.setSpacing(0)
        pw_icon = QLabel("🔒")
        pw_icon.setObjectName("icon_lock")
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.password.returnPressed.connect(self.try_login)
        pw_layout.addWidget(pw_icon)
        pw_layout.addWidget(self.password)
        content_layout.addLayout(pw_layout)

        content_layout.addSpacing(15)

        self.btn_login = QPushButton("Sign In")
        self.btn_login.setObjectName("btn_login")
        self.btn_login.setCursor(Qt.PointingHandCursor)
        self.btn_login.setAutoDefault(True)
        self.btn_login.clicked.connect(self.try_login)
        content_layout.addWidget(self.btn_login)

        content_layout.addStretch()
        main_layout.addLayout(content_layout)
        self.setLayout(main_layout)

    def try_login(self):
        uid = self.username.text().strip()
        pw = self.password.text().strip()

        if not uid or not pw:
            QMessageBox.warning(self, "알림", "아이디와 비밀번호를 입력해주세요!")
            return

        if self.db.verify_user(uid, pw):
            self.accept()
        else:
            QMessageBox.critical(self, "실패", "계정 정보가 틀립니다. 다시 확인해주세요.")