import tkinter as tk
import random
import pandas as pd
from tkinter import messagebox

BACKGROUND_COLOR = "#b1ddc6"
current_card = {}
# ---------- READING DATA ----------
try:
    data = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    data = pd.read_csv("data/french_words.csv")
finally:
    word_list = data.to_dict(orient="records")


# ---------- CHANGE WORD ----------
def new_card():
    global current_card, flip_timer, start
    window.after_cancel(flip_timer)
    try:
        current_card = random.choice(word_list)
    except IndexError:
        messagebox.showinfo(title="Oops", message="You have finished all the words.")

    canvas.itemconfig(title, text="French", fill="black")
    canvas.itemconfig(word_text, text=current_card["French"], fill="black")
    canvas.itemconfig(canvas_image, image=front_img)

    flip_timer = window.after(3000, flip_card)

# ---------- REMOVE CURRENT WORD FROM LIST ----------
def is_known():
    word_list.remove(current_card)
    data = pd.DataFrame(word_list)
    data.to_csv('data/words_to_learn.csv', index=False)
    new_card()
# ---------- BACK WORD ----------
def flip_card():
    canvas.itemconfig(title, text="English", fill="white")
    canvas.itemconfig(word_text, text=current_card["English"], fill="white")
    canvas.itemconfig(canvas_image, image=back_img)


# ---------- UI ----------
window = tk.Tk()
window.minsize(width=900, height=700)
window.maxsize(width=900, height=700)
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, flip_card)

# Image
canvas = tk.Canvas(width=800, height=526, highlightthickness=0)
front_img = tk.PhotoImage(file="images/card_front.png")
back_img = tk.PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=front_img)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=2)

check_img = tk.PhotoImage(file="images/right.png")
unknown_img = tk.PhotoImage(file="images/wrong.png")

# Button
unknown_button = tk.Button(image=unknown_img, highlightthickness=0, bd=0, command=new_card)
unknown_button.grid(column=0, row=1)
check_button = tk.Button(image=check_img, highlightthickness=0, bd=0, command=is_known)
check_button.grid(column=1, row=1)

# Text
title = canvas.create_text(400, 150, text=f"", font=("Ariel", 40, "italic"))
word_text = canvas.create_text(400, 263, text=f"", font=("Ariel", 60, "bold"))

new_card()

window.mainloop()
