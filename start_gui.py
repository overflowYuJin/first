import tkinter as tk
import sys
import json
import subprocess

with open('data.json', 'r') as file:
    json_data = json.load(file)

Main_width = 300
Main_height = 100
Can_write = True

#기본 창 설정
Main = tk.Tk()
Main.title("설정")
Main.geometry(f"{Main_width}x{Main_height}")
Main.resizable(False, False)

Input_entry = tk.Entry(Main, justify="left")
Input_entry.place(x=0,y=0, width=200, height=50)

Output_entry = tk.Entry(Main, state="readonly", justify="center", bg="white")
Output_entry.place(x=0, y=50, width=300, height=50)

def Output_message(contents):
    try:
        Output_entry.config(state="normal") 
        Output_entry.delete(0, 'end')

        #내용 수정
        Output_entry.insert(0, contents)

        Output_entry.config(state="readonly")
        return True # 성공적으로 바꿈

    except Exception as E:
        print(f"{E}")
        sys.exit()

def setting(contents):
    global Can_write
    try:
        if contents == "start":
            data = Input_entry.get()
            if data.isdigit() and len(data) == 6 and '9' not in data and '0' not in data:

                json_data['setting'] = True
                json_data['password'] = data

                with open('data.json', 'w') as file:
                    json.dump(json_data, file, indent=4)

                print(f"비밀번호 설정됌 : {data}")

                subprocess.Popen(["python3", "main.py"])
                sys.exit()
            else:
                Output_message(f"0, 9가 포함되지 않은 6자리 번호를 입력")
                Input_entry.delete(0, 'end')
        else:
            Output_message("비밀번호를 입력해")


    except Exception as e:
        print(f"{e}")
        sys.exit()

def pressed_button():
    setting("start")

Pass_button = tk.Button(Main, text="enter", command=pressed_button)
Pass_button.place(x=200,y=0, width=100, height=50)

Main.after(10, lambda: setting("Nope"))


Main.mainloop()

