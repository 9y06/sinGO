import sys  # 시스템 관련 작업을 위한 모듈
import tty  # 터미널 관련 작업을 위한 모듈
import termios  # 터미널 I/O 설정을 위한 모듈
import json  # JSON 파일 읽기/쓰기 작업을 위한 모듈
from datetime import datetime  # 날짜 및 시간 처리를 위한 모듈
from prettytable import PrettyTable  # 테이블 형식으로 데이터를 출력하기 위한 모듈

# 신고 데이터 파일 경로
reports_file = "reports.json"
reports2_file = "reports2.json"

# 신고 데이터를 로드하는 함수
def load_reports(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            if isinstance(data, list):  # 데이터가 리스트인지 확인
                return data
            else:
                return []  # 리스트가 아니면 빈 리스트 반환
    except FileNotFoundError:
        return [] # 파일을 찾을 수 없으면 빈 리스트 반환

# 신고 데이터를 저장하는 함수
def save_reports(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, ensure_ascii=False, indent=4) # JSON 데이터를 파일에 저장

# 초기 신고 목록 로드
reports = load_reports(reports_file)
reports2 = load_reports(reports2_file)

# 함수: 단일 문자 읽기
def read_single_char():
    fd = sys.stdin.fileno() # 파일 디스크립터 가져오기
    old_settings = termios.tcgetattr(fd) # 현재 터미널 설정 저장
    try:
        tty.setraw(fd) # 터미널을 raw 모드로 설정
        char = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return char

# 함수: 입력받을 때 *로 표시
def read_single_char():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        char = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return char

def get_input(prompt=""):
    print(prompt, end='', flush=True)
    input_str = ""
    while True:
        char = read_single_char()
        if char == '\n' or char == '\r':  # 엔터 키
            print()  # Move to the next line
            break
        elif char == '\b' or ord(char) == 127:  # 백스페이스 키
            if len(input_str) > 0:
                input_str = input_str[:-1] # 입력 문자열에서 마지막 문자 제거
                sys.stdout.write('\b \b') # 콘솔에서 마지막 * 제거
                sys.stdout.flush()
        else:
            input_str += char # 입력 문자열에 문자 추가
            if prompt.startswith("비밀번호"):
                sys.stdout.write('*')  # 비밀번호 입력 시 '*'로 표시
            else:
                sys.stdout.write(char)
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
        return "student"  # 학생을 리텀함
    else:
        print("로그인에 실패하였습니다. 아이디나 비밀번호를 확인해주세요.")
        return stu_login() # 다시 로그인

# 관리자 로그인 함수
def mng_login():
    username = input("아이디를 입력하세요. : ")
    password = get_input("비밀번호를 입력하세요. : ")

    if username == "admin" and password == "admin1234":
        print("로그인 되었습니다.")
        return "manager"  # 관리자를 리턴함 -> resolve에 권한이 주어짐
    else:
        print("로그인에 실패하였습니다. 아이디나 비밀번호를 확인해주세요.")
        return mng_login() # 다시 로그인

# 관리자, 학생 구분 함수
def main():
    user_type = int(input('관리자 로그인 : 1, 재학생 로그인 : 2  '))

    if user_type == 1:
        user_role = mng_login()
    elif user_type == 2:
        user_role = stu_login()
    else:
        print("잘못된 입력입니다.")
        return

    if user_role:
        # 로그인 성공 후 카테고리 선택으로 넘어감
        categori(user_role)

# 카테고리 구분 함수 
def categori(user_role): # 사용자로부터 불편 사항 신고(1) 또는 학교 생활 신고(2) 중 하나를 선택받습니다.
    user_choice = int(input('불편 시설 신고 : 1, 학교 생활 신고 : 2  '))

    if user_choice == 1:
        choice() # choice() 함수를 호출하여 불편 사항 신고의 세부 선택을 받기
        handle_choice(user_role) # 선택된 기능을 처리하기 위해 handle_choice() 함수를 호출
    elif user_choice == 2:
        choice2() # choice2() 함수를 호출하여 학교 생활 신고의 세부 선택을 받기
        handle_choice2(user_role) # 선택된 기능을 처리하기 위해 handle_choice2() 함수를 호출합니다.
    else:
        # 사용자가 1 또는 2 이외의 값을 입력했을 경우, 다시 입력할 수 있게 한다.
        print('다시 입력해주세요.')
        categori(user_role)

# 불편 사항 처리 함수
def add_report(): # 불편사항 신고
    description = input("신고내용 : ")
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # 현재 시간을 가져와서 "년-월-일 시:분:초" 형식으로 포맷합니다.
    reports.append({"description": description, "date": date, "resolved": False}) # report 리스트에 새로운 신고 항목을 제목, 일시, 미처리 상태로 추가한다.
    save_reports(reports, reports_file)
    print(f"불편 사항이 추가되었습니다. ({date})")

def list_reports(): # 불편사항 전체 목록 보기
    table = PrettyTable()
    table.field_names = ["신고번호", "내용", "처리상태"] # 테이블의 열 이름을 설정합니다.
    for index, report in enumerate(reports):
        status = "완료" if report["resolved"] else "미처리"  # 처리 상태에 따라 텍스트를 설정합니다.
        table.add_row([index + 1, report["description"], status]) # 테이블에 한 행을 추가합니다. 신고번호는 인덱스 + 1로 지정합니다.
    print(table)

def view_report(): # 하나의 불편사항 자세히 보기
    report_number = int(input("확인할 신고 번호를 입력하세요.: ")) - 1
    if 0 <= report_number < len(reports): # 입력된 신고 번호가 유효한지 확인합니다.
        report = reports[report_number] # reports 리스트에서 해당 신고 번호에 해당하는 신고 항목을 가져옵니다.
        status = "완료" if report["resolved"] else "미처리" # 처리 상태에 따라 텍스트를 설정합니다.
        table = PrettyTable() # PrettyTable 객체를 생성하여 테이블을 만듭니다.
        table.field_names = ["내용", "접수날짜", "처리상태"]
        table.add_row([report["description"], report["date"], status])
        print(table)
    else:
        print("유효한 신고 번호를 입력하세요.")
        return view_report()

def resolve_report(user_role): # 불편사항 처리상태 수정하기
    if user_role == "manager": # 사용자가 "manager"인 경우 처리를 진행합니다.
        report_number = int(input("처리할 신고 번호를 입력하세요.: ")) - 1
        if 0 <= report_number < len(reports): # 입력된 신고 번호가 유효한지 확인합니다.
            reports[report_number]["resolved"] = True # 해당 신고 항목의 처리 상태를 "완료"로 변경합니다.
            save_reports(reports, reports_file) # 변경된 신고 리스트를 파일에 저장합니다.
            print("신고가 처리되었습니다.")
        else:
            print("유효한 신고 번호를 입력하세요.")
    else:
        print("권한이 없습니다.")

# 학교 생활 처리 함수
def add_report2(): 
    description = input("신고내용 : ")
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    reports2.append({"description": description, "date": date, "resolved": False})
    save_reports(reports2, reports2_file)
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
        print("입력된 신고번호는 유효하지 않습니다.")

def resolve_report2(user_role):
    if user_role == "manager":
        report_number = int(input("처리할 신고 번호를 입력하세요.: ")) - 1
        if 0 <= report_number < len(reports2):
            reports2[report_number]["resolved"] = True
            save_reports(reports2, reports2_file)
            print("신고가 처리되었습니다.")
        else:
            print("유효한 신고 번호를 입력하세요.")
    else:
        print("권한이 없습니다.")

def choice():  # 불편한 시설 신고하기 함수
    commands_table = PrettyTable() # PrettyTable 객체를 생성하여 테이블을 만듭니다.
    commands_table.field_names = ["불편 시설 신고", "입력하시오"] # 테이블의 열 이름을 설정합니다.
    commands_table.add_row(["신고하기", "[add]"]) # 테이블에 각 메뉴 항목을 추가합니다.
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

def handle_choice(user_role):
    while True:
        command = input().strip().lower() # 사용자로부터 명령을 입력받습니다. 입력 문자열의 앞뒤 공백을 제거하고 소문자로 변환합니다.
        if command == 'add':
            add_report()
        elif command == 'list':
            list_reports()
        elif command == 'view':
            view_report()
        elif command == 'resolve':
            resolve_report(user_role)
        elif command == 'quit':
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 입력입니다. 다시 입력하세요.")

def handle_choice2(user_role):
    while True:
        command2 = input().strip().lower()
        if command2 == 'add':
            add_report2()
        elif command2 == 'list':
            list_reports2()
        elif command2 == 'view':
            view_report2()
        elif command2 == 'resolve':
            resolve_report2(user_role)
        elif command2 == 'quit':
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 입력입니다. 다시 입력하세요.")

if __name__ == "__main__":
    main()
