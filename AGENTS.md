# AGENTS.md – Verbindliche Regeln für Codex, Claude und andere Agenten

## Wichtigste Projektregel

**Dieses Projekt ist gefährdet, durch übermäßige Architekturplanung niemals fertiggestellt zu werden.**

Funktionierende, spielbare Instrumente haben Vorrang vor theoretisch perfekter Erweiterbarkeit. Skalierbarkeit entsteht durch einfache Schnittstellen und saubere Trennung von Verantwortlichkeiten, **nicht** durch Infrastruktur für Anforderungen, die noch nicht praktisch benötigt werden.

## Vor jeder Arbeit

1. `README.md`, `docs/ROADMAP.md` (aktueller Meilenstein) und `docs/DECISIONS.md` lesen.
2. Bei Hardwarebezug zusätzlich `docs/HARDWARE.md` lesen.
3. Nur am aktuellen Meilenstein arbeiten. Spätere Meilensteine nicht vorziehen.

## Regeln

1. Vor wesentlichen Änderungen die aktuelle Projektdokumentation lesen.
2. GitHub (dieses Repository) ist die zentrale technische Wissensbasis. Erkenntnisse gehören ins Repo, nicht nur in den Chat.
3. Kleine, nachvollziehbare Entwicklungsschritte; ein Thema pro Commit.
4. C++17 für eigene native DSP-Entwicklung. Tulip-GUI in MicroPython/LVGL.
5. Bestehende Bibliotheken und APIs wiederverwenden (AMY, DaisySP, libDaisy, MI-Portierungen).
6. Keine JUCE-, VST3-, AU- oder Desktop-Synthesizer-Projekte.
7. Hardwarezugriffe (Audio-I/O, MIDI, I²C, DMA, Interrupts) vom DSP-Code trennen.
8. Plattformabhängige Optimierungen sind ausdrücklich erlaubt.
9. Daisy nicht künstlich auf das Leistungsniveau des AMYboards beschränken.
10. Parameter und GUI möglichst hardwareunabhängig halten (`docs/PARAMETER_MODEL.md`).
11. Multi-DSP-Erweiterbarkeit berücksichtigen, aber **nicht** vorzeitig implementieren.
12. **Keine Firmware ohne ausdrücklichen Auftrag flashen.**
13. Vor Firmwareänderungen Backup und Recovery dokumentieren (`docs/HARDWARE.md`, Abschnitt Recovery).
14. Keine destruktiven Git-Operationen (kein Force-Push, kein Rewrite veröffentlichter History, kein `reset --hard` auf fremde Arbeit).
15. Keine unnötigen Frameworks, Build-Systeme oder Abhängigkeiten.
16. Tests und Messergebnisse dokumentieren (`docs/research/`, mit Datum, Hardware, Firmwarestand).
17. Fremdlizenzen respektieren; Herkunft übernommenen Codes im Commit und in `docs/REFERENCES.md` nennen.
18. Funktionierende Instrumente haben Vorrang vor architektonischer Perfektion.

## Zusätzliche Repository-Regeln

- **Keine Firmware-Binaries** (`.bin`, `.hex`, `.elf`, `.dfu`, `.uf2`, Flash-Dumps, Backups) committen, auch nicht über LFS. Backups liegen lokal beim Eigentümer (D016).
- **Keine Secrets** (Tokens, WLAN-Passwörter) committen.
- Originaldokumente in `docs/handovers/` werden **nie verändert**. Korrekturen kommen in neue Dateien.
- Aussagen über Hardware kennzeichnen: **BELEGT** (Quelle nennen) / **GESCHÄTZT** / **UNGEPRÜFT**.
- Keine Fakten erfinden. Unbekanntes in `docs/OPEN_QUESTIONS.md` eintragen.
- Andere Repositories (insbesondere `sscheidl/Custom-Firmware`) nicht verändern.
- Gehäuse und Mechanik (D015): Einbauten dürfen Recovery-Zugänge (USB, BOOT/RST, SD) nie verbauen. CAD und eigene Netzteilplatinen nur mit ausdrücklichem Auftrag.

## Definition of Done für einen Arbeitsschritt

- Ergebnis auf echter Hardware geprüft **oder** ausdrücklich als UNGEPRÜFT markiert.
- `docs/ROADMAP.md` (Status) und ggf. `docs/DECISIONS.md` / `docs/OPEN_QUESTIONS.md` aktualisiert.
- Commit mit klarer Nachricht auf dem vorgesehenen Branch.
