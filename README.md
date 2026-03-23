# 🎲 Noir Dice

Ett visuellt tärningsverktyg i Python för det svenska rollspelet **Noir**.

Programmet automatiserar tärningsslag enligt Noirs regler och visar resultatet tydligt med grafik, animationer och ljud.

---

## ✨ Funktioner

* 🎲 Slår T10 enligt Noirs regelsystem
* ➕ Hanterar maxning (10:or ger extra slag)
* ⛔ Hanterar spärr (1:or stoppar maxning)
* 🎞️ Animerat tärningskast (GIF)
* 🔊 Ljudfeedback (via `pygame`)
* 🎩 Visuella resultat (fedora, godfather, etc.)
* 🎨 Highlight av viktiga slag (1 & 10, samt dubblar)
* 💥 Exceptionella resultat:

  * Dubbel + ≥ 20 → **Exceptionellt lyckat**
  * Dubbel + < 20 → **Exceptionellt misslyckat**
* 🧠 Visar varför resultatet blev exceptionellt (t.ex. *"Dubbel 7"*)

---

## 🎯 Initiativsystem

* ➕ Lägg till spelare med namn + värde
* 🎲 Slå initiativ för alla spelare
* 📊 Automatisk sortering (högst först)
* ▶️ Växla turordning med “Nästa spelare”
* 🎯 Highlight av aktuell spelare

---

## 📦 Krav

* Python 3.10+
* Pillow
* pygame-ce

Installera beroenden:

```bash
pip install -r requirements.txt
```

---

## ▶️ Starta programmet

```bash
python gui.py
```

---

## 📁 Projektstruktur

```
noir-dice/
│
├── gui.py
├── noir/
│   └── mechanics.py
├── assets/
│   ├── d10.png
│   ├── spin.gif
│   ├── fedora.png
│   ├── godfather.png
│   ├── wrong.png
│   ├── noirge.png
│   ├── dice.wav
│   ├── sax.wav
│   └── carcrash.wav
└── README.md
```

---

## 🎨 Designfilosofi

Fokus på:

* Enkelhet vid spelbordet
* Tydlig visuell feedback
* Noir-känsla (mörk, stilren, tematisk)

---

## 🚀 Framtida idéer

* 📱 Mobilanpassning
* 🎭 Fler visuella teman
* 🎲 Fler Noir-mekanik (t.ex. skador, resurser)

---

## 🧠 Om projektet

Detta är ett hobbyprojekt byggt i Python för att kombinera programmering med rollspel och kreativ UI-design.

---

## 📜 Licens

Öppen källkod.

Fri att använda och bygga vidare på.

Detta projekt är ett hobbyprojekt och inte officiellt kopplat till Noir eller Helmgast.
