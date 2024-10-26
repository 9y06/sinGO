import sys
import tty
import termios
from datetime import datetime
from prettytable import PrettyTable

# 전역 변수로 사용자 유형을 저장
is_admin = False

# 함수: 단일 문자 읽기
def read_single_char():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        char = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return char

# 함수: 입력받을 때 *로 표시
def get_input(prompt=""):
    print(prompt, end='', flush=True)
    input_str = ""
    while True:
        char = read_single_char()
        if char == '\n' or char == '\r':  # Enter key
            print()  # Move to the next line
            break
        elif char == '\b' or ord(char) == 127:  # Backspace key
            if len(input_str) > 0:
                input_str = input_str[:-1]
                # Erase the last '*' from the console
                sys.stdout.write('\b \b')
                sys.stdout.flush()
        else:
            input_str += char
            sys.stdout.write('*')
            sys.stdout.flush()
    return input_str

# 학생 로그인 함수
def stu_login():
    username = input("아이디를 입력하세요. : ")
    password = get_input("비밀번호를 입력하세요. : ")

    # 간단한 인증 예제 (id는 학생이름 비밀번호는 학반번호.)
    valid_users = {
        "김하나": "1201",
        "서진교": "1202",
        "신민채": "1203",
        "윤효진": "1204",
        "이유정": "1205",
        "김동현": "1206",
        "김동훈": "1207",
        "김민규": "1208",
        "김민준": "1209",
        "김성한": "1210",
        "김은찬": "1211",
        "김정현": "1212",
        "동경호": "1213",
        "백선웅": "1214",
        "오정민": "1215",
        "이지호": "1216",
        "정민성": "1217",
        "진예준": "1218",
    }

    if username in valid_users and password == valid_users[username]:
        print("로그인 되었습니다.")
        return True  # 메뉴로 넘어감
    else:
        print("로그인에 실패하였습니다. 아이디나 비밀번호를 확인해주세요.")
        return False  # 메뉴로 못 넘어감

# 관리자 로그인 함수
def mng_login():
    username = input("아이디를 입력하세요. : ")
    password = get_input("비밀번호를 입력하세요. : ")

    if username == "admin" and password == "admin1234":
        print("로그인 되었습니다.")
        return True  # 메뉴로 넘어감
    else:
        print("로그인에 실패하였습니다. 아이디나 비밀번호를 확인해주세요.")
        return False  # 메뉴로 못 넘어감

# 관리자, 학생 구분 함수
def main():
    global is_admin
    user_type = int(input('관리자 로그인 : 1, 재학생 로그인 : 2  '))

    if user_type == 1:
        if not mng_login():
            return
        is_admin = True
    elif user_type == 2:
        if not stu_login():
            return
        is_admin = False
        
    # 로그인 성공 후 카테고리 선택으로 넘어감
    categori()

# 카테고리 구분 함수 
def categori():
    user_choice = int(input('불편 사항 신고 : 1, 학교 생활 신고 : 2  '))

    if user_choice == 1:
        handle_choice()
    elif user_choice == 2:
        handle_choice2()
    else:
        print('다시 입력해주세요.')
        categori()

# 불편 사항 처리 함수
reports = []

def add_report():
    description = input("신고내용 : ")
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    reports.append({"description": description, "date": date, "resolved": False})
    print(f"불편 사항이 추가되었습니다. ({date})")

def list_reports():
    table = PrettyTable()
    table.field_names = ["신고번호", "내용", "처리상태"]
    for index, report in enumerate(reports):
        status = "완료" if report["resolved"] else "미처리"
        table.add_row([index + 1, report["description"], status])
    print(table)

def view_report():
    report_number = int(input("확인할 신고 번호를 입력하세요.: ")) - 1
    if 0 <= report_number < len(reports):
        report = reports[report_number]
        status = "완료" if report["resolved"] else "미처리"
        table = PrettyTable()
        table.field_names = ["내용", "접수날짜", "처리상태"]
        table.add_row([report["description"], report["date"], status])
        print(table)
    else:
        print("유효한 신고 번호를 입력하세요.")

def resolve_report():
    if not is_admin:
        print("권한이 없습니다.")
        return
    report_number = int(input("처리할 신고 번호를 입력하세요.: ")) - 1
    if 0 <= report_number < len(reports):
        reports[report_number]["resolved"] = True
        print("신고가 처리되었습니다.")
    else:
        print("유효한 신고 번호를 입력하세요.")

# 학교 생활 처리 함수
reports2 = []

def add_report2():
    description = input("신고내용 : ")
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    reports2.append({"description": description, "date": date, "resolved": False})
    print(f"학교 생활 문제가 추가되었습니다. ({date})")

def list_reports2():
    table = PrettyTable()
    table.field_names = ["신고번호", "내용", "처리상태"]
    for index, report in enumerate(reports2):
        status = "완료" if report["resolved"] else "미처리"
        table.add_row([index + 1, report["description"], status])
    print(table)

def view_report2():
    report_number = int(input("확인할 신고 번호를 입력하세요.: ")) - 1
    if 0 <= report_number < len(reports2):
        report = reports2[report_number]
        status = "완료" if report["resolved"] else "미처리"
        table = PrettyTable()
        table.field_names = ["내용", "접수날짜", "처리상태"]
        table.add_row([report["description"], report["date"], status])
        print(table)
    else:
        print("유효한 신고 번호를 입력하세요.")

def resolve_report2():
    if not is_admin:
        print("권한이 없습니다.")
        return
    report_number = int(input("처리할 신고 번호를 입력하세요.: ")) - 1
    if 0 <= report_number < len(reports2):
        reports2[report_number]["resolved"] = True
        print("신고가 처리되었습니다.")
    else:
        print("유효한 신고 번호를 입력하세요.")

def choice():  # 불편한 시설 신고하기 함수
    commands_table = PrettyTable()
    commands_table.field_names = ["불편 시설 신고", "입력하시오"]
    commands_table.add_row(["신고하기", "[add]"])
    commands_table.add_row(["신고 리스트 보기", "[list]"])
    commands_table.add_row(["처리 현황 보기", "[view]"])
    commands_table.add_row(["신고 처리하기", "[resolve]"])
    commands_table.add_row(["실행 종료", "[quit]"])

    print(commands_table)

def choice2():  # 학교 생활 문제 신고 함수
    commands_table2 = PrettyTable()
    commands_table2.field_names = ["학교 생활 문제 신고", "입력하시오"]
    commands_table2.add_row(["신고하기", "[add]"])
    commands_table2.add_row(["신고 리스트 보기", "[list]"])
    commands_table2.add_row(["처리 현황 보기", "[view]"])
    commands_table2.add_row(["신고 처리하기", "[resolve]"])
    commands_table2.add_row(["실행 종료", "[quit]"])

    print(commands_table2)

def handle_choice():
    choice()
    while True:
        command = input().strip().lower()
        if command == 'add':
            add_report()
        elif command == 'list':
            list_reports()
        elif command == 'view':
            view_report()
        elif command == 'resolve':
            resolve_report()
        elif command == 'quit':
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 입력입니다. 다시 입력하세요.")

def handle_choice2():
    choice2()
    while True:
        command = input().strip().lower()
        if command == 'add':
            add_report2()
        elif command == 'list':
            list_reports2()
        elif command == 'view':
            view_report2()
        elif command == 'resolve':
            resolve_report2()
        elif command == 'quit':
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 입력입니다. 다시 입력하세요.")

if __name__ == "__main__":
    main()
