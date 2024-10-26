from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # 레이아웃 생성
        layout = QVBoxLayout()

        # 사용자 이름 라벨과 입력란 생성
        self.username_label = QLabel('Username:', self)
        self.username_input = QLineEdit(self)

        # 비밀번호 라벨과 입력란 생성
        self.password_label = QLabel('Password:', self)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)

        # 로그인 버튼 생성
        self.login_button = QPushButton('Login', self)
        self.login_button.clicked.connect(self.handle_login)

        # 레이아웃에 위젯 추가
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)

        # 레이아웃 설정
        self.setLayout(layout)

        # 창 설정
        self.setWindowTitle('Login')
        self.setGeometry(300, 300, 300, 200)

    def handle_login(self):
        # 사용자 이름과 비밀번호 가져오기
        username = self.username_input.text()
        password = self.password_input.text()

        # 간단한 검증
        if username == '서진교' and password == '1202':
            QMessageBox.information(self, 'Success', 'Login Successful')
        elif username == '신민채' and password == '1203':
            QMessageBox.information(self, 'Success', 'Login Successful')
        else:
            QMessageBox.warning(self, 'Error', 'Bad Username or Password')

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
