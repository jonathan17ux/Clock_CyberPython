import tkinter as tk
from PIL import Image, ImageTk
import datetime
import os

# Set the working directory to the script location
script_dir = os.path.dirname(os.path.abspath(__file__))

# === Setup ===
root = tk.Tk()
root.attributes('-fullscreen', True)         # Fullscreen mode
root.config(cursor="none")                   # Hide mouse cursor

# Allow exit with ESC key (optional, for dev mode)


def close(event=None):
    root.destroy()


root.bind("<Escape>", close)

# === Load Background ===
bg_image = Image.open(os.path.join(script_dir, "background_clock.png"))
bg_photo = ImageTk.PhotoImage(bg_image)

canvas = tk.Canvas(root, highlightthickness=0)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, anchor=tk.NW, image=bg_photo)

# === Time / Date Text ===
time_text = canvas.create_text(
    325, 130, fill="#f4bf18", font=("Impact", 100), anchor="e")
p_text = canvas.create_text(
    390, 145, fill="#f4bf18", font=("Impact", 50))
date_text = canvas.create_text(
    325, 220, fill="lightblue", font=("Impact", 40), anchor="e")
day_text = canvas.create_text(
    325, 255, fill="lightblue", font=("Impact", 25), anchor="e")

# === Update Clock ===


def update_clock():
    now = datetime.datetime.now()
    time_str = now.strftime("%I:%M")
    p_str = now.strftime("%p")
    date_str = now.strftime("%B - %d")
    day_str = now.strftime("%A")
    canvas.itemconfig(time_text, text=time_str)
    canvas.itemconfig(p_text, text=p_str)
    canvas.itemconfig(date_text, text=date_str)
    canvas.itemconfig(day_text, text=day_str)
    root.after(1000, update_clock)


update_clock()

# === Load and Animate Gift GIF ===
gif = Image.open(os.path.join(script_dir, "cat.gif"))
frames = []

try:
    while True:
        frame = gif.copy().resize((100, 100))
        frames.append(ImageTk.PhotoImage(frame))
        gif.seek(len(frames))  # Move to next frame
except EOFError:
    pass

gif_index = 0
pause_between_loops = 30000  # Delay after full loop (30 seconds)
gif_item = canvas.create_image(440, 170, anchor=tk.NE, image=frames[0])


def update_gif():
    global gif_index
    canvas.itemconfig(gif_item, image=frames[gif_index])
    if gif_index < len(frames) - 1:

        gif_index += 1
        root.after(100, update_gif)
    else:

        gif_index = 0
        root.after(pause_between_loops, update_gif)


update_gif()

# === Run ===
root.mainloop()
