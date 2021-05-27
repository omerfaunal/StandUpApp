"""

    Project name: Stand Up Alert
    Author: Ömer Ünal
    Date created: 27/05/2021
    Python Version: 3.9

"""

from tkinter import *
from tkinter import messagebox
from userInput import UserInput
import pygame

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Comic Sans MS"

# ---------------------------- VARIABLES ------------------------------- #
timer = None
check = True
reps = 1
time = 0
work_time = 0
break_time = 0


# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    global check
    global time
    global reps

    text_break.enable()
    text_work.enable()
    window.after_cancel(timer)
    up_label.config(text="Timer", fg=GREEN)
    canvas.itemconfig(timer_text, text="00:00")
    check_marks.config(text="")
    check = True
    start_button.config(text="Start")
    time = 0
    reps = 1


# ---------------------------- WINDOW FUNCTIONS ------------------------------- #
def raise_window(func_window):
    func_window.attributes('-topmost', 1)
    func_window.attributes('-topmost', 0)


def warning_message(title, message):
    messagebox.showwarning(title, message)


pygame.mixer.init()


def play_sound(sound):
    pygame.mixer.music.load(sound)
    pygame.mixer.music.play(loops=0)


# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    global reps
    global check
    global time

    if check:
        if text_work.get_time() == 0 or text_break.get_time() == 0:
            up_label.config(text="Enter times", fg=RED)
        elif time == 0:
            work_sec = text_work.get_time() * 60
            short_break_sec = text_break.get_time() * 60
            long_break_sec = text_break.get_time()*5 * 60

            if reps % 8 == 0:
                time = long_break_sec
                up_label.config(text="Exercise", fg=RED)

            elif reps % 2 == 0 and reps != 8:
                time = short_break_sec
                up_label.config(text="Move", fg=PINK)

            elif reps % 2 == 1:
                time = work_sec
                up_label.config(text="Work", fg=GREEN)

            reps += 1
            start_button.config(text="Stop", bg=RED)
            check = False
            count_down()
        else:
            check = False
            start_button.config(text="Stop", bg=RED)
            count_down()

    else:
        window.after_cancel(timer)
        check = True
        start_button.config(text="Start", bg=GREEN)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down():
    global time

    minute = time // 60
    second = time % 60

    canvas.itemconfig(timer_text, text=f"{int(minute):02d}:{int(second):02d}")

    if time > 0:
        global timer
        timer = window.after(1000, count_down)
        time -= 1

    else:
        global check
        check = True

        if reps % 8 == 0:
            play_sound("data/exercise.mp3")
            warning_message("Exercise", "It's time to do some exercise!")
            raise_window(window)
        elif reps % 2 == 0:
            play_sound("data/move.mp3")
            warning_message("Break", "Get up and move!")
            raise_window(window)
        else:
            play_sound("data/continue.mp3")
            warning_message("Work", "Now you can continue!")
            raise_window(window)

        start_timer()

        mark = ""
        for i in range((reps-1)//2):
            mark += "✔"
        check_marks.config(text=mark)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Stand Up Alert")
window.config(padx=50, pady=50, bg=YELLOW)

container = Frame(window)
container.grid(column=1, row=0)

up_label = Label(text="Stand Up", font=(FONT_NAME, 20, "bold"), bg=YELLOW, fg=GREEN)
up_label.grid(column=1, row=1)

work_label = Label(container, text="", font=(FONT_NAME, 10, "normal"), bg=YELLOW, fg=PINK)
work_label.pack(side="left")

break_label = Label(container, text="", font=(FONT_NAME, 10, "normal"), bg=YELLOW, fg=PINK)
break_label.pack(side="right")

text_work = UserInput(work_label, True, "Work time")
text_work.config(bg=PINK, width=10)
text_work.grid(column=0, row=0)

text_break = UserInput(break_label, False, "Break time")
text_break.config(bg=PINK, width=10, relief="groove")
text_break.grid(column=2, row=0)

canvas = Canvas(width=200, height=274, bg=YELLOW, highlightthickness=0)
tomato_image = PhotoImage(file="data/tomato.png")
canvas.create_image(100, 162, image=tomato_image)
timer_text = canvas.create_text(100, 180, text="00:00", fill="white", font=(FONT_NAME, 20, "bold"))
canvas.grid(column=1, row=2)

start_button = Button(text="Start", command=start_timer, bg=GREEN, fg="white", relief="groove")
start_button.grid(column=0, row=3)

reset_button = Button(text="Reset", command=reset_timer, bg=RED, fg="white", relief="groove")
reset_button.grid(column=2, row=3)

check_marks = Label(fg=GREEN, bg=YELLOW)
check_marks.grid(column=1, row=4)

window.mainloop()
