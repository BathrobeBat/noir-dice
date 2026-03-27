import tkinter as tk
from tkinter import ttk
import random
from PIL import Image, ImageTk
import pygame

BG = "#1a1a1a"
FG = "#bb00ff"
ACCENT = "#b30000"
GOLD = "#d4af37"
PURPLE = "#bb00ff"
RED = "#ff4444"
GREEN = "#00cc66"

# -------------------------
# UI HELPERS
# -------------------------
def NLabel(parent, **kwargs):
    if "fg" not in kwargs:
        kwargs["fg"] = FG
    if "bg" not in kwargs:
        kwargs["bg"] = BG
    return tk.Label(parent, **kwargs)

pygame.mixer.init()

root = tk.Tk()
root.title("Noir Dice")
root.geometry("900x700")
root.tk.call('tk', 'scaling', 1.3)

# -------------------------
# ASSETS
# -------------------------
def load_img(path, size=(120, 120)):
    img = Image.open(f"assets/{path}")
    img = img.resize(size)
    return ImageTk.PhotoImage(img)

spin_frames = []
spin = Image.open("assets/spin.gif")

try:
    while True:
        frame = spin.copy().resize((120, 120))
        spin_frames.append(ImageTk.PhotoImage(frame))
        spin.seek(len(spin_frames))
except EOFError:
    pass

dice_img = load_img("d10.png")
fedora_img = load_img("fedora.png", (80, 80))
godfather_img = load_img("godfather.png", (100, 100))
wrong_img = load_img("wrong.png", (100, 100))
noirge_img = load_img("noirge.png", (100, 100))

# -------------------------
# SOUND
# -------------------------
def play_sound(file):
    try:
        pygame.mixer.music.load(f"assets/{file}")
        pygame.mixer.music.play()
    except:
        pass

def play_dice_sound():
    play_sound("dice.wav")

# -------------------------
# GAME LOGIC
# -------------------------
def roll_d10():
    return random.randint(1, 10)

def difficulty(value):
    rolls = [roll_d10(), roll_d10()]
    extra = []

    # ❗ kolla om det finns en etta
    has_one = 1 in rolls

    # ❗ bara slå extraslag om INGEN etta finns
    if not has_one:
        for r in rolls:
            if r == 10:
                extra.append(roll_d10())

    total = sum(rolls) + sum(extra) + value

    return {
        "rolls": rolls,
        "extra": extra,
        "total": total,
        "success": total >= 20   # ← din regel
    }

def is_exceptional(rolls, total):
    if len(rolls) >= 2 and rolls[0] == rolls[1]:
        if total >= 20:
            return "success"
        else:
            return "fail"
    return None

# -------------------------
# HELPERS
# -------------------------
def clear_frame(frame):
    for w in frame.winfo_children():
        w.destroy()

def highlight_color(rolls):
    if len(rolls) >= 2 and rolls[0] == rolls[1]:
        return "#d4af37"  # guld
    return None

def animate_dice(label, frame_index=0):
    if not label.winfo_exists():
        return

    frame = spin_frames[frame_index]
    label.config(image=frame)
    label.image = frame

    next_frame = (frame_index + 1) % len(spin_frames)
    root.after(50, lambda: animate_dice(label, next_frame))

# -------------------------
# SVÅRIGHET
# -------------------------
def build_sv_tab(tab):
    frame = tk.Frame(tab, bg=BG)
    frame.pack(expand=True, fill="both")

    NLabel(frame, image=fedora_img, bg=BG).pack(pady=10)
    NLabel(frame, text="NOIR DICE", font=("Segoe UI", 26, "bold"), bg=BG).pack()

    entry = tk.Entry(frame, font=("Segoe UI", 18), justify="center")
    entry.pack(pady=20)

    dice_frame = tk.Frame(frame, bg=BG)
    dice_frame.pack()

    result_frame = tk.Frame(frame, bg=BG)
    result_frame.pack(pady=20)

    def roll():
        clear_frame(dice_frame)
        clear_frame(result_frame)

        labels = []
        for _ in range(2):
            lbl = NLabel(dice_frame, bg=BG)
            lbl.pack(side="left", padx=15)
            labels.append(lbl)

        for lbl in labels:
            animate_dice(lbl)

        play_dice_sound()

        root.after(800, show_result)

    def show_result():
        clear_frame(dice_frame)
        clear_frame(result_frame)

        value = int(entry.get())
        r = difficulty(value)

        rolls = r["rolls"]
        extra = r["extra"]
        total = r["total"]

        # visa tärningar
        highlight = highlight_color(rolls)

        has_one = 1 in rolls

        for d in rolls:

            # 🎨 färglogik
            if d == 1:
                color = "red"
            elif d == 10 and not has_one:
                color = "green"
            else:
                color = "#bb00ff"

            f = tk.Frame(dice_frame, bg="#1a1a1a", bd=2, relief="solid")
            f.pack(side="left", padx=15)

            NLabel(f, image=dice_img, bg="#1a1a1a").pack()

            NLabel(
                f,
                text=str(d),
                fg=color,
                bg="#1a1a1a",
                font=("Segoe UI", 14, "bold")
            ).pack()

            if d == 10 and has_one:
                NLabel(
                    f,
                    text="BLOCKED",
                    fg="red",
                    bg="#1a1a1a",
                    font=("Segoe UI", 8, "bold")
                ).pack()
        
        if extra:
            NLabel(dice_frame, text="+", font=("Segoe UI", 18), bg=BG).pack(side="left")

            for d in extra:
                f = tk.Frame(dice_frame, bg="#1a1a1a", bd=2, relief="solid")
                f.pack(side="left", padx=10)

                NLabel(f, image=dice_img, bg="#1a1a1a").pack()
                NLabel(
                    f,
                    text=str(d),
                    fg="green",
                    bg="#1a1a1a",
                    font=("Segoe UI", 14, "bold")
                ).pack()


        # breakdown
        rolls_str = " + ".join(str(d) for d in rolls)
        extra_str = " + ".join(str(d) for d in extra) if extra else "0"

        NLabel(
            result_frame,
            text=f"Tärningar: {rolls_str}  |  Bonus: {extra_str}  |  Värde: {value}\nTotalt: {rolls_str} + {extra_str} + {value} = {total}",
            font=("Segoe UI", 12),
            bg=BG,
            fg=FG,
            justify="center"
        ).pack(pady=10)

        ex = is_exceptional(rolls, total)

        if rolls[0] == rolls[1]:
            NLabel(
                result_frame,
                text=f"Dubbel {rolls[0]}",
                fg=GOLD,
                font=("Segoe UI", 14, "bold"),
                bg=BG
            ).pack()

        if 1 in rolls:
            NLabel(
                result_frame,
                text="⚠️ 1:a blockerar extraslag",
                fg="red",
                font=("Segoe UI", 12, "italic")
            ).pack()

        if ex == "success":
            NLabel(result_frame, image=godfather_img, bg=BG).pack()
            NLabel(result_frame, text="EXCEPTIONELLT LYCKAT!", fg="green", font=("Segoe UI", 18)).pack()
            NLabel(result_frame, text=f"Dubbel {rolls[0]}").pack()
            play_sound("sax.wav")

        elif ex == "fail":
            NLabel(result_frame, image=noirge_img, bg=BG).pack()
            NLabel(result_frame, text="EXCEPTIONELLT MISSLYCKAT!", fg="red", font=("Segoe UI", 18)).pack()
            NLabel(result_frame, text=f"Dubbel {rolls[0]}").pack()
            play_sound("carcrash.wav")

        else:
            if r["success"]:
                NLabel(result_frame, image=fedora_img, bg=BG).pack()
                NLabel(result_frame, 
                         text="Lyckat!", 
                         fg="green",
                         bg=BG).pack()
            else:
                NLabel(result_frame, image=wrong_img, bg=BG).pack()
                NLabel(result_frame, 
                         text="Misslyckat!", 
                         fg="red",
                         bg=BG).pack()

    tk.Button(
        frame,
        text="🎲 Slå",
        font=("Segoe UI", 16),
        bg="#000000",
        fg="#bb00ff",
        activebackground="#222222",
        padx=20,
        pady=10,
        command=roll
    ).pack(pady=20)

# -------------------------
# INITIATIV
# -------------------------
def build_init_tab(tab):
    frame = tk.Frame(tab, bg=BG)
    frame.pack(expand=True, fill="both")

    # ========================
    # STATE
    # ========================
    players = []
    current_turn = 0
    turn_rows = []
    active_vars = []

    # ========================
    # HEADER
    # ========================
    NLabel(frame, image=fedora_img, bg=BG).pack(pady=10)
    NLabel(frame, text="INITIATIV", font=("Segoe UI", 26, "bold"), bg=BG).pack(pady=(0, 10))

    # ========================
    # INPUT
    # ========================
    input_frame = tk.Frame(frame, bg=BG)
    input_frame.pack(pady=10)

    name_entry = tk.Entry(input_frame, font=("Segoe UI", 14), width=15)
    name_entry.pack(side="left", padx=5)

    value_entry = tk.Entry(input_frame, font=("Segoe UI", 14), width=5)
    value_entry.pack(side="left", padx=5)

    def add_player():
        name = name_entry.get()
        try:
            value = int(value_entry.get())
        except:
            return

        if name:
            players.append({"name": name, "value": value})
            name_entry.delete(0, tk.END)
            value_entry.delete(0, tk.END)
            refresh_players()

    tk.Button(
        frame,
        text="+ Lägg till",
        command=add_player,
        bg="#000",
        fg=FG,
        font=("Segoe UI", 12),
        relief="solid"
    ).pack(pady=10)

    # ========================
    # PLAYER LIST
    # ========================
    player_frame = tk.Frame(frame, bg=BG)
    player_frame.pack()

    def refresh_players():
        for w in player_frame.winfo_children():
            w.destroy()

        for i, p in enumerate(players):
            row = tk.Frame(player_frame, bg=BG)
            row.pack()

            NLabel(row, text=f"{p['name']} ({p['value']})").pack(side="left")

            tk.Button(
                row,
                text="X",
                bg="#000",
                fg=FG,
                relief="solid",
                command=lambda i=i: remove_player(i)
            ).pack(side="left", padx=5)

    def remove_player(i):
        players.pop(i)
        refresh_players()

    # ========================
    # RESULT FRAME
    # ========================
    result_frame = tk.Frame(frame, bg=BG)
    result_frame.pack(pady=20)

    # ========================
    # TURN SYSTEM
    # ========================
    def highlight_turn():
        for i, row in enumerate(turn_rows):
            if not active_vars[i].get():
                row.config(bg="#111111")
            elif i == current_turn:
                row.config(bg="#3a0a4a")
            else:
                row.config(bg="#1a1a1a")

    def next_turn():
        nonlocal current_turn

        active_indices = [i for i, v in enumerate(active_vars) if v.get()]
        if not active_indices:
            return

        if current_turn not in active_indices:
            current_turn = active_indices[0]
        else:
            pos = active_indices.index(current_turn)
            current_turn = active_indices[(pos + 1) % len(active_indices)]

        highlight_turn()

    # ========================
    # INIT ROLL
    # ========================
    def roll_init():
        nonlocal current_turn

        for w in result_frame.winfo_children():
            w.destroy()

        if not players:
            return

        play_dice_sound()

        results = []
        active_vars.clear()
        turn_rows.clear()
        current_turn = 0

        for p in players:
            r = difficulty(p["value"])
            ex = is_exceptional(r["rolls"], r["total"])

            if ex == "success":
                init_value = r["total"] * 2
            elif ex == "fail":
                init_value = 1
            elif r["success"]:
                init_value = r["total"]
            else:
                init_value = max(r["rolls"])

            results.append({
                "name": p["name"],
                "total": init_value,
                "raw_total": r["total"],
                "rolls": r["rolls"],
                "extra": r["extra"],
                "value": p["value"]
            })

        results.sort(key=lambda x: x["total"], reverse=True)

        # ========================
        # VISA RESULTAT
        # ========================
        for i, r in enumerate(results, start=1):
            row = tk.Frame(result_frame, bg="#1a1a1a", bd=2, relief="solid")
            row.pack(fill="x", pady=5)

            turn_rows.append(row)

            var = tk.BooleanVar(value=True)
            active_vars.append(var)

            tk.Checkbutton(
                row,
                variable=var,
                bg="#1a1a1a",
                selectcolor="#000",
                activebackground="#1a1a1a",
                highlightthickness=0
            ).pack(side="left", padx=5)

            name_text = f"{i}. {r['name']} ({r['total']})"

            NLabel(
                row,
                text=name_text,
                font=("Segoe UI", 14, "bold"),
                bg="#1a1a1a"
            ).pack(side="left", padx=10)

            rolls_str = " + ".join(str(d) for d in r["rolls"])
            extra_str = " + ".join(str(d) for d in r["extra"]) if r["extra"] else "0"

            calc = f"{rolls_str} + {extra_str} + {r['value']} → {r['total']}"

            NLabel(
                row,
                text=calc,
                font=("Segoe UI", 12),
                bg="#1a1a1a"
            ).pack(side="right", padx=10)

        highlight_turn()

    # ========================
    # BUTTONS
    # ========================
    tk.Button(
        frame,
        text="🎲 Slå initiativ",
        command=roll_init,
        font=("Segoe UI", 16),
        bg="#000",
        fg=FG,
        relief="solid"
    ).pack(pady=20)

    tk.Button(
        frame,
        text="▶ Nästa tur",
        command=next_turn,
        font=("Segoe UI", 14),
        bg="#000",
        fg=FG,
        relief="solid"
    ).pack(pady=10)

# -------------------------
# MOTSTÅND
# -------------------------
def build_resist_tab(tab):
    frame = tk.Frame(tab, bg=BG)
    frame.pack(expand=True, fill="both")

    participants = []

    # ========================
    # HEADER
    # ========================
    NLabel(frame, image=fedora_img, bg=BG).pack(pady=10)
    NLabel(frame, text="MOTSTÅND", font=("Segoe UI", 26, "bold"), bg=BG).pack(pady=(0, 10))

    # ========================
    # INPUT
    # ========================
    input_frame = tk.Frame(frame, bg=BG)
    input_frame.pack(pady=10)

    name_entry = tk.Entry(input_frame, font=("Segoe UI", 14), width=15)
    name_entry.pack(side="left", padx=5)

    value_entry = tk.Entry(input_frame, font=("Segoe UI", 14), width=5)
    value_entry.pack(side="left", padx=5)

    def add_participant():
        name = name_entry.get()
        try:
            value = int(value_entry.get())
        except:
            return

        if name:
            participants.append({"name": name, "value": value})
            name_entry.delete(0, tk.END)
            value_entry.delete(0, tk.END)
            refresh_list()

    tk.Button(
        frame,
        text="+ Lägg till",
        command=add_participant,
        bg="#000",
        fg=FG,
        font=("Segoe UI", 12),
        relief="solid"
    ).pack(pady=10)

    # ========================
    # LISTA
    # ========================
    list_frame = tk.Frame(frame, bg=BG)
    list_frame.pack()

    def refresh_list():
        for w in list_frame.winfo_children():
            w.destroy()

        for i, p in enumerate(participants):
            row = tk.Frame(list_frame, bg=BG)
            row.pack()

            NLabel(row, text=f"{p['name']} ({p['value']})").pack(side="left")

            tk.Button(
                row,
                text="X",
                bg="#000",
                fg=FG,
                relief="solid",
                command=lambda i=i: remove_participant(i)
            ).pack(side="left", padx=5)

    def remove_participant(i):
        participants.pop(i)
        refresh_list()

    # ========================
    # RESULTAT
    # ========================
    result_frame = tk.Frame(frame, bg=BG)
    result_frame.pack(pady=20)

    # ========================
    # LOGIK
    # ========================
    def roll_resist():
        for w in result_frame.winfo_children():
            w.destroy()

        if len(participants) < 2:
            return

        play_dice_sound()

        results = []

        for p in participants:
            rolls = [roll_d10(), roll_d10()]
            total = sum(rolls) + p["value"]

            results.append({
                "name": p["name"],
                "value": p["value"],
                "rolls": rolls,
                "total": total,
                "exceptional": rolls[0] == rolls[1]
            })

        # ========================
        # SORTERING + TIE BREAK
        # ========================
        def sort_key(r):
            return (
                r["total"],
                r["value"],
                max(r["rolls"])
            )

        results.sort(key=sort_key, reverse=True)

        winner = results[0]

        # ========================
        # SUDDEN DEATH
        # ========================
        if len(results) >= 2:
            a = results[0]
            b = results[1]

            if (
                a["total"] == b["total"]
                and a["value"] == b["value"]
                and max(a["rolls"]) == max(b["rolls"])
            ):
                while True:
                    a_roll = roll_d10()
                    b_roll = roll_d10()

                    if a_roll != b_roll:
                        winner = a if a_roll > b_roll else b
                        break

                NLabel(
                    result_frame,
                    text=f"⚔️ Sudden death: {a_roll} vs {b_roll} → {winner['name']} vinner!",
                    fg="gold",
                    font=("Segoe UI", 14, "bold"),
                    bg=BG
                ).pack(pady=10)

        # ========================
        # VISA RESULTAT
        # ========================
        for i, r in enumerate(results, start=1):

            # 🎨 basfärg
            bg_color = "#1a1a1a"

            # 🟣 vinnare
            if r == winner:
                bg_color = "#3a0a4a"

            # 🟢 exceptionellt lyckat
            if r["exceptional"] and r == winner:
                bg_color = "#003300"

            # 🔴 exceptionellt misslyckat
            if r["exceptional"] and r != winner:
                bg_color = "#330000"

            row = tk.Frame(result_frame, bg=bg_color, bd=2, relief="solid")
            row.pack(fill="x", pady=5)

            name_text = f"{i}. {r['name']} ({r['total']})"

            NLabel(
                row,
                text=name_text,
                font=("Segoe UI", 14, "bold"),
                bg=bg_color
            ).pack(side="left", padx=10)

            # ✨ exceptionell text
            if r["exceptional"]:
                if r == winner:
                    NLabel(
                        row,
                        text="✨ Exceptionellt lyckat!",
                        fg="green",
                        font=("Segoe UI", 12, "bold"),
                        bg=bg_color
                    ).pack(side="left", padx=10)
                else:
                    NLabel(
                        row,
                        text="💀 Exceptionellt misslyckat!",
                        fg="red",
                        font=("Segoe UI", 12, "bold"),
                        bg=bg_color
                    ).pack(side="left", padx=10)

            rolls_str = " + ".join(str(d) for d in r["rolls"])
            calc = f"{rolls_str} + {r['value']} → {r['total']}"

            NLabel(
                row,
                text=calc,
                font=("Segoe UI", 12),
                bg=bg_color
            ).pack(side="right", padx=10)

    # ========================
    # BUTTON
    # ========================
    tk.Button(
        frame,
        text="⚔️ Slå motstånd",
        command=roll_resist,
        font=("Segoe UI", 16),
        bg="#000",
        fg=FG,
        relief="solid"
    ).pack(pady=20)

# -------------------------
# TABS
# -------------------------
tab_control = ttk.Notebook(root)

tab_sv = tk.Frame(tab_control)
tab_init = tk.Frame(tab_control)
tab_resist = tk.Frame(tab_control)

tab_control.add(tab_sv, text="Svårighet")
tab_control.add(tab_init, text="Initiativ")
tab_control.add(tab_resist, text="Motstånd")

tab_control.pack(expand=1, fill="both")

build_sv_tab(tab_sv)
build_init_tab(tab_init)
build_resist_tab(tab_resist)

root.mainloop()