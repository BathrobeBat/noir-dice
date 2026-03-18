# 🎲 Noir Tärningsverktyg

Ett enkelt Python-program med GUI för att slå tärningar enligt reglerna i rollspelet **Noir**.

## ✨ Funktioner

- 🎲 Slår T10 enligt Noirs regelsystem
- 🔁 Maxning (10:or ger extra slag)
- 🚫 Spärr (1:or blockerar maxning)
- 🎞️ Animerad tärningskast (GIF)
- 🔊 Ljudeffekt vid slag
- 🌙 Mörkt tema (dark mode GUI)
- 🖼️ Visuella tärningar

## 🧰 Krav

- Python 3.x
- Pillow

Installera beroenden:

```bash
pip install -r requirements.txt
```

## ▶️ Starta programmet

```bash
python gui.py
```

## 📁 Projektstruktur

```
noir-dice/
│
├── gui.py                # GUI-applikation
├── main.py               # CLI-version (valfri)
├── requirements.txt      # Beroenden
├── assets/
│   ├── dice.wav          # Ljudeffekt
│   ├── d10.png           # Tärningsbild
│   └── spin.gif          # Animation
└── noir/
    ├── __init__.py
    ├── dice.py           # Grundläggande tärningslogik
    └── mechanics.py      # Spelmekanik (slag, regler)
```

## 🧠 Regler (kortfattat)

- Slå 2T10
- Summera resultatet
- Varje 10:a ger en extra tärning (maxning)
- Varje 1:a spärrar en 10:a
- Målet är att nå **20 eller mer** vid svårighetsslag

## 🚀 Planerade funktioner

- ⚔️ Initiativsystem
- 👥 Stöd för flera spelare
- 🎨 Färgkodning (kritiska slag / misslyckanden)
- 📱 Möjlig mobilversion

## 📜 Licens

Detta projekt är ett hobbyprojekt och inte officiellt kopplat till Noir.
