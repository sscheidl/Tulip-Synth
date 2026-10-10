# Konsolidierung der Claude-Analyse vom 09.10.2026

## 0. Quellenlage (wichtig)

| Dokument | Status |
|---|---|
| `claude/Tulip_Synth_Machbarkeit_Roadmap_2026-10-09.md` | **NICHT VERFÜGBAR** in der Bootstrap-Sitzung |
| AMYboard-Übergabe 09.10.2026 | **NICHT VERFÜGBAR** |
| Daisy-/Audrey-II-Übergabe 09.10.2026 | **NICHT VERFÜGBAR** |
| Masterprompt Rev. 3 (Zusammenfassung der Claude-Ergebnisse, Abschnitte 6.1–6.3) | verfügbar, archiviert in `handovers/` |

Gesucht wurde im Cloud-Container, in `sscheidl/Tulip-Synth` (leer), in `sscheidl/Custom-Firmware` (nur lesend; keine Treffer außer Audrey-Archivinventar) und in den claude.ai-Artifacts des Kontos (keine Treffer). Auf den Windows-Pfad `D:\…` besteht aus der Cloud kein Zugriff.

**Folge:** Dieses Dokument konsolidiert die Claude-Ergebnisse **so, wie der Masterprompt sie zusammenfasst**, und prüft jede Aussage **unabhängig an den Primärquellen** mit denselben Referenzständen (`tulipcc@36e6332`, `amy@69a1469`, `Audrey-II@e5ab799`, `DaisyExamples@259ed82`). Einzelheiten: `research/SOURCE_VERIFICATION_2026-10-10.md`.
Sobald der Originalbericht vorliegt, ist dieses Dokument damit abzugleichen (Q-DOC-1).

## 1. Kernaussagen zu AMYboard (Masterprompt 6.1)

| Aussage | Prüfergebnis |
|---|---|
| I²C über Grove, Adresse `0x3f`, 400 kHz | **BELEGT** (`docs/amyboard/README.md`, Beispielcode) |
| Alternative: AMY-SysEx über MIDI | **BELEGT** (`faq.md`, `amy.override_send = midi.sysex_amy`) |
| ~350 mA Stromaufnahme | **BELEGT** (aus 3,3 V bei Tulip-Versorgung; Tulip selbst ~575 mA) |
| Separates USB-C-Netzteil empfohlen | **BELEGT** (README „Power note“: Boot-Loops des Tulip bei schwacher Versorgung) |
| Standard-AMY unterstützt verschiedene Synthesealgorithmen | **BELEGT**; u. a. Karplus-Strong als Wellenform `KS` |
| `xcc700` eingeschränkt | **BELEGT**: keine floats, structs, `for`, Präprozessor; 8 Slots; „very alpha“ |
| Komplexe Engines brauchen native Firmware | **BELEGT** als Weg (AMY-Hooks); Aufwand **UNGEPRÜFT** |
| AMY-Portierung für Daisy existiert | **BELEGT** (`amy/daisy/amy_daisy.cpp`, `APP_TYPE=BOOT_SRAM`, Block 128, UART-MIDI) |
| AMYboard-Verkettung über I²C/MIDI und S/PDIF | **BELEGT** (`faq.md` „Chaining“); kein eingebautes Voice-Splitting |

## 2. Kernaussagen zu Daisy / Audrey II (Masterprompt 6.2)

| Aussage | Prüfergebnis |
|---|---|
| Stock-Firmware ohne USB-MIDI-Code | **BELEGT** (überhaupt kein MIDI-/USB-Code außerhalb `lib/`) |
| USB-MIDI erfordert angepasste Firmware | **BELEGT** (Folgerung aus oben) |
| Daisy besitzt Stereo-Audiocodec | **BELEGT** (Audrey nutzt `hw.StartAudio` direkt); Codec-Typ revisionsabhängig, **UNGEPRÜFT** |
| 48 kHz, Blockgröße 4 | **BELEGT** (`FeedbackSynth_main.cpp` Z. 9–10) |
| 11 Potis + 1 Schalter | **BELEGT** (10 Klangparameter + Output Volume; Toggle an D14) |
| Ein Audioeingang | **BELEGT** (`IN_L` genutzt) |
| Flash-/Bootloader-Grenzen | **BELEGT** in Teilen: Stock ohne `APP_TYPE` (interner Flash); AMY-Daisy nutzt `BOOT_SRAM` |
| Backup/Recovery vor Änderungen nötig | übernommen als D012 |
| Performance komplexer Engines unbewiesen | **UNGEPRÜFT** (bleibt so bis M2/M4) |
| DSP-Referenzen Torus, Nimbus, `StringVoice`, `ModalVoice`, `Resonator`, `KarplusString` | **BELEGT** vorhanden (DaisyExamples `259ed82`, DaisySP `Source/PhysicalModeling/`) |
| Portierbarkeit nach ESP32-S3 | **UNGEPRÜFT** (M3) |

## 3. Die zehn Befunde aus Abschnitt 5 der Claude-Analyse

Der Masterprompt (6.3) nennt **neun** Themen. Befund 10 ist ohne den Originalbericht unbekannt. Die Originaldokumente bleiben unverändert. Korrekturen stehen hier und in den neuen Projektdokumenten.

| # | Befund | Status | Korrektur / Folge | Korrigierte Fassung in |
|---|---|---|---|---|
| 1 | AMYboard-Übergabe enthält möglicherweise versehentlich die Daisy-Übergabe | **UNGEPRÜFT** (Originale fehlen) | AMYboard-Übergabe aus Primärquellen **rekonstruiert** und als Rekonstruktion gekennzeichnet; Hashvergleich nachholen (Q-DOC-2) | `handovers/AMYboard_Uebergabe_REKONSTRUKTION_2026-10-10.md` |
| 2 | Falsche Aussage: Daisy brauche externen Audiocodec | **Korrektur BELEGT** | Daisy Seed hat einen integrierten Stereo-Codec; Audrey-Stock-Firmware nutzt ihn direkt. Kein externer Codec nötig | `HARDWARE.md` §3 |
| 3 | USB-MIDI-Beschränkungen unzureichend dokumentiert | **BELEGT** | (a) Audrey-Stock: kein MIDI. (b) AMYboard: USB nur Gerät/Gadget, **kein Host**. (c) Tulip: USB-**Host** für Keyboards. (d) Daisy-USB-MIDI nur mit eigener Firmware | `HARDWARE.md` §1–3 |
| 4 | USB-Buchsentypen und Board-Revisionen unklar | teilweise **BELEGT** | AMYboard: USB-C (BELEGT). Daisy Seed: Micro-USB (GESCHÄTZT). Eigene Seed-Revision: Hinweis auf Rev7, **UNGEPRÜFT**. Tulip-Revision **UNGEPRÜFT** | `HARDWARE.md`, Q-HW-2, Q-HW-4 |
| 5 | Audrey-Firmware-Dateinamen uneindeutig | **BELEGT** | README verlinkt `audrey-ii-v3.bin` **und** `audrey-ii.bin`; Archiv hat `audrey-ii-v3.bin` (92 192 B, CRC32 `73655DBD`) | `HARDWARE.md` §3.2, Q-HW-5 |
| 6 | Flash-/Bootloader-Hinweise fehlen | **BELEGT** | STM32H750: 128 KB interner Flash; Stock passt hinein; größere Firmware (AMY-Daisy) braucht `BOOT_SRAM` + Daisy-Bootloader | `HARDWARE.md` §3.3 |
| 7 | Nutzbare Audrey-Bedienelemente nicht beschrieben | **BELEGT** | Tabelle mit 11 Potis + Schalter inkl. Pins | `HARDWARE.md` §3.1 |
| 8 | Unklare Aussagen zu eigenen C-DSP-Erweiterungen | **BELEGT** | Zwei Wege trennen: `xcc700` on-device (stark eingeschränkt, Fixed-Point) vs. native Firmware mit AMY-Hooks (voll, aber eigener Build) | `HARDWARE.md` §2, D016 |
| 9 | Quellenverweise auf DSP-Portierungen fehlen | **BELEGT** | AMY-Daisy, Torus, Nimbus, DaisySP PhysicalModeling mit Commit-Ständen | `REFERENCES.md` |
| 10 | *unbekannt* | **NICHT VERFÜGBAR** | Originalbericht Abschnitt 5 lesen | Q-DOC-3 |

## 4. Zusätzliche Befunde aus der Quellenprüfung (neu, 10.10.2026)

| # | Befund | Status | Bedeutung |
|---|---|---|---|
| Z1 | AMY bietet Karplus-Strong als eingebaute Wellenform `KS` (Abklingen über `feedback`) | BELEGT | M1 braucht keine eigene Engine (D016) |
| Z2 | Tulip CC hat eine eigene lokale AMY-Engine mit KS | BELEGT | GUI kann ohne AMYboard vorentwickelt werden (D017) |
| Z3 | AMYboard: ~3 MB SPIRAM frei für Samples (~30 s mono) | BELEGT | Obergrenze für Granular-Base-Profil (M6) |
| Z4 | AMYboard-CPU-Richtwerte: Juno ~12 %, DX7 ~8 %, PCM ~2 % pro Stimme | BELEGT | Erwartung für Polyphonie; KS-Kosten selbst ungemessen |
| Z5 | AMY-Standard: 44,1 kHz / 256 Samples; auf Daisy 48 kHz / 128 | BELEGT | Latenz und Profilunterschiede |
| Z6 | AMYboard-I²C-Kette: max. ~4 Boards über Tulip-Strom | BELEGT | Relevanz erst M7 |
| Z7 | Display-/I²C-Last auf dem AMYboard kann Audio aushungern | BELEGT (FAQ) | Parameterrate über I²C in M1 begrenzen |
| Z8 | Masterprompt nennt `daisyaudio/DaisyExamples`; geprüft wurde `electro-smith/DaisyExamples`, Commit `259ed82` existiert dort | BELEGT | Referenz-URL vereinheitlicht |
| Z9 | DaisySP trennt LGPL-Module in Submodul `DaisySP-LGPL` | BELEGT | Lizenzwahl bei M4+ beachten |
