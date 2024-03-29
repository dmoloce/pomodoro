from tkinter import *
import math

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None
paused = False


# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    title_label.config(text="Timer")
    checkmarks.config(text="")
    global reps
    reps = 0


# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    global reps
    reps += 1

    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if reps % 8 == 0:
        countdown(long_break_sec)
        title_label.config(text="Long Break", fg=RED)
    elif reps % 2 == 0:
        countdown(short_break_sec)
        title_label.config(text="Short Break", fg=PINK)
    else:
        countdown(work_sec)
        title_label.config(text="Work", fg=GREEN)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def countdown(count):
    global timer
    global paused

    if paused:
        return

    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"
    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        timer = window.after(1000, countdown, count - 1)
    else:
        start_timer()
        marks = ""
        work_sessions = math.floor(reps / 2)
        for _ in range(work_sessions):
            marks += "✔"
        checkmarks.config(text=marks)

# ---------------------------- PAUSE MECHANISM ------------------------------- #
def pause_timer():
    global paused
    global timer
    paused = not paused
    if paused:
        window.after_cancel(timer)
        pause_button.config(text="Resume")
    else:
        pause_button.config(text="Pause")
        # Correctly calculate remaining time in seconds from the mm:ss format
        current_time = canvas.itemcget(timer_text, 'text').split(":")
        count_resume = int(current_time[0]) * 60 + int(current_time[1])
        countdown(count_resume)

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

title_label = Label(text="Timer", font=(FONT_NAME, 32, "bold"), fg=GREEN, bg=YELLOW)
title_label.grid(column=1, row=0)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 29, "bold"))
canvas.grid(column=1, row=2)

button_start = Button(text="Start", highlightthickness=0, command=start_timer)
button_start.grid(column=0, row=3)

pause_button = Button(text="Pause", highlightthickness=0, command=pause_timer)
pause_button.grid(column=1, row=3)

button_reset = Button(text="Reset", highlightthickness=0, command=reset_timer)
button_reset.grid(column=2, row=3)

checkmarks = Label(font=("Arial", 20, "bold"), fg=GREEN, bg=YELLOW)
checkmarks.grid(column=1, row=4)

window.mainloop()
