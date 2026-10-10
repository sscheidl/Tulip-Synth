# Hardware

Stand: 10.10.2026. Quellenstände: `shorepine/tulipcc@36e6332`, `shorepine/amy@69a1469`, `Synthux-Academy/Audrey-II@e5ab799`, `electro-smith/DaisyExamples@259ed82`. Details zur Prüfung: [research/SOURCE_VERIFICATION_2026-10-10.md](research/SOURCE_VERIFICATION_2026-10-10.md).

Kennzeichnung: **BELEGT** / **GESCHÄTZT** / **UNGEPRÜFT**.

## 1. Tulip CC (GUI- und Steuerzentrale)

| Eigenschaft | Wert | Status |
|---|---|---|
| Prozessor | ESP32-S3 | BELEGT (tulipcc README) |
| Display | 1024×600, kapazitiver Multi-Touch | BELEGT |
| RAM | 8,5 MB gesamt, davon ~2 MB für MicroPython | BELEGT |
| Flash | 32 MB, ~24 MB als Dateisystem | BELEGT |
| GUI | LVGL 9 + Tulip-Wrapper (`UIScreen`, `UISlider`, `UIButton` …) | BELEGT (`docs/tulip_api.md`) |
| Lokaler Synth | AMY mit u. a. Karplus-Strong, „120-voice“ | BELEGT (README) |
| MIDI | MIDI In/Out, USB-MIDI **als Host** inkl. Hubs | BELEGT (README; AMYboard-FAQ: „Tulip does USB host“) |
| I²C | Grove/Mabee-Anschluss | BELEGT |
| Stromaufnahme | ~575 mA @ 5 V inkl. Display | BELEGT |
| Hardware-Revision des eigenen Geräts | – | UNGEPRÜFT |
| Installierte Firmware-Version | – | UNGEPRÜFT |

## 2. AMYboard (erste Syntheseplattform)

| Eigenschaft | Wert | Status |
|---|---|---|
| Prozessor | ESP32-S3, MicroPython + AMY | BELEGT (`docs/amyboard/README.md`) |
| Audio | Line In/Out, S/PDIF In/Out, alles Stereo 3,5 mm | BELEGT (README, FAQ) |
| Pegel | DIP-Schalter (4×) Line/Modular | BELEGT |
| AMY-Samplerate / Block | 44,1 kHz / 256 Samples (Standard außerhalb Daisy/Web) | BELEGT (`amy/src/amy.h`) |
| USB | **USB-C**, nur Gerät/Gadget (kein USB-Host) | BELEGT (README, FAQ) |
| I²C front | Grove, für Zubehör (Encoder, OLED) | BELEGT |
| I²C back („host“) | zum Anschluss an Tulip; AMYboard ist dort Slave | BELEGT |
| I²C-Adresse / Takt | `0x3f`, 400 kHz | BELEGT (README-Beispiel `amy.override_send = lambda x: i2c.writeto(0x3f, x)`) |
| Alternative Steuerung | AMY-SysEx über MIDI (`amy.override_send = midi.sysex_amy`) | BELEGT (FAQ) |
| Stromversorgung | USB-C 5 V, Eurorack +12 V oder 3,3 V über I²C-Host-Port; höchste Spannung gewinnt | BELEGT |
| Stromaufnahme | ~350 mA aus 3,3 V bei Versorgung über Tulip | BELEGT |
| Freier Sample-Speicher | ~3 MB SPIRAM (~30 s Mono 44,1 kHz) | BELEGT (FAQ) |
| CPU-Budget (Richtwerte) | Juno-Stimme ~12 %, DX7 ~8 %, PCM ~2 % → ~8 Juno-Stimmen | BELEGT (FAQ) |
| CPU-Kosten Karplus-Strong | nicht dokumentiert | UNGEPRÜFT (Messung in M1) |
| Karplus-Strong | AMY-Wellenform `KS`; Abklingen über `feedback`; Ringpuffer je Oszillator beim ersten Note-On alloziert | BELEGT (`amy/src/oscillators.c`) |
| On-Device-C-DSP (`xcc700`) | „very alpha“; nur `int`/`int16_t`, **keine floats, structs, `for`, Präprozessor**; 8 Slots; S8.23 Fixed-Point | BELEGT (`docs/user_c_dsp.md`) |
| Native Erweiterung | AMY-Hooks `amy_external_render_hook`, `amy_external_bus_postprocess_hook` (erfordern eigene Firmware-Builds) | Hooks BELEGT, eigener AMYboard-Build UNGEPRÜFT |
| Verkettung | Audio über S/PDIF, Steuerung über I²C/MIDI; kein eingebautes Voice-Splitting | BELEGT (FAQ) |

**Wichtig:** Die Grenzen von `xcc700` und der Standard-Firmware sind **nicht** die Grenzen des ESP32-S3. Native C/C++-Engines sind über eigene Firmware-Builds mit AMY-Hooks möglich (Aufwand UNGEPRÜFT).

### 2.1 Stromversorgung in M1 (verbindlich)

- Das AMYboard wird in M1 **über eigenes USB-C-Netzteil** versorgt. Dann nutzt es seine eigenen 5 V statt der 3,3-V-Schiene des Tulip (BELEGT, README: „it uses the highest voltage present“).
- Begründung: Ein am Tulip versorgtes AMYboard zieht ~350 mA zusätzlich zu den ~575 mA des Tulip. Schwache Netzteile, dünne Kabel oder Hubs führen zu **Boot-Loops des Tulip** (BELEGT, README „Power note“).
- Tulip an ein stabiles 1–2-A-Netzteil mit gutem Datenkabel, kein Hub.
- Offen: ob bei gemeinsamer Masse über Grove und separater USB-Versorgung Brummschleifen am Audioausgang entstehen (UNGEPRÜFT).

## 3. Daisy Seed in Synthux Audrey II (erweiterte DSP-Plattform)

| Eigenschaft | Wert | Status |
|---|---|---|
| Prozessor | STM32H750 (Cortex-M7, 480 MHz) | Herstellerangabe (Daisy-Seed-Datenblatt liegt lokal beim Eigentümer); in dieser Prüfung nicht neu nachgelesen |
| Interner Flash | 128 KB | Herstellerangabe (ST); Stock-Firmware ~90 KB passt (BELEGT über Dateigröße) |
| Audiocodec | **auf dem Daisy Seed integriert**, kein externer Codec nötig | BELEGT (Audrey nutzt direkt `hw.StartAudio` über SAI, `FeedbackSynth_main.cpp`) |
| Codec-Typ | revisionsabhängig | UNGEPRÜFT (im Datenblatt der eigenen Revision nachsehen) |
| Board-Revision | Archiv des Eigentümers enthält `ES_Daisy_Seed_Rev7.pdf` und „Daisy Seed Black“-Foto, das ist ein Hinweis, kein Beleg | UNGEPRÜFT |
| USB-Buchse am Seed | Micro-USB | GESCHÄTZT (am Gerät prüfen) |
| Audrey-Samplerate / Block | 48 kHz / **4 Samples** | BELEGT (`FeedbackSynth_main.cpp` Z. 9–10) |
| Audrey-Audioeingang | `IN_L` wird als Eingang genutzt (mono) | BELEGT (`AudioCallback`) |
| Audrey-Ausgang | Stereo `OUT_L`/`OUT_R` mit Limiter | BELEGT |
| MIDI in Audrey-Stock-Firmware | **kein MIDI-/USB-Code** | BELEGT (keine Treffer für `midi`/`usb` außerhalb `lib/`) |
| Build-Ziel der Stock-Firmware | kein `APP_TYPE` gesetzt → libDaisy-Standard (interner Flash) | BELEGT (Makefile), Auswirkung GESCHÄTZT |
| Lizenz Audrey-II | MIT | BELEGT |

### 3.1 Bedienelemente der Audrey II (Stock-Firmware)

BELEGT aus `Source/FeedbackSynthControls.cpp` (11 ADC-Kanäle + 1 Schalter):

| # | Funktion | Daisy-Pin | Simple-Pin |
|---|---|---|---|
| 1 | Frequency | A10 | 40 |
| 2 | Feedback Gain (großer Knopf) | A9 | 39 |
| 3 | Feedback Body | A5 | 35 |
| 4 | Feedback Lowpass | A4 | 34 |
| 5 | Feedback Highpass | A8 | 38 |
| 6 | Reverb Mix | A7 | 37 |
| 7 | Reverb Decay | A6 | 36 |
| 8 | Echo Send | A1 | 31 |
| 9 | Echo Time | A0 | 30 |
| 10 | Echo Feedback | A3 | 33 |
| 11 | Output Volume | A2 | 32 |
| S | Delay-Schalter (Toggle, halbiert/verdoppelt Delayzeit) | D14 | 15 |

### 3.2 Firmware-Dateien (Namensverwirrung)

BELEGT: Die Audrey-II-README verlinkt **zwei verschiedene Dateinamen**:
- „Latest Firmware“: `simple-designer-instruments/official/audrey-ii/audrey-ii-v3.bin`
- Flash-Anleitung Schritt 1: `…/audrey-ii/audrey-ii.bin`

Im lokalen Archiv des Eigentümers liegt `audrey-ii-v3.bin` (92 192 Bytes, CRC32 `73655DBD`, laut Inventar in `sscheidl/Custom-Firmware`). Welche Datei auf dem Gerät läuft, ist UNGEPRÜFT.

### 3.3 Flash, Bootloader und Speicherbudget

- STM32H750 hat nur **128 KB internen Flash**. Die Stock-Firmware (~90 KB) passt hinein (BELEGT über Dateigröße).
- Größere Firmware (z. B. AMY auf Daisy) nutzt `APP_TYPE = BOOT_SRAM` und braucht den **Daisy-Bootloader** (BELEGT, `amy/daisy/Makefile`). Damit ändert sich der Flash-Ablauf (Bootloader zuerst flashen, Anwendung dann über den Bootloader).
- DaisyExamples `patch/Torus` baut mit `-Os` (Größenoptimierung), ein Hinweis auf knappen Flash (GESCHÄTZT).
- Für M2: erst klären, ob die eigene USB-MIDI-Firmware in 128 KB passt oder den Bootloader braucht.

## 4. Backup und Recovery (Pflicht vor jeder Firmwareänderung, D012)

Allgemeine Regeln:
1. Ausgangszustand dokumentieren (Firmware-Version, Datei, Hash, Fotos).
2. Wiederherstellungs-Image lokal sichern (**nicht** ins Git, D015).
3. Wiederherstellungsweg **vor** dem ersten Flash einmal trocken durchgehen.
4. Flashen nur mit ausdrücklicher Freigabe durch den Eigentümer.

| Gerät | Recovery-Weg | Status |
|---|---|---|
| Daisy Seed | Bootloader-Modus + Original-`.bin` per Daisy Web Programmer oder `make program-dfu` | BELEGT (Audrey-README) |
| Daisy Seed | Der STM32-System-DFU-Bootloader liegt im ROM und lässt sich nicht überschreiben, ein dauerhaftes Unbrauchbarmachen per Flash ist daher unwahrscheinlich | GESCHÄTZT (STM32-Allgemeinwissen), am eigenen Gerät UNGEPRÜFT |
| Daisy Seed | Original-Firmware **direkt vom Gerät auslesen** (DFU-Upload) als Backup | UNGEPRÜFT; falls nicht möglich: Archivdatei `audrey-ii-v3.bin` als Referenz |
| AMYboard | Bootloader-Modus (beide Tasten halten, RST zuerst loslassen, dann BOOT) + Web-Upgrader „Upgrade“ (behält Dateien) oder „Fully erase and re-flash“ | BELEGT (`docs/amyboard/firmware.md`), am Gerät UNGEPRÜFT |
| AMYboard | Vor jedem Upgrade: Sketches/Dateien von `/user/` sichern (Upgrade-Optionen können Dateien löschen) | GESCHÄTZT |
| Tulip CC | Flashing-Anleitung `docs/tulip_flashing.md` | BELEGT, UNGEPRÜFT am Gerät |

In M1 wird **keine** Firmware geflasht. Ein offizielles AMYboard- oder Tulip-Update wäre nur nach Freigabe zulässig.

## 5. Verkabelung für M1

```text
[Netzteil 5V 1–2A]──USB-C──[Tulip CC]──Grove I²C──[AMYboard: back "host"/tulip port]
                              │                        │
                         (MIDI-Keyboard            [eigenes USB-C-Netzteil]
                          an Tulip USB-Host            │
                          oder TRS-MIDI)          Line Out 3,5 mm ─► Mixer/Kopfhörer
```

DIP-Schalter am AMYboard für Line-Pegel: alle 4 auf **OFF** (BELEGT, README).
