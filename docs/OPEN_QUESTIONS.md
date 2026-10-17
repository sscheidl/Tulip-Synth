# Offene Fragen

Format: ID · Frage · warum relevant · wie zu klären · benötigt für.
Erledigte Fragen nicht löschen, sondern mit Antwort und Datum markieren.

## Dokumente und Organisation

| ID | Frage | Klärung | Für |
|---|---|---|---|
| Q-DOC-1 | Wo liegen die Originale `Tulip_AMYboard_Projektuebergabe_2026-10-09.md`, die Daisy-/Audrey-II-Übergabe vom 09.10.2026 und `claude/Tulip_Synth_Machbarkeit_Roadmap_2026-10-09.md`? In dieser Sitzung waren sie nicht zugänglich (Cloud-Container ohne Zugriff auf `D:\…`, nicht in GitHub, nicht als Artifact). | Eigentümer legt sie unverändert in `docs/handovers/` ab; dann `CLAUDE_REVIEW_2026-10-09.md` abgleichen | M0-Rest |
| Q-DOC-2 | Enthält die AMYboard-Übergabe tatsächlich versehentlich die Daisy-Übergabe? | Hashvergleich beider Originale | M0-Rest |
| Q-DOC-3 | Was ist Befund Nr. 10 aus Abschnitt 5 der Claude-Analyse? (Der Masterprompt nennt neun Themen.) | Originalbericht lesen | M0-Rest |
| Q-ORG-1 | Lizenz für dieses Repository (privat; später MIT wäre kompatibel mit AMY, DaisySP, Audrey-II) | Entscheidung Eigentümer | vor Veröffentlichung |
| Q-ORG-2 | Lokales Arbeitsverzeichnis `D:\Eigene Dateien\Eigene Dokumente\Playground\Tulip-Synth`: existiert es bereits mit Inhalten? | Eigentümer prüft vor `git clone` | M0-Rest |

## Hardware

| ID | Frage | Klärung | Für |
|---|---|---|---|
| Q-HW-1 | Firmwareversionen von Tulip CC und AMYboard | **Teilweise beantwortet 17.10.2026:** Tulip nach offiziellem OTA: MicroPython `1.24.0-preview`, Build `82e69df-dirty on 2026-10-14`; siehe research/TULIP_UPDATE_2026-10-17.md. Vorheriger Stand im seriellen Prüfbericht. AMY-Version und AMYboard-Firmware noch offen. | M1 |
| Q-HW-2 | Hardware-Revision des Tulip CC (z. B. v4r11) und USB-Buchsen | Gerät/Platine | M1 |
| Q-HW-3 | Brummschleife bei Grove-Masseverbindung + getrennter USB-Versorgung? | Messung/Hören | M1 |
| Q-HW-4 | Daisy-Seed-Revision, Codec-Typ, USB-Buchse der eigenen Audrey | Platine, Datenblatt Rev7 | M2 |
| Q-HW-5 | Welche Audrey-Firmware läuft (`audrey-ii-v3.bin` oder `audrey-ii.bin`)? Unterschied? | Hash nach Auslesen vergleichen | M2 |
| Q-HW-6 | Lässt sich die Original-Firmware per DFU vom Seed auslesen? | Test mit `dfu-util -U` (nur lesend) nach Freigabe | M2 |
| Q-HW-7 | Erkennt der Tulip-USB-Host ein Daisy-USB-MIDI-Gerät? Oder Verbindung über TRS-MIDI/UART? | Test | M2 |
| Q-HW-8 | Welchen konkreten Bedarf könnte das vorhandene Uno „ARD R3 DIP“ mit ATmega328 als Bedien-/Steuercontroller erfüllen, und ist es dafür geeignet? | Zweck zuerst wählen; dann Board/MCU, Zustand, Pins, Pegel, Versorgung und Timing prüfen; [HARDWARE §7](HARDWARE.md#7-weitere-vorhandene-boards-und-werkzeuge--zweck-und-eignung-getrennt) | bei Bedarf |
| Q-HW-9 | Gibt es einen Zweck für das vorhandene AZ Delivery Nano V3 mit CH340; eignet sich das konkrete Board dafür? | Zweck und Eignung getrennt prüfen: MCU/Revision, Bootloader, USB/Treiber, Pins, Pegel und Timing | bei Bedarf |
| Q-HW-10 | Ist der vorhandene „STM8 und STM32 Programmer ST-LINK V2 01“ für späteres Daisy-Debugging sinnvoll und kompatibel? Eigentümer vermutet keinen Nutzen. | Bedarf getrennt von Eignung prüfen: Variante, Funktion, Software-/Firmwareunterstützung, SWD-Zugang, Pinbelegung und Zielpegel; kein Flashauftrag | M2+, optional |
| Q-HW-11 | Welche FAT32-SD-Karte funktioniert am eigenen AMYboard; besitzt die eigene Tulip-Revision eine SD-Erweiterung? | Revision/Firmware/Kartenmodell notieren, Mount- und Dateilesetest; siehe research/SD_CARDS_2026-10-11.md | M1 bei SD-Bedarf, kein KS-Blocker |
| Q-HW-12 | Ist an der Audrey II ein SD-Sockel vorhanden/nachrüstbar und welche SDMMC-Pins sind zugänglich? Welche längsten Lesepausen entstehen? | Hardware prüfen; später mit passender Firmware messen, keine Stock-Unterstützung voraussetzen | bei Daisy-SD-Bedarf, spätestens M6 |

## Gehäuse und Mechanik (D015)

| ID | Frage | Klärung | Für |
|---|---|---|---|
| Q-MECH-1 | Maße und Befestigungspunkte von Tulip CC, AMYboard und Audrey II/Daisy Seed (eigene Geräte) | Ausmessen, Fotos; tulipcc `case.lbrn2` und AMYboard-Frontplatten-DXF auswerten | G1 |
| Q-MECH-2 | Audrey II komplett einbauen oder nur den Daisy Seed (mit eigener Trägerplatine/Bedienelementen)? | Entscheidung nach M2 | G1/G2 |
| Q-MECH-3 | Bleiben die seitlichen USB-C- und SD-Zugänge des AMYboards in einem Modulschacht erreichbar? | Mechanik-Mockup | G2 |
| Q-MECH-4 | Strombudget mit dem ausgebauten RackBrute-6U-Netzteil (Vorzug): AMYboards an +12 V, Daisy an +5 V, Tulip über eigenes Netzteil oder DC/DC aus +12 V? Reserve für Zusatzmodule? | Stromaufnahme je Modul messen (M1/M2) | G2 |
| Q-MECH-9 | Stromaufnahme eines AMYboards an +12 V (Bus) und eines Daisy Seed an 5 V | Messung mit USB-/Labor-Strommessgerät (M1/M2) | G2 |
| Q-MECH-10 | ~~Welche Eurorack-Netzteile/Gehäuse sind vorhanden?~~ **Beantwortet 10.10.2026:** 2× RackBrute 6U, Netzteilmodul mit Bus herausschraubbar. Die Routemaster wird nicht verwendet. | Eigentümer | erledigt |
| Q-MECH-11 | Passt das AMYboard (Bautiefe inkl. Stecker) in die obere RackBrute-Reihe (~53 mm) oder nur in die untere (~75 mm)? Netzteilmodul: Eingang wirklich 15 V / 3 A extern (ModularGrid), tatsächliche Tiefe (80 mm?), Länge/Anschlüsse des Busses im ausgebauten Zustand, Aufteilung der vier Kreise? Gültige Ausgangswerte (Handbuch-Richtwerte vs. ModularGrid)? | Nachmessen, Handbuch | G1/G2 |
| Q-MECH-8 | Entkoppeln Tulip CC und Daisy Seed eine externe 5-V-Einspeisung von USB-VBUS (Rückspeisung beim Flashen am PC)? | Schaltpläne Tulip (tulipcc `docs/pcbs/`) und Daisy-Seed-Datenblatt | G2 |
| Q-MECH-5 | Massekonzept und Brummschleifen bei gemeinsamer Versorgung und gemeinsamen Audioausgängen | Messung | G2 |
| Q-MECH-6 | Wärmeentwicklung im geschlossenen Gehäuse, Belüftungsbedarf | Temperaturmessung im Dauertest | G2 |
| Q-MECH-7 | Welche Audioanschlüsse soll das Endgerät haben (Stereo-Out, Kopfhörer, Audio-In, Einzelausgänge je Modul, S/PDIF)? | Entscheidung Eigentümer nach M4 | G2 |
| Q-MECH-12 | **UNGEPRÜFT:** Eignet sich die Platine eines USB-Hubs mit externem Netzteil als interne Stromverteilung für bis zu vier Module? Modell/Netzteilwerte, Betrieb ohne Host, Strom je Port/gesamt, Spannung unter Last, Schutzschaltungen, USB-Rückspeisung, Audio-Störungen und Wärme offen. | Eigentümer prüft; Idee vom 11.10.2026, siehe [HARDWARE §6.5](HARDWARE.md#65-idee-usb-hub-platine-mit-externem-netzteil-als-stromverteilung-ungeprüft) | G2 |

## Software / DSP

| ID | Frage | Klärung | Für |
|---|---|---|---|
| Q-SW-1 | Wie viele gleichzeitige KS-Stimmen schafft das AMYboard? | Messung | M1 |
| Q-SW-2 | Welche AMY-Parameter formen den KS-Klang sinnvoll (feedback, Filter, Hüllkurve, Anregung)? | Experiment, AMY-Quellen | M1 |
| Q-SW-3 | Maximale sinnvolle I²C-Parameterrate Tulip → AMYboard ohne Aussetzer? | Messung | M1 |
| Q-SW-4 | Wie aufwendig ist ein eigener AMYboard-Firmware-Build (tulipcc, ESP-IDF-Version, AMY-Hooks)? | Build-Versuch auf Windows-Host | M3 |
| Q-SW-5 | Float vs. Fixed-Point für gemeinsamen DSP-Code auf ESP32-S3 (FPU nur Single-Precision; AMY nutzt S8.23) | Benchmark | M3 |
| Q-SW-6 | Passt eine Daisy-Firmware mit USB-MIDI + DaisySP-Voice in 128 KB internen Flash? | Build, `size` | M2 |
| Q-SW-7 | Lizenzlage DaisySP-LGPL vs. DaisySP (MIT) für spätere Weitergabe | Lizenztexte | M4 |

## Langfristig (M7, nicht dringend)

| ID | Frage |
|---|---|
| Q-LT-1 | Sample-Clock-Synchronisation zwischen mehreren Modulen (S/PDIF als Taktquelle?) |
| Q-LT-2 | Analoges vs. digitales Mischen mehrerer Module |
| Q-LT-3 | Kann ein Daisy Seed in eine AMYboard-S/PDIF-Kette eingebunden werden? |
| Q-LT-4 | **UNGEPRÜFT:** Seed3 Desktop Dev Kit + Seed 1.2 als digitaler DSP-Koprozessor: passen D26/D27/D28 (ggf. D25/D24) einschließlich Pin-AF, SAI-Blöcken und KiCad-Netzen? Welche MUX-/Schalterfunktionen müssen entfallen, umgelegt oder elektrisch getrennt werden; gibt es alternative Pins? |
| Q-LT-5 | **UNGEPRÜFT:** Wie werden Seed3-Codec und SAI2-Link gemeinsam getaktet? Sind DMA, Cache/Puffer, Einweg-/Duplex-Audio, Start/Reset und Langzeit-Synchronisierung ohne Sample-Slips möglich; welche Latenz entsteht? |
| Q-LT-6 | **UNGEPRÜFT:** Welcher bidirektionale Steuerweg, Ereigniszeitbezug und digitales Mixing am Seed3 sind praktikabel? Kann Seed 1.2 ohne Nutzung seines Codecs im Audioweg arbeiten? |
| Q-LT-7 | **UNGEPRÜFT:** Sind Signalpegel, ausgeschalteter Partner, Strombudget und USB-/externe Versorgung beider Seeds rückspeisefrei (auch über GPIO)? Siehe Q-MECH-8. |

Prüfplan für Q-LT-4 bis Q-LT-7: [Daisy-Koprozessor-Forschungsoption](research/DAISY_DIGITAL_COPROCESSOR_OPTION.md), Stand 11.10.2026. Keine davon ist beantwortet; Forschung erst im optionalen M7 nach Neubewertung.
