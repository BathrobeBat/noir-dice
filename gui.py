import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageSequence
import pygame
from collections import Counter

from noir.mechanics import difficulty

# -----------------------
# INIT
# -----------------------

pygame.mixer.init()

BASE_DIR = os.path.dirname(__file__)
ASSETS = os.path.join(BASE_DIR, "assets")

SOUND_DICE = os.path.join(ASSETS, "dice.wav")
SOUND_SUCCESS = os.path.join(ASSETS, "sax.wav")
SOUND_FAIL = os.path.join(ASSETS, "carcrash.wav")

IMG_D10 = os.path.join(ASSETS, "d10.png")
IMG_GIF = os.path.join(ASSETS, "spin.gif")
IMG_FEDORA = os.path.join(ASSETS, "fedora.png")
IMG_GODFATHER = os.path.join(ASSETS, "godfather.png")
IMG_WRONG = os.path.join(ASSETS, "wrong.png")
IMG_NOIRGE = os.path.join(ASSETS, "noirge.png")

# -----------------------
# STYLE
# -----------------------

BG = "#e6e6e6"
FG = "#111"
BTN_BG = "#111"
BTN_FG = "#7c3aed"
HIGHLIGHT = "#a855f7"  # lila

# -----------------------
# LJUD
# -----------------------

def play_sound(path):
    try:
        pygame.mixer.Sound(path).play()
    except:
        pass

# -----------------------
# ROOT
# -----------------------

root = tk.Tk()
root.title("Noir Dice")
root.geometry("650x700")
root.configure(bg=BG)

root.tk.call('tk', 'scaling', 1.3)

# -----------------------
# LOAD IMAGES
# -----------------------

def load_img(path, size):
    return ImageTk.PhotoImage(Image.open(path).resize(size))

dice_img = load_img(IMG_D10, (100, 100))
fedora_img = load_img(IMG_FEDORA, (60, 60))
godfather_img = load_img(IMG_GODFATHER, (70, 70))
wrong_img = load_img(IMG_WRONG, (70, 70))
noirge_img = load_img(IMG_NOIRGE, (70, 70))

gif = Image.open(IMG_GIF)
gif_frames = [
    ImageTk.PhotoImage(frame.copy().resize((100, 100)))
    for frame in ImageSequence.Iterator(gif)
]

# -----------------------
# HELPERS
# -----------------------

def clear_frame(frame):
    for w in frame.winfo_children():
        w.destroy()

def get_style(value, is_highlight=False):
    if is_highlight:
        return HIGHLIGHT, ("Segoe UI", 20, "bold")
    if value == 10:
        return "#16a34a", ("Segoe UI", 18, "bold")
    if value == 1:
        return "#dc2626", ("Segoe UI", 18, "bold")
    return FG, ("Segoe UI", 16)

# -----------------------
# TABS
# -----------------------

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

tab_difficulty = tk.Frame(notebook, bg=BG)
tab_initiative = tk.Frame(notebook, bg=BG)

notebook.add(tab_difficulty, text="Svårighet")
notebook.add(tab_initiative, text="Initiativ")

# =====================================================
# 🎲 SVÅRIGHET
# =====================================================

title = tk.Label(
    tab_difficulty,
    text="NOIR DICE",
    image=fedora_img,
    compound="left",
    font=("Segoe UI", 28, "bold"),
    bg=BG
)
title.pack(pady=20)

entry = tk.Entry(tab_difficulty, font=("Segoe UI", 18), justify="center")
entry.pack(pady=10)

gif_label = tk.Label(tab_difficulty, bg=BG)
gif_label.pack()

animation_running = False

def animate_gif(i=0):
    if not animation_running:
        return
    gif_label.config(image=gif_frames[i])
    root.after(50, animate_gif, (i+1) % len(gif_frames))

dice_frame = tk.Frame(tab_difficulty, bg=BG)
dice_frame.pack(pady=20)

result_frame = tk.Frame(tab_difficulty, bg=BG)
result_frame.pack(pady=10)

def show_result(value):
    global animation_running

    clear_frame(dice_frame)
    clear_frame(result_frame)

    r, total, success = difficulty(value)

    animation_running = False
    gif_label.config(image="")

    all_dice = r["grundslag"] + r["extra"]

    counts = Counter(all_dice)
    doubles = [k for k, v in counts.items() if v >= 2]
    has_double = len(doubles) > 0

    # -----------------------
    # VISA TÄRNINGAR
    # -----------------------

    def draw_die(parent, d):
        frame = tk.Frame(parent, bg=BG)
        frame.pack(side="left", padx=15)

        tk.Label(frame, image=dice_img, bg=BG).pack()

        is_highlight = d in doubles
        color, font = get_style(d, is_highlight)

        tk.Label(frame, text=str(d), fg=color, bg=BG, font=font).pack()

    for d in r["grundslag"]:
        draw_die(dice_frame, d)

    if r["extra"]:
        tk.Label(dice_frame, text="+", bg=BG, font=("Segoe UI", 20)).pack(side="left")

        for d in r["extra"]:
            draw_die(dice_frame, d)

    # -----------------------
    # RESULTAT
    # -----------------------

    if has_double:
        double_value = doubles[0]

        if total >= 20:
            img = godfather_img
            text = f"EXCEPTIONELLT LYCKAT!"
            sub = f"Dubbel {double_value}"
            play_sound(SOUND_SUCCESS)
        else:
            img = noirge_img
            text = f"EXCEPTIONELLT MISSLYCKAT!"
            sub = f"Dubbel {double_value}"
            play_sound(SOUND_FAIL)

    else:
        sub = ""
        if success:
            img = fedora_img
            text = "Lyckat!"
        else:
            img = wrong_img
            text = "Misslyckat!"

    tk.Label(result_frame, image=img, bg=BG).pack()
    tk.Label(result_frame, text=text, bg=BG, font=("Segoe UI", 18)).pack()

    if sub:
        tk.Label(result_frame, text=sub, bg=BG, font=("Segoe UI", 14, "italic")).pack()

    tk.Label(result_frame, text=f"Summa: {total}", bg=BG, font=("Segoe UI", 16)).pack()

def run():
    global animation_running

    try:
        value = int(entry.get())
    except:
        return

    animation_running = True
    animate_gif()

    play_sound(SOUND_DICE)

    root.after(500, lambda: show_result(value))

tk.Button(
    tab_difficulty,
    text="🎲 Slå",
    command=run,
    bg=BTN_BG,
    fg=BTN_FG,
    font=("Segoe UI", 16, "bold"),
    padx=20,
    pady=10
).pack(pady=20)

# =====================================================
# 🎯 INITIATIV
# =====================================================

players = []
initiative_results = []
current_turn_index = 0

player_frame = tk.Frame(tab_initiative, bg=BG)
player_frame.pack(pady=10)

entry_name = tk.Entry(tab_initiative, font=("Segoe UI", 14))
entry_name.pack()

entry_value = tk.Entry(tab_initiative, font=("Segoe UI", 14))
entry_value.pack()

def add_player():
    name = entry_name.get()
    try:
        value = int(entry_value.get())
    except:
        return

    players.append({"name": name, "value": value})
    entry_name.delete(0, tk.END)
    entry_value.delete(0, tk.END)
    refresh_players()

def remove_player(i):
    players.pop(i)
    refresh_players()

def refresh_players():
    clear_frame(player_frame)

    for i, p in enumerate(players):
        row = tk.Frame(player_frame, bg=BG)
        row.pack(fill="x")

        tk.Label(row, text=f"{p['name']} ({p['value']})", bg=BG).pack(side="left")

        tk.Button(row, text="X", command=lambda i=i: remove_player(i)).pack(side="right")

def roll_initiative():
    global initiative_results, current_turn_index

    results = []

    for p in players:
        r, total, _ = difficulty(p["value"])
        results.append((p["name"], total))

    results.sort(key=lambda x: x[1], reverse=True)

    initiative_results = results
    current_turn_index = 0

    show_initiative_results()
    play_sound(SOUND_DICE)

def show_initiative_results():
    clear_frame(result_frame_initiative)

    for i, (name, value) in enumerate(initiative_results):

        if i == current_turn_index:
            bg_color = "#d4c2ff"
            font = ("Segoe UI", 16, "bold")
        else:
            bg_color = BG
            font = ("Segoe UI", 16)

        tk.Label(
            result_frame_initiative,
            text=f"{i+1}. {name} - {value}",
            bg=bg_color,
            font=font
        ).pack(fill="x", padx=20, pady=2)

def next_turn():
    global current_turn_index

    if not initiative_results:
        return

    current_turn_index = (current_turn_index + 1) % len(initiative_results)
    show_initiative_results()

btn_style = {
    "bg": BTN_BG,
    "fg": BTN_FG,
    "font": ("Segoe UI", 16, "bold"),
    "padx": 20,
    "pady": 10
}

tk.Button(tab_initiative, text="+ Lägg till", command=add_player, **btn_style).pack(pady=10)
tk.Button(tab_initiative, text="🎲 Slå initiativ", command=roll_initiative, **btn_style).pack(pady=10)
tk.Button(tab_initiative, text="➡️ Nästa spelare", command=next_turn, **btn_style).pack(pady=10)

result_frame_initiative = tk.Frame(tab_initiative, bg=BG)
result_frame_initiative.pack(pady=10)

# -----------------------
# START
# -----------------------

root.mainloop()