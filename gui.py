import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageSequence
import pygame

from noir.mechanics import difficulty

# --------------------
# INIT PYGAME (LJUD)
# --------------------
pygame.mixer.init()

# --------------------
# PATHS
# --------------------
BASE_DIR = os.path.dirname(__file__)

SOUND_PATH = os.path.join(BASE_DIR, "assets", "dice.wav")
SAX_PATH = os.path.join(BASE_DIR, "assets", "sax.wav")
CRASH_PATH = os.path.join(BASE_DIR, "assets", "carcrash.wav")

IMG_PATH = os.path.join(BASE_DIR, "assets", "d10.png")
GIF_PATH = os.path.join(BASE_DIR, "assets", "spin.gif")

FEDORA_PATH = os.path.join(BASE_DIR, "assets", "fedora.png")
GODFATHER_PATH = os.path.join(BASE_DIR, "assets", "godfather.png")
WRONG_PATH = os.path.join(BASE_DIR, "assets", "wrong.png")
NOIRGE_PATH = os.path.join(BASE_DIR, "assets", "noirge.png")

# --------------------
# LADDA LJUD
# --------------------
dice_sound = pygame.mixer.Sound(SOUND_PATH)
sax_sound = pygame.mixer.Sound(SAX_PATH)
crash_sound = pygame.mixer.Sound(CRASH_PATH)

dice_sound.set_volume(0.5)
sax_sound.set_volume(0.7)
crash_sound.set_volume(0.7)

# --------------------
# GUI INIT
# --------------------
root = tk.Tk()
root.title("Noir Dice")
root.geometry("600x650")
root.resizable(True, True)

root.tk.call('tk', 'scaling', 1.4)
root.configure(bg="#e6e6e6")

# --------------------
# STYLE
# --------------------
style = ttk.Style()
style.theme_use("default")

style.configure("TButton", padding=10, font=("Segoe UI", 14))
style.configure("TLabel", font=("Segoe UI", 14), background="#e6e6e6")

# --------------------
# BILDER
# --------------------
def load_img(path, size):
    img = Image.open(path).convert("RGBA")
    img = img.resize(size, Image.LANCZOS)
    return ImageTk.PhotoImage(img)

dice_img = load_img(IMG_PATH, (100, 100))
fedora_img = load_img(FEDORA_PATH, (50, 50))
godfather_img = load_img(GODFATHER_PATH, (60, 60))
wrong_img = load_img(WRONG_PATH, (60, 60))
noirge_img = load_img(NOIRGE_PATH, (60, 60))

# GIF
gif = Image.open(GIF_PATH)
gif_frames = [
    ImageTk.PhotoImage(frame.copy().convert("RGBA").resize((100, 100), Image.LANCZOS))
    for frame in ImageSequence.Iterator(gif)
]

# behåll referenser
root.dice_img = dice_img
root.gif_frames = gif_frames
root.fedora_img = fedora_img
root.godfather_img = godfather_img
root.wrong_img = wrong_img
root.noirge_img = noirge_img

animation_running = False

# --------------------
# GIF ANIMATION
# --------------------
def animate_gif(index=0):
    if not animation_running:
        return
    gif_label.config(image=gif_frames[index])
    root.after(50, animate_gif, (index + 1) % len(gif_frames))

# --------------------
# TÄRNINGSSTIL
# --------------------
def get_style(n):
    if n == 10:
        return "#ffd700", ("Segoe UI", 18, "bold")
    elif n == 1:
        return "#b71c1c", ("Segoe UI", 16, "bold")
    return "black", ("Segoe UI", 16)

# --------------------
# VISA TÄRNINGAR
# --------------------
def show_dice_images(r):
    for widget in dice_frame.winfo_children():
        widget.destroy()

    for d in r["grundslag"]:
        frame = tk.Frame(dice_frame, bg="#e6e6e6")
        frame.pack(side="left", padx=25)

        tk.Label(frame, image=dice_img, bg="#e6e6e6").pack()

        color, font = get_style(d)

        tk.Label(frame, text=str(d), bg="#e6e6e6", fg=color, font=font).pack()

    if r["extra"]:
        tk.Label(dice_frame, text="+", bg="#e6e6e6", font=("Segoe UI", 18)).pack(side="left")

        for d in r["extra"]:
            frame = tk.Frame(dice_frame, bg="#e6e6e6")
            frame.pack(side="left", padx=25)

            tk.Label(frame, image=dice_img, bg="#e6e6e6").pack()

            color, font = get_style(d)

            tk.Label(frame, text=str(d), bg="#e6e6e6", fg=color, font=font).pack()

# --------------------
# RESULTAT
# --------------------
def show_result(value):
    global animation_running

    r, total, success = difficulty(value)

    animation_running = False
    gif_label.config(image="")

    show_dice_images(r)

    exceptional = (
        len(r["grundslag"]) == 2 and
        r["grundslag"][0] == r["grundslag"][1]
    )

    if success and exceptional:
        icon = godfather_img
        text = "EXCEPTIONELLT LYCKAT!"
        sax_sound.play()

    elif success:
        icon = fedora_img
        text = "Lyckat!"

    elif not success and exceptional:
        icon = noirge_img
        text = "EXCEPTIONELLT MISSLYCKAT!"
        crash_sound.play()

    else:
        icon = wrong_img
        text = "Misslyckat!"

    result_label.config(text=f"Summa: {total}")
    status_label.config(text=text, image=icon, compound="left")

# --------------------
# KNAPP
# --------------------
def run():
    global animation_running

    try:
        value = int(entry.get())
    except:
        result_label.config(text="Fel värde")
        return

    animation_running = True
    animate_gif()

    dice_sound.play()

    root.after(500, lambda: show_result(value))

# --------------------
# UI
# --------------------
title_frame = tk.Frame(root, bg="#e6e6e6")
title_frame.pack(pady=20)

tk.Label(title_frame, image=fedora_img, bg="#e6e6e6").pack(side="left", padx=10)

tk.Label(
    title_frame,
    text="NOIR DICE",
    font=("Segoe UI", 24, "bold"),
    bg="#e6e6e6"
).pack(side="left")

input_frame = tk.Frame(root, bg="#e6e6e6")
input_frame.pack(pady=10)

tk.Label(input_frame, text="Värde:", bg="#e6e6e6", font=("Segoe UI", 16)).pack(side="left")

entry = tk.Entry(input_frame, font=("Segoe UI", 16), width=6)
entry.pack(side="left", padx=10)

ttk.Button(root, text="Slå", command=run).pack(pady=15)

gif_label = tk.Label(root, bg="#e6e6e6")
gif_label.pack()

dice_frame = tk.Frame(root, bg="#e6e6e6")
dice_frame.pack(pady=20)

result_frame = tk.Frame(root, bg="#dcdcdc", padx=20, pady=15)
result_frame.pack(pady=20)

result_label = tk.Label(result_frame, text="Summa:", bg="#dcdcdc", font=("Segoe UI", 16))
result_label.pack()

status_label = tk.Label(result_frame, text="", bg="#dcdcdc", font=("Segoe UI", 16, "bold"))
status_label.pack(pady=10)

# --------------------
# START
# --------------------
root.mainloop()