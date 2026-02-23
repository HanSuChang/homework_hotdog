from PyQt5.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QWidget, QLabel, \
    QPushButton, QMessageBox, QAbstractItemView, QLineEdit, QDialog, QRadioButton, QButtonGroup
from db_helper import DB, DB_CONFIG


# 🟢 [신규] 배달앱 스타일 결제창 클래스
class PaymentDialog(QDialog):
    def __init__(self, total_price, parent=None):
        super().__init__(parent)
        self.setWindowTitle("핫도그의 민족 - 결제하기")
        self.setFixedSize(350, 480)

        # 결제창도 브라운 톤으로 통일
        self.setStyleSheet("""
            QDialog { background-color: #F4EAE0; }
            QLabel { color: #3E2723; font-weight: bold; }
            QLineEdit { border: 1px solid #BCAAA4; padding: 10px; background-color: #FFFFFF; border-radius: 5px; }
            QRadioButton { font-size: 14px; margin: 6px; color: #3E2723; }
            QPushButton { background-color: #D84315; color: white; font-weight: bold; border-radius: 5px; padding: 12px; font-size: 16px; }
            QPushButton:hover { background-color: #BF360C; }
        """)

        layout = QVBoxLayout()

        # 1. 배달 주소 입력칸
        layout.addWidget(QLabel("📍 배달 받으실 주소"))
        self.input_address = QLineEdit()
        self.input_address.setPlaceholderText("예: 대전광역시 유성구 핫도그동 123")
        layout.addWidget(self.input_address)

        layout.addSpacing(15)

        # 2. 총 결제 금액
        self.total_label = QLabel(f"💰 총 결제 금액: {total_price}원")
        self.total_label.setStyleSheet("font-size: 18px; color: #D84315; margin-bottom: 10px;")
        layout.addWidget(self.total_label)

        # 3. 결제 수단 라디오 버튼 (보내주신 사진 참고)
        layout.addWidget(QLabel("💳 결제수단 선택"))
        self.pay_group = QButtonGroup(self)
        methods = ["신용/체크카드", "토스페이", "카카오페이", "계좌 결제", "네이버페이", "휴대폰 결제","만나서 결제"]

        for i, m in enumerate(methods):
            rb = QRadioButton(m)
            if i == 0: rb.setChecked(True)  # 기본으로 첫 번째 선택
            self.pay_group.addButton(rb)
            layout.addWidget(rb)

        layout.addSpacing(20)

        # 4. 최종 결제 버튼
        self.btn_pay = QPushButton(f"{total_price}원 결제하기")
        self.btn_pay.clicked.connect(self.process_payment)
        layout.addWidget(self.btn_pay)

        self.setLayout(layout)

    def process_payment(self):
        # 주소가 비어있는지 검사
        if not self.input_address.text().strip():
            QMessageBox.warning(self, "알림", "배달 받으실 주소를 정확히 입력해주세요!")
            return

        # 문제 없으면 결제창 닫고 성공 신호 보내기
        self.accept()


# =======================================================
# 아래는 기존 메인 화면 코드입니다. (checkout 함수만 변경됨)
# =======================================================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("핫도그의 민족 - 관리 시스템")
        self.setGeometry(100, 100, 1050, 600)
        self.db = DB(**DB_CONFIG)

        self.setStyleSheet("""
            QMainWindow { background-color: #F4EAE0; }
            QLabel { color: #3E2723; }
            QTableWidget { background-color: #FFFFFF; border: 1px solid #BCAAA4; gridline-color: #D7CCC8; }
            QHeaderView::section { background-color: #8D6E63; color: white; font-weight: bold; padding: 4px; border: 1px solid #795548; }
            QPushButton { background-color: #FFB300; color: #3E2723; font-weight: bold; border-radius: 4px; padding: 8px; }
            QPushButton:hover { background-color: #FFA000; }
            QLineEdit { border: 1px solid #BCAAA4; padding: 5px; background-color: #FFFFFF; }
        """)

        main_layout = QHBoxLayout()

        left_layout = QVBoxLayout()
        self.label = QLabel("🌭 명량핫도그 재고/메뉴 관리")
        self.label.setStyleSheet("font-size: 20px; font-weight: bold; margin: 10px; background: transparent;")

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["번호", "메뉴명", "가격", "재고", "카테고리", "칼로리(kcal)"])
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.itemSelectionChanged.connect(self.fill_inputs_from_selection)

        self.btn_add_cart = QPushButton("장바구니에 담기 ➡️")
        self.btn_add_cart.setMinimumHeight(40)
        self.btn_add_cart.clicked.connect(self.add_to_cart)

        self.add_label = QLabel("📝 데이터 추가/수정/삭제 (표에서 메뉴를 클릭해보세요!)")
        self.add_label.setStyleSheet("font-weight: bold; margin-top: 15px; background: transparent;")

        input_layout = QHBoxLayout()
        self.input_name = QLineEdit()
        self.input_name.setPlaceholderText("메뉴명")
        self.input_price = QLineEdit()
        self.input_price.setPlaceholderText("가격")
        self.input_stock = QLineEdit()
        self.input_stock.setPlaceholderText("재고 (기본 10)")
        self.input_category = QLineEdit()
        self.input_category.setPlaceholderText("카테고리")
        self.input_kcal = QLineEdit()
        self.input_kcal.setPlaceholderText("칼로리")

        input_layout.addWidget(self.input_name)
        input_layout.addWidget(self.input_price)
        input_layout.addWidget(self.input_stock)
        input_layout.addWidget(self.input_category)
        input_layout.addWidget(self.input_kcal)

        btn_layout = QHBoxLayout()
        self.btn_insert = QPushButton("➕ 새 메뉴 추가")
        self.btn_update = QPushButton("✏️ 선택 메뉴 수정")
        self.btn_delete = QPushButton("🗑️ 선택 메뉴 삭제")

        self.btn_insert.clicked.connect(self.insert_new_menu)
        self.btn_update.clicked.connect(self.update_menu)
        self.btn_delete.clicked.connect(self.delete_menu)

        btn_layout.addWidget(self.btn_insert)
        btn_layout.addWidget(self.btn_update)
        btn_layout.addWidget(self.btn_delete)

        left_layout.addWidget(self.label)
        left_layout.addWidget(self.table)
        left_layout.addWidget(self.btn_add_cart)
        left_layout.addWidget(self.add_label)
        left_layout.addLayout(input_layout)
        left_layout.addLayout(btn_layout)

        right_layout = QVBoxLayout()
        self.cart_label = QLabel("🛒 장바구니")
        self.cart_label.setStyleSheet("font-size: 20px; font-weight: bold; margin: 10px; background: transparent;")

        self.cart_table = QTableWidget()
        self.cart_table.setColumnCount(5)
        self.cart_table.setHorizontalHeaderLabels(["메뉴명", "가격", "-", "수량", "+"])
        self.cart_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.cart_table.setColumnWidth(0, 130)
        self.cart_table.setColumnWidth(1, 70)
        self.cart_table.setColumnWidth(2, 30)
        self.cart_table.setColumnWidth(3, 40)
        self.cart_table.setColumnWidth(4, 30)

        self.total_label = QLabel("총 결제 금액: 0원")
        self.total_label.setStyleSheet(
            "font-size: 18px; font-weight: bold; color: #D84315; margin: 10px; background: transparent;")

        self.btn_checkout = QPushButton("💳 결제하기")
        self.btn_checkout.setMinimumHeight(40)
        self.btn_checkout.clicked.connect(self.checkout)

        right_layout.addWidget(self.cart_label)
        right_layout.addWidget(self.cart_table)
        right_layout.addWidget(self.total_label)
        right_layout.addWidget(self.btn_checkout)

        main_layout.addLayout(left_layout, 6)
        main_layout.addLayout(right_layout, 4)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.cart_items = {}
        self.load_data()

    def load_data(self):
        data = self.db.fetch_hotdogs()
        self.table.setRowCount(len(data))
        for row_idx, row_data in enumerate(data):
            for col_idx, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                self.table.setItem(row_idx, col_idx, item)

    def fill_inputs_from_selection(self):
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            return
        row = selected_rows[0].row()

        self.input_name.setText(self.table.item(row, 1).text())
        self.input_price.setText(self.table.item(row, 2).text())
        self.input_stock.setText(self.table.item(row, 3).text())
        self.input_category.setText(self.table.item(row, 4).text())
        self.input_kcal.setText(self.table.item(row, 5).text())

    def insert_new_menu(self):
        name = self.input_name.text().strip()
        price = self.input_price.text().strip()
        stock = self.input_stock.text().strip()
        category = self.input_category.text().strip()
        kcal = self.input_kcal.text().strip()

        if not stock: stock = '10'

        if not name or not price or not category or not kcal:
            QMessageBox.warning(self, "경고", "모든 항목을 입력해주세요!")
            return

        self.db.insert_hotdog(name, int(price), int(stock), category, int(kcal))
        QMessageBox.information(self, "성공", "메뉴가 추가되었습니다!")
        self.clear_inputs()
        self.load_data()

    def update_menu(self):
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "경고", "수정할 메뉴를 표에서 먼저 클릭해주세요!")
            return

        hotdog_id = int(self.table.item(selected_rows[0].row(), 0).text())
        name = self.input_name.text().strip()
        price = self.input_price.text().strip()
        stock = self.input_stock.text().strip()
        category = self.input_category.text().strip()
        kcal = self.input_kcal.text().strip()

        self.db.update_hotdog(hotdog_id, name, int(price), int(stock), category, int(kcal))
        QMessageBox.information(self, "성공", "메뉴 정보가 수정되었습니다!")
        self.clear_inputs()
        self.load_data()

    def delete_menu(self):
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "경고", "삭제할 메뉴를 표에서 먼저 클릭해주세요!")
            return

        hotdog_id = int(self.table.item(selected_rows[0].row(), 0).text())
        name = self.table.item(selected_rows[0].row(), 1).text()

        reply = QMessageBox.question(self, "확인", f"'{name}' 메뉴를 정말 삭제하시겠습니까?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.db.delete_hotdog(hotdog_id)
            QMessageBox.information(self, "성공", "메뉴가 삭제되었습니다.")
            self.clear_inputs()
            self.load_data()

    def clear_inputs(self):
        self.input_name.clear()
        self.input_price.clear()
        self.input_stock.clear()
        self.input_category.clear()
        self.input_kcal.clear()

    def add_to_cart(self):
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows: return
        row = selected_rows[0].row()
        menu_name = self.table.item(row, 1).text()
        price = int(self.table.item(row, 2).text())
        if menu_name in self.cart_items:
            self.cart_items[menu_name]['qty'] += 1
        else:
            self.cart_items[menu_name] = {'price': price, 'qty': 1}
        self.update_cart_ui()

    def change_qty(self, menu_name, amount):
        if menu_name in self.cart_items:
            self.cart_items[menu_name]['qty'] += amount
            if self.cart_items[menu_name]['qty'] <= 0: del self.cart_items[menu_name]
            self.update_cart_ui()

    def update_cart_ui(self):
        self.cart_table.setRowCount(len(self.cart_items))
        total_price = 0
        for idx, (menu_name, info) in enumerate(self.cart_items.items()):
            qty = info['qty']
            price = info['price']
            total_price += price * qty
            self.cart_table.setItem(idx, 0, QTableWidgetItem(menu_name))
            self.cart_table.setItem(idx, 1, QTableWidgetItem(f"{price}원"))
            btn_minus = QPushButton("-")
            btn_minus.clicked.connect(lambda checked, m=menu_name: self.change_qty(m, -1))
            self.cart_table.setCellWidget(idx, 2, btn_minus)
            self.cart_table.setItem(idx, 3, QTableWidgetItem(f"{qty}개"))
            btn_plus = QPushButton("+")
            btn_plus.clicked.connect(lambda checked, m=menu_name: self.change_qty(m, 1))
            self.cart_table.setCellWidget(idx, 4, btn_plus)
        self.total_label.setText(f"총 결제 금액: {total_price}원")

    # 🟢 [신규] 결제하기 버튼을 눌렀을 때 실행되는 함수 (새 결제창 연결)
    def checkout(self):
        if not self.cart_items:
            QMessageBox.warning(self, "알림", "장바구니가 비어있습니다.")
            return

        total_price = sum(info['price'] * info['qty'] for info in self.cart_items.values())

        # 새로 만든 결제창 띄우기
        dialog = PaymentDialog(total_price, self)

        # 결제창에서 '결제하기'를 성공적으로 누른 경우 (주소까지 잘 입력하고)
        if dialog.exec_() == QDialog.Accepted:
            address = dialog.input_address.text().strip()
            QMessageBox.information(self, "주문 접수 완료", f"결제가 완료되었습니다!\n[{address}]로 맛있게 배달해 드릴게요 🛵")

            self.cart_items.clear()
            self.update_cart_ui()