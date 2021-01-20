from tkinter import *
import math
import winsound

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 0.05
SHORT_BREAK_MIN = 0.05
LONG_BREAK_MIN = 0.05

reps = 0
timer = None

checkmarks_list = ["__", "__", "__", "__"]


# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    start_button["state"] = "active"
    global checkmarks_list
    global reps
    reps = 0
    window.after_cancel(timer)
    timer_label.config(text="Timer", fg=GREEN)
    canvas.itemconfig(timer_text, text="00:00")
    checkmarks_list = ["__", "__", "__", "__"]
    checkmarks_label.config(text=checkmarks_list)


def work_sessions_completed():
    start_button["state"] = "active"
    global checkmarks_list
    global reps
    reps = 0
    window.after_cancel(timer)
    timer_label.config(text="Work Sessions Completed! Click Start to begin again.", fg=GREEN, font=(FONT_NAME, 14, "bold"))
    canvas.itemconfig(timer_text, text="00:00")
    checkmarks_list = ["__", "__", "__", "__"]
    checkmarks_label.config(text=checkmarks_list)


# ---------------------------- TIMER MECHANISM ------------------------------- #

def start_timer():
    start_button["state"] = "disabled"
    global reps
    reps += 1
    if reps == 9:
        work_sessions_completed()
    elif reps % 2 != 0:
        work_seconds = WORK_MIN * 60
        timer_label.config(text="Work", fg=GREEN)
        count_down(work_seconds)
    elif reps % 2 == 0:
        if reps < 8:
            short_break_seconds = SHORT_BREAK_MIN * 60
            timer_label.config(text="Short Break", fg=PINK)
            count_down(short_break_seconds)
        else:
            long_break_seconds = LONG_BREAK_MIN * 60
            timer_label.config(text="Long Break", fg=RED)
            count_down(long_break_seconds)



# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #


def count_down(count):
    global reps
    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"
    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        window.focus_force()
        winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
        start_timer()
        for _ in range(math.floor(reps / 2)):
            checkmarks_list[_] = "✔"
            checkmarks_label.config(text=checkmarks_list)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

# Create Tomato canvas
canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 32, "bold"))
canvas.grid(column=1, row=1)

# Create Timer Label
timer_label = Label(text="Timer", font=(FONT_NAME, 32, "bold"), fg=GREEN, bg=YELLOW)
timer_label.grid(column=1, row=0)

# Create checkmark Label
checkmarks_label = Label(text=checkmarks_list, fg=GREEN, bg=YELLOW)
checkmarks_label.grid(column=1, row=4)

#Create Progress Label
progress_label = Label(text="Work Sessions Completed", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 14, "bold"))
progress_label.grid(column=1, row=5)

# Create Start and Reset buttons
start_button = Button(text="Start", highlightthickness=0, command=start_timer)
start_button.grid(column=0, row=3)

reset_button = Button(text="Reset", highlightthickness=0, command=reset_timer)
reset_button.grid(column=2, row=3)

window.mainloop()
