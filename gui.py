import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageSequence
import winsound

from noir.mechanics import difficulty

# ----------------------
# PATHS
# ----------------------

BASE_DIR = os.path.dirname(__file__)
SOUND_PATH = os.path.join(BASE_DIR, "assets", "dice.wav")
IMG_PATH = os.path.join(BASE_DIR, "assets", "d10.png")
GIF_PATH = os.path.join(BASE_DIR, "assets", "spin.gif")

# ----------------------
# LJUD
# ----------------------

def play_dice_sound():
    try:
        winsound.PlaySound(SOUND_PATH, winsound.SND_FILENAME | winsound.SND_ASYNC)
    except:
        pass

# ----------------------
# GUI ROOT
# ----------------------

root = tk.Tk()
root.configure(bg="#1e1e1e")
root.title("Noir Dice")
root.geometry("400x350")
root.resizable(False, False)

# ----------------------
# BILDER (MÅSTE EFTER ROOT)
# ----------------------

# statisk d10
img = Image.open(IMG_PATH)
img = img.resize((60, 60), Image.LANCZOS)
dice_img = ImageTk.PhotoImage(img)

# gif frames (säker version)
gif = Image.open(GIF_PATH)
gif_frames = [
    ImageTk.PhotoImage(frame.copy().convert("RGBA").resize((60, 60), Image.LANCZOS))
    for frame in ImageSequence.Iterator(gif)
]

# ⚠️ Viktigt: behåll referenser
root.dice_img = dice_img
root.gif_frames = gif_frames

# ----------------------
# ANIMATION (med stopp)
# ----------------------

animation_running = False

def animate_gif(label, frames, delay=50):
    def update(ind):
        if not animation_running:
            return

        frame = frames[ind]
        label.config(image=frame)

        ind = (ind + 1) % len(frames)
        label.after(delay, update, ind)

    update(0)

# ----------------------
# VISA TÄRNINGAR
# ----------------------

def show_dice_images(r):
    for widget in dice_frame.winfo_children():
        widget.destroy()

    # grundslag
    for d in r["grundslag"]:
        frame = tk.Frame(dice_frame)
        frame.pack(side="left", padx=5)

        tk.Label(frame, image=dice_img).pack()
        tk.Label(frame, text=str(d), font=("Segoe UI", 10, "bold")).pack()

    # extra
    if r["extra"]:
        tk.Label(dice_frame, text="+", font=("Segoe UI", 12)).pack(side="left")

        for d in r["extra"]:
            frame = tk.Frame(dice_frame)
            frame.pack(side="left", padx=5)

            tk.Label(frame, image=dice_img).pack()
            tk.Label(frame, text=str(d), font=("Segoe UI", 10, "bold")).pack()

# ----------------------
# RESULTAT
# ----------------------

def show_result(value):
    global animation_running

    r, total, success = difficulty(value)

    # stoppa animation
    animation_running = False
    gif_label.config(image="")

    show_dice_images(r)

    text = f"Summa: {total}\n\n"
    text += "✅ Lyckat!" if success else "❌ Misslyckat!"

    result_label.config(text=text)

# ----------------------
# STARTA SLAG
# ----------------------

def run_difficulty():
    global animation_running

    try:
        value = int(entry.get())
    except:
        result_label.config(text="Fel värde")
        return

    result_label.config(text="🎲 Rullar...")
    root.update()

    play_dice_sound()

    # ▶ starta animation
    animation_running = True
    animate_gif(gif_label, gif_frames)

    # ⏱ visa resultat efter delay
    root.after(800, lambda: show_result(value))

# ----------------------
# STIL
# ----------------------

style = ttk.Style()
style.theme_use("default")

style.configure(
    "TLabel",
    background="#1e1e1e",
    foreground="#ffffff",
    font=("Segoe UI", 10)
)

style.configure(
    "TButton",
    padding=6,
    font=("Segoe UI", 10)
)

# ----------------------
# GUI LAYOUT
# ----------------------

root.geometry("500x450")

main_frame = tk.Frame(root, bg="#1e1e1e")
main_frame.pack(fill="both", expand=True, padx=20, pady=20)

# Titel
title = ttk.Label(main_frame, text="🎲 NOIR DICE", font=("Segoe UI", 18, "bold"))
title.pack(pady=(0, 20))

# Input-rad
input_frame = ttk.Frame(main_frame)
input_frame.pack(pady=10)

ttk.Label(input_frame, text="Värde:", font=("Segoe UI", 11)).pack(side="left", padx=5)

entry = ttk.Entry(input_frame, width=10, font=("Segoe UI", 11))
entry.pack(side="left", padx=5)

# Knapp
roll_button = ttk.Button(main_frame, text="Slå", command=run_difficulty)
roll_button.pack(pady=15)

# GIF animation
gif_label = tk.Label(main_frame)
gif_label.pack(pady=5)

# Dice display
dice_frame = tk.Frame(main_frame, bg="#1e1e1e")
dice_frame.pack(pady=15)

# Resultat
result_label = tk.Label(
    main_frame,
    text="Resultat visas här",
    bg="#2a2a2a",
    fg="white",
    font=("Segoe UI", 12),
    padx=15,
    pady=15,
    justify="center"
)
result_label.pack(pady=10)

root.mainloop()