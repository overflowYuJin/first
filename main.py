import tkinter as tk
import sys
import json
import subprocess



with open('data.json', 'r') as file:
    data = json.load(file)

# 기초 설정이 안되 있음 << 실행하면 안됌
if not data.get('setting'): 
    print('setting is false')
    subprocess.run(["python3", "start_gui.py"])
    sys.exit()



# 입력한 비밀번호
password_list = []

# 지정된 비밀번호
user_password = list(data['password'])

# 비밀번호 창
lock_window = tk.Tk()

# 사용자 화면 값
screen_width = lock_window.winfo_screenwidth()
screen_height = lock_window.winfo_screenheight()

# 버튼 작동 함수
def button_actions(number, side):
    try:
        if side == "Left" and number in [1,2,3,4]:
                password_add_event(number)
        elif side == "Right" and number in [5,6,7,8]:
                password_add_event(number)
        else:
            raise ValueError
    except ValueError as V:
        print(f"{V}")
        sys.exit()



def left_button(number):
    button_actions(number, "Left")



def right_button(number):
    button_actions(number, "Right")


# 비밀번호 입력 함수
def password_add_event(number):
    password_list.append(str(number))
    password_entry("do")

    
    if len(password_list) == 6: # 비밀번호를 다 침.
        if password_list == user_password:
            print("correct password")
            main_menu()
        else:
            print("Wrong password")
            password_list.clear()
            password_entry("wrong")

# 잠금해체 후 열릴 화면
def main_menu():
    lock_window.destroy()
    print("locker window was closed")
    
    main_width = 300
    main_height = 400

    main = tk.Tk()
    main.title("test")
    
    main.geometry(f"{main_width}x{main_height}")

    reset_width = 100
    reset_height = 50


    def reset():

        data['setting'] = False
        data['password'] = 000000

        with open('data.json', 'w') as file:
            json.dump(data, file, indent=4)

            print("초기화 완료")

        sys.exit()

    reset_button = tk.Button(main, text="reset", command=reset)
    reset_button.place(x= int(main_width/2) - reset_width, y= int(main_height/2) - reset_height, width=reset_width, height=reset_height)



    main.mainloop()




# 비밀번호 입력 초기화
def clear_passwords():
    password_list.clear()
    password_entry("clear")
    print("it was cleared")

# 비밀번호 입력 취소
def cancel_number():
    try:
        password_list.pop()
        password_entry("do")
        print("it was poped?")
    except:
        print("pop_Except")
    
# 창 크기
window_width = 700
window_height = 300

half_window_width = window_width/2
half_window_height = window_height/2

# 초기 창 좌표
x_coordinate = int((screen_width/2)-(half_window_width))
y_coordinate = int((screen_height/2)- (2 * int(half_window_height)+ 0.5 * (half_window_height)))

lock_window.title("비밀번호를 입력해")
lock_window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")
lock_window.resizable(False,False)

button_width = 175
button_height = 50

left_X_coordinate = 50
Y_constant = 65
X_constant = 50

left_button_texts = ["1", "2", "3", "4"]
right_button_texts = ["5", "6", "7", "8"]

# 좌버튼 생성
for i in range(4):
    l_button = tk.Button(lock_window, text=left_button_texts[i], command=lambda i=i: left_button(i+1))
    l_button.place(x=X_constant, y= 25 + i * Y_constant, width=button_width, height=button_height)

# 우버튼 생성
for i in range(4):
    r_button = tk.Button(lock_window, text=right_button_texts[i], command=lambda i=i: right_button(i+5)) 
    r_button.place(x=window_width-(X_constant + int(button_width)), y = 25 + i * Y_constant, width=button_width, height=button_height)

# 그 외의 기능 버튼

y_offset = 25 + Y_constant

special_button_width = 50
special_button_height = 3 * Y_constant - 15

# 왼쪽에 위치함
cancel_button = tk.Button(lock_window, text="cancel", command=cancel_number)
cancel_button.place(x= int(window_width/2) - 120 , y= y_offset , width=special_button_width, height=special_button_height)

# 오른쪽에 위치함
clear_button = tk.Button(lock_window, text="clear", command=clear_passwords)
clear_button.place(x= int(window_width/2) + 70 , y = y_offset, width=special_button_width, height= special_button_height)

# 비밀번호 표시기
mark_entry = tk.Entry(lock_window, state="normal", bg="white", justify="center", )
mark_entry.place(x=X_constant + button_width + 10 , y=25, height=50, width= 230)

# 남은 비밀번호 자리 표시하는 함수
def password_entry(function):
    mark_entry.config(state="normal") 
    mark_entry.delete(0, 'end')

    if function == "do": 
        mark_entry.insert(0, f"{'* ' * len(password_list) + '- ' * (6-len(password_list))}")

    elif function == "clear": 
        mark_entry.insert(0, f"{"- " * 6 }")

    elif function == "wrong":
        mark_entry.insert(0, "Wrong Number.")

    mark_entry.config(state="readonly") # 잠금

lock_window.after(10, lambda: password_entry("clear")) # 함수 호출을 위함

lock_window.mainloop()