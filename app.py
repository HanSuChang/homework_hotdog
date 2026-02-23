import sys
from PyQt5.QtWidgets import QApplication
from login_dialog import LoginDialog
from main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 1. 로그인 창 띄우기
    login = LoginDialog()

    # 로그인 성공 시에만 메인 화면 실행
    if login.exec_() == LoginDialog.Accepted:
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    else:
        # 로그인 취소 시 프로그램 종료
        sys.exit(0)