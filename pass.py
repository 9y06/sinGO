import sys
import tty
import termios
from prettytable import Prettytable

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

# 로그인 함수
def stu_login():
    username = input("Enter your username: ")
    password = get_input("Enter your password: ")

    # 간단한 인증 예제 (id는 학생이름 비밀번호는 학반번호.)

    if username == "김하나" and password == "1201":
        print("Login successful!")
    elif username == "서진교" and password == "1202":
        print("Login successful!")
    elif username == "신민채" and password == "1203":
        print("Login successful!")
    elif username == "윤효진" and password == "1204":
        print("Login successful!")
    elif username == "이유정" and password == "1205":
        print("Login successful!")
    elif username == "김동현" and password == "1206":
        print("Login successful!")
    elif username == "김동훈" and password == "1207":
        print("Login successful!")
    elif username == "김민규" and password == "1208":
        print("Login successful!")
    elif username == "김성한" and password == "1210":
        print("Login successful!")
    elif username == "김은찬" and password == "1211":
        print("Login successful!")
    elif username == "김정현" and password == "1212":
        print("Login successful!")
    elif username == "동경호" and password == "1213":
        print("Login successful!")
    elif username == "백선웅" and password == "1214":
        print("Login successful!")
    elif username == "오정민" and password == "1215":
        print("Login successful!")
    elif username == "이지호" and password == "1216":
        print("Login successful!")
    elif username == "정민성" and password == "1217":
        print("Login successful!")
    elif username == "진예준" and password == "1218":
        print("Login successful!")
    else:
        print("Login failed. Invalid username or password.")

def mng_login():
    username = input("Enter your username: ")
    password = get_input("Enter your password: ")


    if username == "admin" and password == "admin1234":
        print("Login successful!")
    else:
        print("Login failed. Invalid username or password.")

Admin = int(input('관리자 로그인 : 1, 재학생 로그인 : 2  '))

if Admin == 1:
    mng_login()

elif Admin == 2:
    stu_login()


# 메뉴 선택하기
menu = input('메뉴를 선택하세요(학교 시설 신고 : 1, 학교 생활 신고 : 2, 문의사항 : 3) :')
if menu == 1:
    print(222)if menu == 2:elelif lielselif nmuenu ==4 : 3:print()    print()