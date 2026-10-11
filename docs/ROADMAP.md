# Roadmap

Kleine, überprüfbare Meilensteine. Jeder Meilenstein endet mit einem **auf Hardware geprüften** Ergebnis oder einer dokumentierten Begründung, warum nicht.

```text
M0 ─► M1 ─► M2 ─► M3 ─► M4 ─► M5 ─► M6 ─ ─ ► M7 (optional)
Doku  AMY   Daisy  C++   Reso  PM    Gran    Multi-DSP
      ▲ erste wichtige Fertigstellungsgrenze

Gehäuse (D015), parallel:
      G1 Entwicklergehäuse (M1, Daisy-Platz ab M2) ───► G2 Endgehäuse (nach M4)
```

| M | Titel | Abhängig von | Status |
|---|---|---|---|
| M0 | Projekt-Bootstrap | – | abgeschlossen |
| M1 | Erstes Hardwareinstrument (Tulip + AMYboard) | M0 | **als Nächstes** |
| M2 | Daisy-Kompatibilität | M1 (Parametermodell, GUI) | offen |
| M3 | Erste gemeinsame C++-Engine | M2 (Daisy-Toolchain), ESP-IDF-Build | offen |
| M4 | Erweiterter Resonator-Synth | M3 | offen |
| M5 | Physical Modeling | M4 | offen |
| M6 | Granular Synth | M3 (Profile), Speichermessungen | offen |
| M7 | Multi-DSP-Experimente (optional) | M4 + Neubewertung | optional |
| G1 | Entwicklergehäuse (provisorisch) | M1-Schritt 2 | offen, Teil von M1 |
| G2 | Endgültiges 3D-gedrucktes Gehäuse | M4, G1-Erfahrungen | offen |

---

## M0 – Projekt-Bootstrap ✅

Abgeschlossen am 10.10.2026, Branch `claude/brave-hopper-u0eei2`, Commit `be6a9db8a6521fef3c487e227540784c5300e3dc`.

- [x] Bestandsaufnahme (lokal/Cloud, GitHub, Dokumente, Werkzeuge)
- [x] Repository initialisiert, README, `.gitignore`, `AGENTS.md`
- [x] Dokumentation übernommen bzw. Fehlen dokumentiert (`docs/handovers/README.md`)
- [x] Claude-Ergebnisse konsolidiert, soweit verfügbar (`CLAUDE_REVIEW_2026-10-09.md`)
- [x] Kernbefunde an Primärquellen verifiziert (`research/SOURCE_VERIFICATION_2026-10-10.md`)
- [x] Architekturentscheidungen (`DECISIONS.md`)
- [x] Werkzeuginventur (`DEV_ENVIRONMENT.md`); Inventur des Windows-Hosts steht noch aus
- [x] Roadmap

**Offene Reste aus M0** (blockieren M1 nicht):
- Originaldokumente (Übergaben vom 09.10., Claude-Bericht) ins Repo legen → `docs/handovers/`
- Windows-Werkzeuginventur ausführen (`DEV_ENVIRONMENT.md`, Abschnitt 3)

---

## M1 – Erstes Hardwareinstrument: Tulip + ein AMYboard

**Ziel:** Ein spielbarer Hardware-Synthesizer mit grafischer Bedienung.

Schritte (jeweils einzeln prüfbar):
1. **Hardware-Inventur:** Tulip- und AMYboard-Firmwareversion notieren, Fotos, Revisionen (HARDWARE.md ergänzen).
2. **Strom:** AMYboard über eigenes USB-C oder den RackBrute-Bus (+12 V) versorgen, nicht über den Tulip; Tulip an 1–2-A-Netzteil (HARDWARE.md 2.1, 6.4).
3. **Lokaler Klang:** Auf dem Tulip AMY-KS-Note spielen (`wave=amy.KS`), ohne AMYboard (D018).
4. **Verbindung:** Grove-I²C Tulip → AMYboard-Hostport; `amy.override_send = lambda x: i2c.writeto(0x3f, x)`; Testnote hörbar am AMYboard-Ausgang.
5. **Parametermodell:** `instruments/resonator/params.py` mit 4–6 Parametern (z. B. Damping/Feedback, Brightness/Filter, Attack, Volume).
6. **GUI:** `UIScreen` mit `UISlider`s für diese Parameter (LVGL-Wrapper aus tulipcc).
7. **MIDI:** Noten von Keyboard (Tulip-USB-Host oder TRS-MIDI) → KS-Stimmen auf AMYboard.
8. **Preset:** ein JSON-Preset speichern/laden.
9. **Messung:** maximale stabile KS-Polyphonie auf dem AMYboard; Ergebnis in `docs/research/`.
10. **Entwicklergehäuse (G1):** AMYboard in RackBrute 6U (Versorgung +12 V über Bus), Tulip daneben mit eigenem USB-C-Netzteil; Zugang zu USB, BOOT/RST und SD erhalten (HARDWARE.md §6.4).
11. **Dauertest:** 30 min Spielen/Parameteränderungen ohne Reboot, im Entwicklergehäuse.

**Prüfkriterien (alle erforderlich):**
- [ ] Noten vom MIDI-Keyboard erklingen über das AMYboard.
- [ ] Mindestens 4 Parameter per Touch hörbar veränderbar.
- [ ] Ein Preset lässt sich speichern und nach Neustart laden.
- [ ] 30 min stabiler Betrieb ohne Reboot von Tulip oder AMYboard.
- [ ] Gemessene KS-Polyphonie dokumentiert.
- [ ] Tulip und AMYboard sind im Entwicklergehäuse verschraubt; Kabel zugentlastet; Recovery-Zugänge ohne Zerlegen erreichbar.

**Nicht in M1:** eigene Firmware, eigene DSP-Engine, Daisy, mehrere Presets-Bänke, Visualisierung, CAD-Endgehäuse, eigene Netzteilplatine.

**Risiken:** Stromversorgung/Boot-Loops (Gegenmaßnahme: getrennte Versorgung) · I²C-Stabilität bei hoher Parameterrate (Rate begrenzen, Änderungen bündeln) · AMY-KS klingt zu einfach (akzeptiert, Ausbau in M4) · GUI-Rendering stört Audio auf dem Tulip (Audio läuft auf dem AMYboard, Risiko gering).

---

## M2 – Daisy-Kompatibilität

1. Audrey-Hardware, Seed-Revision und laufende Firmware dokumentieren.
2. Original-Firmware sichern (Auslesen per DFU, sonst Archiv-`.bin` + Hash) – **D012**.
3. Recovery-Verfahren einmal trocken durchspielen.
3a. Daisy/Audrey mechanisch ins Entwicklergehäuse aufnehmen (G1 erweitern), Recovery-Zugang erhalten.
4. Daisy-Toolchain auf dem Windows-Host prüfen (arm-none-eabi-gcc, make, dfu-util).
5. Minimale eigene Firmware: USB-MIDI (libDaisy `MidiUsbHandler`), Note-On/Off, ein einfacher Klang (z. B. DaisySP `StringVoice`), 2–3 Parameter über CC/NRPN.
6. Flash-Budget prüfen: passt in 128 KB oder Bootloader nötig?
7. Tulip-Transport um Daisy-Zuordnung erweitern; gleiche GUI steuert Daisy.

**Prüfkriterien:** Original-Firmware wiederherstellbar · Tulip spielt Noten auf Daisy · Parameter wirken · Audioausgabe sauber.
**Regel:** Keine große Engine portieren, bevor die Verbindung steht.
**Risiken:** Flash-Grenze · USB-Host-Kompatibilität Tulip ↔ Daisy-USB-MIDI (UNGEPRÜFT) · Bedienelemente der Audrey in eigener Firmware neu belegen.

---

## M3 – Erste gemeinsame C++-Engine

1. Einfachen Resonator-Algorithmus wählen (Kandidaten: DaisySP `KarplusString`/`StringVoice`, eigener KS).
2. Plattformneutral in `dsp/common/` (C++17, float, keine Allokation im Callback).
3. Daisy-Build über libDaisy; AMYboard-Build über ESP-IDF mit AMY-Hook (`amy_external_render_hook`).
4. CPU-Last und Speicher auf beiden Plattformen messen; Base/Extended-Profil mit Zahlen füllen.

**Prüfkriterien:** Derselbe Algorithmus klingt auf beiden Plattformen · Messwerte dokumentiert.
**Ausstiegsregel:** Ist die Portierung auf den ESP32-S3 unverhältnismäßig (Toolchain, Fixed-Point, Hook-Integration), Ursachen dokumentieren und gemeinsamen Code begrenzen (D006).
**Risiken:** Eigener AMYboard-Firmware-Build ist der größte Unbekannte des Projekts (UNGEPRÜFT).

---

## M4 – Erweiterter Resonator-Synth
Vorhandene Portierungen nutzen (DaisyExamples `patch/Torus` = Rings-Port, DaisySP `ModalVoice`/`Resonator`), mehrere Resonatormodelle, plattformabhängige Polyphonie, Daisy-Zusatzparameter, GUI und Presets erweitern.
**Prüfkriterium:** musikalisch nutzbares Resonator-Instrument auf mindestens einer Plattform, Presets wechselbar.

## M5 – Physical Modeling
Plucked/Bowed/Blown, Modal, Waveguides; Ziel 8 Stimmen (auf Daisy); CPU/Speicher messen; gemeinsame Parameter/Presets.
**Prüfkriterium:** mindestens zwei Modelle spielbar, Stimmenzahl gemessen und dokumentiert.

## M6 – Granular Synth
Sample-Verwaltung, Grain-Engine (Referenz: DaisyExamples `patch/Nimbus` = Clouds-Port), Modulation, Polyphonie, Wellenformanzeige auf Tulip, Profile (AMYboard ~3 MB SPIRAM vs. Daisy-SDRAM).
**Prüfkriterium:** Sample laden, Grains spielbar, Wellenform sichtbar.

## M7 – Multi-DSP-Experimente (optional, kein Teil von V1.0)
Zwei AMYboards (S/PDIF-Kette, eigenes `override_send`-Voice-Splitting), zwei Daisys, Layering, FX-Modul. **Vor Beginn neu bewerten:** Aufwand, Nutzen, Clock-Sync, Latenz, Mischung.

**Dokumentationsstand 11.10.2026:** [Seed3 Desktop Dev Kit + Seed 1.2 als rein digitaler DSP-Koprozessor](research/DAISY_DIGITAL_COPROCESSOR_OPTION.md) als ausdrücklich **UNGEPRÜFTE spätere Forschungsoption** aufgenommen. Zuerst revisionsrichtige Pin-AF-/KiCad-, Clock- und Versorgungsprüfung; Hardware-/Firmwareversuche erst nach gesondertem Auftrag. M7 wurde nicht begonnen; M1 bleibt der nächste Meilenstein.

---

## G2 – Endgültiges Gehäuse (nach M4)

Erst wenn Modulzahl, Anschlüsse und Stromkonzept aus der Praxis feststehen.
1. Anforderungen aus G1 auswerten (HARDWARE.md §6).
2. Stromkonzept bestätigen: Vorzug ist das ausgebaute RackBrute-6U-Netzteilmodul mit Bus für die DSP-Boards, Tulip mit eigener 5-V-Versorgung; Absicherung, Massekonzept, 5-V-Rückspeiseschutz beim Flashen (HARDWARE.md §6.4).
3. CAD für 3D-Druck, Modulschacht mit Reserveplätzen, Anschlussfeld.
4. Wärmetest im geschlossenen Gehäuse.

**Prüfkriterien:** alle Module sicher befestigt und versorgt · Recovery aller Module ohne Zerlegen möglich · mindestens ein freier Modulplatz · 30-min-Dauertest im geschlossenen Gehäuse.

---

## Projektweite Risiken

| Risiko | Wirkung | Gegenmaßnahme |
|---|---|---|
| Überplanung | Projekt wird nie fertig | AGENTS.md-Hauptregel, M1 zuerst |
| Unbekannter Aufwand eigener AMYboard-Firmware | M3 verzögert | Ausstiegsregel D006; Daisy trägt Extended-Funktionen |
| Firmware-Schaden Audrey | Gerät temporär unbrauchbar | D012, Recovery vorher testen |
| Flash-Grenze Daisy (128 KB) | Engine passt nicht | Bootloader/QSPI-Weg früh klären (M2) |
| Gehäuse wird zu früh perfektioniert | M1 verzögert | G1 bewusst provisorisch; CAD erst G2 |
| Gemeinsame Stromversorgung/Masse im Gehäuse | Reboots, Brummen, Schäden | getrennte geprüfte Netzteile bis G2; Massekonzept vor G2 |
| Fremdlizenzen (MIT/LGPL) | Weitergabe eingeschränkt | Herkunft dokumentieren, DaisySP-LGPL bewusst wählen |
