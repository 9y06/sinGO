import sys
import tty
import termios
import json
from datetime import datetime
from prettytable import PrettyTable

# 신고 데이터 파일 경로
reports_file = "reports.json"
reports2_file = "reports2.json"

# 로그인 상태 변수
current_user_type = None

# 신고 데이터를 로드하는 함수
def load_reports(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            if isinstance(data, list):  # 리스트인지 확인
                return data
            else:
                return []  # 리스트가 아니면 빈 리스트 반환
    except FileNotFoundError:
        return []

# 신고 데이터를 저장하는 함수
def save_reports(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# 초기 신고 목록 로드
reports = load_reports(reports_file)
reports2 = load_reports(reports2_file)

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
            if prompt.startswith("비밀번호"):
                sys.stdout.write('*')  # 비밀번호 입력 시 '*'로 표시
            else:
                sys.stdout.write(char)
            sys.stdout.flush()
    return input_str

# 학생 로그인 함수
def stu_login():
    global current_user_type
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
        current_user_type = "student"
        return True  # 메뉴로 넘어감
    else:
        print("로그인에 실패하였습니다. 아이디나 비밀번호를 확인해주세요.")
        return False  # 메뉴로 못 넘어감

# 관리자 로그인 함수
def mng_login():
    global current_user_type
    username = input("아이디를 입력하세요. : ")
    password = get_input("비밀번호를 입력하세요. : ")

    if username == "admin" and password == "admin1234":
        print("로그인 되었습니다.")
        current_user_type = "admin"
        return True  # 메뉴로 넘어감
    else:
        print("로그인에 실패하였습니다. 아이디나 비밀번호를 확인해주세요.")
        return False  # 메뉴로 못 넘어감

# 관리자, 학생 구분 함수
def main():
    user_type = int(input('관리자 로그인 : 1, 재학생 로그인 : 2  '))

    if user_type == 1:
        if not mng_login():
            return
    elif user_type == 2:
        if not stu_login():
            return
        
    # 로그인 성공 후 카테고리 선택으로 넘어감
    categori()

# 카테고리 구분 함수 
def categori():
    user_choice = int(input('불편 사항 신고 : 1, 학교 생활 신고 : 2  '))

    if user_choice == 1:
        choice()
        handle_choice()
    elif user_choice == 2:
        choice2()
        handle_choice2()
    else:
        print('다시 입력해주세요.')
        categori()

# 불편 사항 처리 함수
def add_report():
    description = input("신고내용 : ")
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    reports.append({"description": description, "date": date, "resolved": False})
    save_reports(reports, reports_file)
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
    if current_user_type == "admin":
        report_number = int(input("처리할 신고 번호를 입력하세요.: ")) - 1
        if 0 <= report_number < len(reports):
            reports[report_number]["resolved"] = True
            save_reports(reports, reports_file)
            print("신고가 처리되었습니다.")

