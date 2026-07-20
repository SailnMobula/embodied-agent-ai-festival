# Workshop: Vom humanoiden Roboter zum Embodied Agent (AgiBot X2 Ultra)

## Auftrag an den Coding Agenten

Baue eine statische, über GitHub Pages hostbare Übersichtsseite zu diesem Workshop.
Sie dient zwei Zwecken:

1. **Während des Workshops**: Navigationsleiste / roter Faden, von dem aus die Live-Demos
   und interaktiven Bausteine aufgerufen werden.
2. **Nach dem Workshop**: Nachschlagewerk, mit dem Teilnehmende den Ablauf und die
   Konzepte eigenständig nachvollziehen können.

Technisch: statisches HTML/CSS/JS, kein Build-Zwang, keine Server-Komponente.
Deployment über GitHub Pages aus `/docs` oder `gh-pages`.

---

## Rahmenbedingungen

| Punkt      | Wert                                                                    |
| ---------- | ----------------------------------------------------------------------- |
| Dauer      | 45–60 Minuten                                                           |
| Zielgruppe | Allgemeine Bevölkerung, technisches Grundverständnis vorhanden          |
| Vorwissen  | **Kein** Robotics-Know-how, **kein** praktisches Software Engineering   |
| Format     | Vortrag + Live-Demo am echten AgiBot X2 Ultra, gesteuert vom Referenten |
| Lernziel 1 | Verstehen, wie so ein System funktioniert                               |
| Lernziel 2 | Wow-Effekt                                                              |
| Lernziel 3 | Realistische Einschätzung: was geht, was nicht                          |

Durchgehender Begriff über die gesamte Veranstaltung: **Skills**. Der Begriff wird in
Station 1 eingeführt und trägt bis zum Schluss.

---

## Ablauf in 5 Stationen

### Station 1 — Was ist ein KI-Agent? (~10 Min)

Inhalt:

- Die vier Bausteine eines Agenten: **LLM, Memory, Reasoning, Skills**
- Analogie als Einstieg: Skills in der Web-/PC-Welt (File Read, Web Search — bekannt aus
  Coding-Agenten) vs. Skills in der Embodied-Welt (Wahrnehmung, Aktion, Manipulation)
- Kontrast: **Wie werden Roboter heute programmiert?** Kleines Beispiel einer State Machine
- Kernbotschaft: Agenten haben das Potenzial, State Machines und Behavior Trees abzulösen

Benötigt auf der Seite:

- Diagramm der vier Agenten-Bausteine
- Gegenüberstellung Web-Skills ↔ Embodied-Skills (zwei Spalten)
- Visualisierung einer einfachen State Machine (Knoten + Übergänge), idealerweise
  klickbar/animiert, damit der Zustandswechsel sichtbar wird

### Station 2 — Kinematik (~5 Min)

Inhalt: Grundidee Vorwärtskinematik — Gelenkwinkel rein, Position des Endeffektors raus.

Benötigt auf der Seite:

- **Interaktive 2D-Demo**: 2–3 Gelenke über Slider verstellbar, Arm wird live gezeichnet,
  Endeffektor-Position (x, y) wird numerisch angezeigt
- Bewusst minimal halten, keine Denavit-Hartenberg-Formalismen, keine Inverskinematik

### Station 3 — Kameras und Wahrnehmung (~10 Min)

Inhalt:

- Welche Sensorik hat der X2: Kameras, Tiefe, 3D-Punktwolken
- Ein bis zwei Wahrnehmungsmodelle besprechen
- Live: ein Modell, das etwas erkennt (z. B. Personenerkennung)

Benötigt auf der Seite:

- Abschnitt zur Sensorik-Übersicht
- Einbindung/Platzhalter für die Live-Erkennung (Bounding Boxes über Kamerabild)
- Beispielbild einer 3D-Punktwolke

### Station 4 — Skills (~10 Min)

Inhalt: Die einzelnen Fähigkeiten des Roboters vorführen, jede für sich.
3–4 Skills, die später per Function Calling ansteuerbar sind.

Benötigt auf der Seite:

- Skill-Katalog als Karten: Name, Beschreibung in Alltagssprache, Parameter,
  zugehöriges Function-Calling-Schema (aufklappbar)

### Station 5 — Der Agent (Herzstück, ~20 Min)

Inhalt:

- Bestehende Web-Oberfläche: Kontext-Prompt setzen, Skills als Function Calls einhängen,
  Befehle geben
- Steuerung über Realtime API + Function Calling
- Gemeinsam den Agenten live zusammenstecken und laufen lassen
- Beispielauftrag: _"Laufe herum, bis du jemanden siehst. Wenn du eine Person erkennst,
  winke ihr zu."_

Benötigt auf der Seite:

- Erklärung, wie Prompt + Skills + Realtime API zusammenspielen (Ablaufdiagramm)
- Der Beispiel-Prompt im Volltext, kopierbar
- Verweis/Link auf die bestehende Web-Oberfläche
- Rückbezug auf Station 1: derselbe Auftrag als State Machine vs. als Agent — hier
  schließt sich der Kreis

---

## Anforderungen an die Seite

- **Sprache**: English
- **Struktur**: Eine Seite pro Station, plus Übersichtsseite mit Zeitleiste der 5 Stationen
  inkl. Minutenangaben
- **Navigation**: Vor/Zurück zwischen den Stationen, jederzeit zurück zur Übersicht
- **Präsentationstauglich**: große Schrift, hoher Kontrast, funktioniert auf einem Beamer
- **Selbsterklärend**: Wer die Seite nach dem Workshop allein öffnet, versteht den Inhalt
  ohne den Vortrag
- **Interaktive Elemente laufen clientseitig** (Kinematik-Demo, State Machine)
- Kein Fachjargon ohne Erklärung; Begriffe wie Endeffektor, Punktwolke, Function Calling
  bekommen einen Ein-Satz-Klartext daneben

## Offene Punkte, die noch zu klären sind

- Konkrete Auswahl der 3–4 Skills für Station 4
- Welche Wahrnehmungsmodelle in Station 3 genau besprochen werden
- Ob die Live-Kamera-Erkennung in die Seite eingebettet wird oder separat läuft
