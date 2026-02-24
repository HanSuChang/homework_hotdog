import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from login_dialog import LoginDialog
from main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)  # 창이 0개여도 앱 안 꺼지게

    try:
        login = LoginDialog()
    except Exception as e:
        QMessageBox.critical(None, "DB 오류", f"데이터베이스 연결 실패:\n{e}\n\nDB가 켜져 있는지 확인해주세요.")
        sys.exit(1)

    result = login.exec_()

    if result == LoginDialog.Accepted:
        try:
            window = MainWindow()
            window.show()
            app.setQuitOnLastWindowClosed(True)  # 메인창 뜬 후 복원
            sys.exit(app.exec_())
        except Exception as e:
            QMessageBox.critical(None, "오류", f"메인 창 실행 오류:\n{e}")
            sys.exit(1)
    else:
        sys.exit(0)