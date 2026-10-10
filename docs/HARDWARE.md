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
2. Wiederherstellungs-Image lokal sichern (**nicht** ins Git, D016).
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

## 6. Gehäuse und Mechanik (D015)

Tulip Synth wird ein **zusammenhängendes Desktopinstrument**. In M0 werden nur Anforderungen festgehalten. **Kein CAD und keine eigene Netzteilplatine in M0.**

### 6.1 Zwei Stufen

| Stufe | Wann | Zweck | Bauweise |
|---|---|---|---|
| **Entwicklergehäuse** | ab M1 | Tulip + AMYboard (+ Daisy ab M2) sicher und gemeinsam betreiben, jederzeit umbaubar | provisorisch, offen: Grundplatte mit Abstandsbolzen, Lochraster-/Multiplex-/Acrylplatte oder einfacher 3D-Druck-Rahmen |
| **Endgültiges Gehäuse** | frühestens nach M4 (wenn Modulzahl, Anschlüsse und Stromkonzept aus der Praxis bekannt sind) | geschlossenes Instrument | 3D-gedruckt, modular erweiterbar |

### 6.2 Anforderungen (gelten für beide Stufen)

**Mechanische Befestigung**
- Jede Platine verschraubt (Abstandsbolzen, Befestigungslöcher bzw. Klemmrahmen), nie nur an Kabeln oder Buchsen hängend.
- Steckverbinder (Grove, USB-C, Klinke) ohne mechanische Last; Zugentlastung für alle Kabel.
- Touchscreen des Tulip fest gelagert, damit Bedienung keine Kräfte auf die Platine überträgt.

**Sichere Stromversorgung**
- M1: getrennte 5-V-USB-C-Versorgung für Tulip und AMYboard (Abschnitt 2.1); Mehrport-**Netzteil** zulässig, kein Daten-Hub als Stromquelle.
- Endgehäuse: **eine** gemeinsame Einspeisung (Netzbuchse mit Schalter), Verteilung an alle Module mit Absicherung je Zweig, Verpolschutz, ausreichende Reserve für Zusatzmodule.
- Gemeinsames Massekonzept planen (Brummschleifen, Q-HW-3), Audio- und Stromleitungen getrennt führen.
- Keine Netzspannung (230 V) offen im Entwicklergehäuse; nur geprüfte externe Netzteile.

**Wartungszugang** (ohne Zerlegen erreichbar)
- USB-Anschlüsse aller Module zum Flashen und für die REPL.
- BOOT/RST-Tasten von AMYboard (seitlich, BELEGT) und Daisy Seed; beim Tulip die Flash-/Reset-Möglichkeit.
- MicroSD-Slot des AMYboards (seitlich, BELEGT).
- Recovery nach HARDWARE.md Abschnitt 4 muss im eingebauten Zustand möglich sein; falls nicht, ist das ein Gehäusefehler.

**Erweiterbarkeit**
- Reservierte Steckplätze für weitere DSP-Module (D009, langfristig).
- Kabelwege für I²C/MIDI-Steuerung und für Audio (analog, ggf. S/PDIF).
- Rückseitiges Anschlussfeld mit Reserve-Ausbrüchen für zusätzliche Audio-Ein-/Ausgänge.
- Belüftung/Wärmeabfuhr vorsehen (Erwärmung der Module im geschlossenen Gehäuse UNGEPRÜFT).

### 6.3 Bekannte mechanische Eckdaten

| Komponente | Eckdaten | Status |
|---|---|---|
| AMYboard | 10 HP Eurorack-Breite, Acryl-Frontplatte über Buchsenmuttern befestigt; Front-Panel als 3MF/DXF/SVG/EPS verfügbar | BELEGT (`docs/amyboard/README.md`, `docs/amyboard/modular.md`) |
| AMYboard | USB-C und MicroSD seitlich, I²C-Host und 10-Pin-Strom hinten; bei Rack-Einbau ist USB verdeckt (dann Sketches über TRS-MIDI) | BELEGT |
| AMYboard | Versorgung auch über Eurorack-10-Pin (+12 V) | BELEGT |
| Tulip CC | Gehäusevorlage für Rev. 4r11 als Laserschnitt-Datei `docs/pcbs/tulip4_r11/case.lbrn2` im tulipcc-Repo | BELEGT (Datei vorhanden, Inhalt nicht geprüft) |
| Tulip CC | Maße, Befestigungspunkte, Display-Einbau des eigenen Geräts | UNGEPRÜFT |
| Daisy Seed / Audrey II | Einbau als komplette Audrey oder nur Seed-Modul; Maße und Befestigung | UNGEPRÜFT |

### 6.4 Gestaltungsoption (GESCHÄTZT, keine Festlegung)

Da das AMYboard Eurorack-Format hat und sich über +12 V aus einem Eurorack-Bus versorgen lässt, wäre für das Endgehäuse ein **interner Modulschacht mit Eurorack-Schienen und Eurorack-Busplatine** eine naheliegende Lösung: weitere AMYboards oder Daisy-basierte Module ließen sich ohne neue Mechanik ergänzen, und eine fertige Eurorack-Stromversorgung ersetzt die eigene Netzteilplatine. Zu prüfen sind Bautiefe und der Zugang zu den seitlichen USB-Buchsen. Entscheidung frühestens nach M4.

**+5-V-Schiene:** Die meisten Eurorack-Netzteile und -Busplatinen führen zusätzlich **+5 V** (am 16-Pin-Busstecker). Damit könnten Tulip (~575 mA) und Daisy aus derselben Stromversorgung gespeist werden, und eine eigene 5-V-Verteilung entfiele. Einschränkungen:

| Punkt | Status |
|---|---|
| Nicht jedes Eurorack-Netzteil liefert +5 V; die +5-V-Belastbarkeit ist oft deutlich kleiner als die der ±12-V-Schienen → beim gewählten Netzteil prüfen, Budget mit Reserve (Tulip + Daisy + Zubehör) | GESCHÄTZT, je Netzteil prüfen |
| Das AMYboard nutzt den **10-Pin**-Stecker und damit nur +12 V; die +5-V-Schiene braucht es nicht | BELEGT (README: „10-pin … +12V“) |
| **Rückspeisung:** Hängt der Tulip oder der Daisy an der Bus-5-V und gleichzeitig zum Flashen per USB am PC, liegen zwei 5-V-Quellen parallel. Ob Tulip CC und Daisy Seed das per Diode/Power-Path entkoppeln, ist unbekannt → bis zur Klärung Entkopplung (Schottky-/Ideal-Diode) im Einspeisekabel vorsehen oder Bus-5-V beim Flashen trennen | UNGEPRÜFT (Schaltpläne prüfen) |
| Anschluss Tulip: 5 V über USB-C-Einspeiseadapter oder einen 5-V-Pin der Platine | UNGEPRÜFT (Q-HW-2) |
| Das AMYboard selbst wählt die höchste anliegende Spannung, USB-C und Bus parallel sind dort vorgesehen | BELEGT (README) |

**Kandidaten für fertige Stromversorgungen** (Hinweis Eigentümer; Werte aus Händlerangaben, Stand 10.10.2026, Herstellerseiten in dieser Sitzung nicht erreichbar → vor Kauf am Datenblatt prüfen):

| Gerät | +12 V | −12 V | +5 V | Eingang / Lieferumfang | Preis (Händler) | Bemerkung |
|---|---|---|---|---|---|---|
| 4ms Row Power 45 | 2,0 A max (1,5 A empf.) | 1,4 A max (1,2 A empf.) | 1,5 A max (1,2 A empf.) | 15–20 V DC Hohlstecker 2,1 mm (Laptop-Netzteil, nicht enthalten); 4 HP Modul | ca. 150–165 € / $ | mehrere Einheiten an einem Netzteil verkettbar; Vorgänger Row Power 40 (+5 V 1,5 A) offenbar eingestellt |
| Befaco Trolley Bus | 5 A | 2,5 A | 4 A | 135-W-Netzteil enthalten; Busplatine 423 × 80 × 25 mm, 28 Steckplätze, 2× USB-A (aus +5 V) | ca. 250–285 € / $ | als Paket aus Busplatine + Einspeisung; Einzelkauf der Platine unklar |
| Befaco Powskiff | 1,5 A | 1,3 A | 1 A | – | – | laut Händler eingestellt |

Grobes 5-V-Budget (GESCHÄTZT): Tulip ~0,58 A (BELEGT) + Daisy Seed (UNGEPRÜFT, Messung M2) + Reserve. Mit 1,2 A empfohlener Last ist die Row Power 45 für Tulip + ein Daisy voraussichtlich ausreichend, aber nicht großzügig. Der Trolley Bus hat deutlich mehr Reserve, auch für die USB-A-Ports. Die +12-V-Last je AMYboard ist unbekannt, weil der Regler nicht dokumentiert ist (UNGEPRÜFT, messen).
Weitere Hersteller (z. B. Doepfer, Tiptop, DIY-Bausätze) sind nicht untersucht. Ein Kauf ist erst für G2 nötig; bis dahin reichen die USB-Netzteile.

#### Vorhandene Eurorack-Stromversorgungen (Eigentümer, 10.10.2026)

| Gerät | Anzahl | +12 V | −12 V | +5 V | Quelle / Status |
|---|---|---|---|---|---|
| Arturia RackBrute (Netzteilmodul) | 2 | 1600 mA | 800 mA | **500 mA** | Angaben Eigentümer aus Arturia-Handbuch („Richtwerte“, max. 31,3 W) |
| Frequency Central Routemaster (DIY-Netzteil + Busplatine) | 1 | ca. 500 mA | ca. 500 mA | 7805-Linearregler, Strom nicht dokumentiert | Bauanleitung/Forum: Linearregler 7812/7912/7805 an 12-V-AC-Steckernetzteil; ~500 mA je Schiene bei 1-A-Netzteil, mehr nur mit stärkerem Netzteil und größeren Kühlkörpern; Werte ±12/±15 V per Trimmer einstellbar (GESCHÄTZT, nicht am eigenen Exemplar geprüft) |

**Hinweis zu den RackBrute-Angaben:** Im Handbuchtext stehen zusätzlich 1600 mA auf −12 V und 900 mA auf +5 V. Das widerspricht den Richtwerten. Die Richtwerte ergeben genau die angegebene Maximalleistung (12 V × 1,6 A + 12 V × 0,8 A + 5 V × 0,5 A = 31,3 W) und gelten deshalb hier als verbindlich. Im 6U-RackBrute ist der Strom zusätzlich auf vier getrennte Kreise aufgeteilt; das Budget gilt dann je Kreis anteilig (Aufteilung UNGEPRÜFT).

**Folgerungen (GESCHÄTZT):**
- **Tulip passt nicht an diese +5-V-Schienen.** Er braucht ~575 mA (BELEGT), die RackBrute liefert 500 mA, die Routemaster erzeugt +5 V linear aus der +12-V-Schiene mit kleinem Budget. Der Tulip bleibt an seinem eigenen USB-C-Netzteil.
- **AMYboards an +12 V aus einer RackBrute:** 1,6 A sind für mehrere Boards voraussichtlich reichlich (Verbrauch je Board UNGEPRÜFT, Q-MECH-9).
- **Daisy an +5 V der RackBrute:** voraussichtlich möglich, Verbrauch messen (M2); Rückspeisung beim Flashen über USB beachten (Q-MECH-8).
- **Routemaster:** als DIY-Linearnetzteil mit kleinem Budget nur Reserve, nicht für Tulip oder mehrere Module.
- **Pragmatische Option für G1:** Das AMYboard ist ein 10-HP-Eurorack-Modul. Ist ein RackBrute-Gehäuse vorhanden, kann es dort direkt eingebaut und versorgt werden; der Tulip steht daneben mit eigenem Netzteil. Das kostet nichts zusätzlich. Bei Rack-Einbau ist die seitliche USB-C-Buchse verdeckt (BELEGT, AMYboard-README); für Flashen/REPL also Zugang vorsehen oder Sketches über TRS-MIDI übertragen.
- **Masse:** Tulip (USB-Netzteil) und AMYboard (Rack-Netzteil) sind über Grove-GND verbunden. Auf Brummschleifen achten (Q-HW-3, Q-MECH-5).
