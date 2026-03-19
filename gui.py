import os
import tkinter as tk
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

FEDORA_PATH = os.path.join(BASE_DIR, "assets", "fedora.png")
GODFATHER_PATH = os.path.join(BASE_DIR, "assets", "godfather.png")
WRONG_PATH = os.path.join(BASE_DIR, "assets", "wrong.png")
NOIRGE_PATH = os.path.join(BASE_DIR, "assets", "noirge.png")

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
root.tk.call('tk', 'scaling', root.winfo_fpixels('1i') / 72)
root.resizable(True, True)
root.title("Noir Dice")
root.geometry("700x650")
root.configure(bg="#e6e6e6")

# ----------------------
# BILDER
# ----------------------

def load_icon(path, size=(60, 60)):
    img = Image.open(path).convert("RGBA")
    img = img.resize(size, Image.LANCZOS)
    return ImageTk.PhotoImage(img)

# tärning
img = Image.open(IMG_PATH).convert("RGBA")
img = img.resize((100, 100), Image.LANCZOS)
dice_img = ImageTk.PhotoImage(img)

# gif
gif = Image.open(GIF_PATH)
gif_frames = [
    ImageTk.PhotoImage(frame.copy().convert("RGBA").resize((100, 100), Image.LANCZOS))
    for frame in ImageSequence.Iterator(gif)
]

# ikoner
fedora_img = load_icon(FEDORA_PATH)
godfather_img = load_icon(GODFATHER_PATH)
wrong_img = load_icon(WRONG_PATH)
noirge_img = load_icon(NOIRGE_PATH)

# behåll referenser
root.dice_img = dice_img
root.gif_frames = gif_frames
root.fedora_img = fedora_img
root.godfather_img = godfather_img
root.wrong_img = wrong_img
root.noirge_img = noirge_img

# ----------------------
# ANIMATION
# ----------------------

animation_running = False

def animate_gif(label, frames, delay=50):
    def update(ind):
        if not animation_running:
            return
        label.config(image=frames[ind])
        label.after(delay, update, (ind + 1) % len(frames))
    update(0)

# ----------------------
# LOGIK
# ----------------------

def is_exceptional(r):
    base = r["grundslag"]
    return len(base) >= 2 and base[0] == base[1]

def show_dice_images(r):
    for widget in dice_frame.winfo_children():
        widget.destroy()

    for d in r["grundslag"]:
        frame = tk.Frame(dice_frame, bg="#e6e6e6")
        frame.pack(side="left", padx=20)

        tk.Label(frame, image=dice_img, bg="#e6e6e6").pack()
        tk.Label(frame, text=str(d), bg="#e6e6e6", font=("Segoe UI", 10, "bold")).pack()

    if r["extra"]:
        tk.Label(dice_frame, text="+", bg="#e6e6e6").pack(side="left")

        for d in r["extra"]:
            frame = tk.Frame(dice_frame, bg="#e6e6e6")
            frame.pack(side="left", padx=20)

            tk.Label(frame, image=dice_img, bg="#e6e6e6").pack()
            tk.Label(frame, text=str(d), bg="#e6e6e6", font=("Segoe UI", 10, "bold")).pack()

def show_result(value):
    global animation_running

    r, total, success = difficulty(value)

    animation_running = False
    gif_label.config(image="")

    show_dice_images(r)

    exceptional = is_exceptional(r)

    if success and exceptional:
        icon = godfather_img
        text = "EXCEPTIONELLT LYCKAT!"
    elif success:
        icon = fedora_img
        text = "Lyckat!"
    elif not success and exceptional:
        icon = noirge_img
        text = "EXCEPTIONELLT MISSLYCKAT!"
    else:
        icon = wrong_img
        text = "Misslyckat!"

    result_label.config(
        text=f"Summa: {total}\n\n{text}",
        image=icon,
        compound="top"
    )

def run_difficulty():
    global animation_running

    try:
        value = int(entry.get())
    except:
        result_label.config(text="Fel värde")
        return

    result_label.config(text="🎲 Rullar...", image="")
    play_dice_sound()

    animation_running = True
    animate_gif(gif_label, gif_frames)

    root.after(800, lambda: show_result(value))

# ----------------------
# GUI LAYOUT
# ----------------------

main_frame = tk.Frame(root, bg="#e6e6e6")
main_frame.pack(fill="both", expand=True, padx=20, pady=20)

# titel
title_frame = tk.Frame(main_frame, bg="#e6e6e6")
title_frame.pack(pady=(0, 20))

tk.Label(title_frame, image=fedora_img, bg="#e6e6e6").pack(side="left", padx=10)

tk.Label(
    title_frame,
    text="NOIR DICE",
    font=("Segoe UI", 26, "bold"),
    bg="#e6e6e6",
    fg="black"
).pack(side="left")

# input
input_frame = tk.Frame(main_frame, bg="#e6e6e6")
input_frame.pack(pady=10)

tk.Label(input_frame, text="Värde:", bg="#e6e6e6", font=("Segoe UI", 14)).pack(side="left", padx=5)

entry = tk.Entry(input_frame, width=10, font=("Segoe UI", 14))
entry.pack(side="left", padx=5)

# knapp
roll_button = tk.Button(
    main_frame,
    text="Slå",
    command=run_difficulty,
    bg="#1e1e1e",
    fg="#bb86fc",
    activebackground="#333333",
    relief="flat",
    padx=25,
    pady=12,
    font=("Segoe UI", 14, "bold"),
    cursor="hand2"
)
roll_button.pack(pady=15)

# animation
gif_label = tk.Label(main_frame, bg="#e6e6e6")
gif_label.pack()

# dice
dice_frame = tk.Frame(main_frame, bg="#e6e6e6")
dice_frame.pack(pady=15)

# resultat
result_label = tk.Label(
    main_frame,
    text="Resultat visas här",
    bg="#ffffff",
    fg="black",
    font=("Segoe UI", 16),
    padx=30,
    pady=20,
    justify="center"
)
result_label.pack(pady=10)

root.mainloop()