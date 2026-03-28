# 🎲 Noir Dice

Ett stilrent tärningsverktyg för rollspel, byggt i Python med Tkinter.

------------------------------------------------------------------------

## ✨ Funktioner

### 🎯 Svårighetsslag

-   Slå 2T10 med stöd för exploderande tior
-   Ettor blockerar extraslag
-   Tydlig uträkning av resultat
-   Exceptionellt lyckat och misslyckat stöd

### ⚡ Initiativsystem

-   Lägg till flera deltagare med värden
-   Automatisk beräkning enligt regler
-   Sorterad turordning
-   Markering av aktiv spelare
-   Möjlighet att hoppa över deltagare (checkbox)
-   Loopande turordning

### ⚔️ Motståndsslag

-   Flera deltagare kan delta
-   2T10 + attribut/skicklighetsvärde
-   Automatisk vinnare
-   Utslagsregler:
    -   Högst total
    -   Högst värde
    -   Högsta enskilda tärning
    -   Sudden death (1T10)
-   Exceptionella slag (lyckade/misslyckade)
-   Visuell markering av resultat

------------------------------------------------------------------------

## 🗂️ Projektstruktur

    noir-dice/
    |
    |   .gitignore
    |   gui.py
    |   main.py
    |   README.md
    |   requirements.txt
    |
    +---assets
    |       carcrash.wav
    |       d10.png
    |       dice.wav
    |       fedora.png
    |       godfather.png
    |       noirge.png
    |       sax.wav
    |       spin.gif
    |       wrong.png
    |
    \---noir
        |   dice.py
        |   mechanics.py
        |   __init__.py

------------------------------------------------------------------------

## 🎨 Gränssnitt

-   Noir-inspirerat mörkt tema
-   Enhetlig design genom hela programmet
-   Tydlig visuell feedback

------------------------------------------------------------------------

## 🚧 Status

✅ Kärnfunktioner färdiga\
🧪 Redo för speltest

------------------------------------------------------------------------

## 🔮 Kommande uppdateringar

Framöver kommer fokus ligga på:

-   🎨 Kosmetiska förbättringar\
-   📦 Göra programmet körbart utan CLI (t.ex. .exe)\
-   📱 Eventuell mobilversion

------------------------------------------------------------------------

## ▶️ Starta programmet

1. Installera beroenden:
`pip install -r requirements.txt`
2. Starta programmet:
`py gui.py`

------------------------------------------------------------------------

## 💡 Syfte

Verktyget är designat för att göra spel snabbare, tydligare och mer
stämningsfullt vid spelbordet.

------------------------------------------------------------------------

## 📜 Licens

Öppen källkod.

Fri att använda och bygga vidare på.

Detta projekt är ett hobbyprojekt och inte officiellt kopplat till Noir
eller Helmgast.
