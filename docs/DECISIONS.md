# Architekturentscheidungen

Format: kurz und verbindlich. Änderungen nur durch neue Einträge oder Statuswechsel (`aktiv` → `ersetzt durch Dxxx`), nie durch stilles Umschreiben.

*Nummerierung (10.10.2026):* D001–D015 stammen vom Eigentümer. Die in M0 zusätzlich angelegten Entscheidungen hießen zunächst D015–D017 und wurden auf **D016–D018** verschoben, damit D015 (Gehäuse) der Vorgabe des Eigentümers entspricht.

| ID | Entscheidung | Status | Gilt für |
|---|---|---|---|
| D001 | Hardware-only, keine Desktop-Synthesizer | aktiv | alle |
| D002 | C++17 für eigene native DSP-Engines | aktiv | ab M2/M3 |
| D003 | Tulip als GUI- und Steuerzentrale | aktiv | ab M1 |
| D004 | AMYboard als erste Syntheseplattform | aktiv | M1 |
| D005 | Daisy als erweiterte DSP-Plattform | aktiv | ab M2 |
| D006 | Gemeinsamer DSP-Code, wo sinnvoll | aktiv | ab M3 |
| D007 | Plattformabhängige Leistungsprofile | aktiv | ab M3 |
| D008 | Hardwareunabhängiges Parametermodell | aktiv | ab M1 |
| D009 | Erweiterbarkeit auf mehrere DSP-Module | **langfristiges Ziel, keine Anforderung an V1.0** | M7 (optional) |
| D010 | Unterschiedliche DSP-Rollen und Audio-Routing langfristig möglich | **langfristiges Ziel, keine Anforderung an V1.0** | M7 (optional) |
| D011 | Bestehende Bibliotheken vor Eigenimplementierung | aktiv | alle |
| D012 | Keine Firmwareänderung ohne Backup/Recovery | aktiv | alle |
| D013 | Instrumente nacheinander entwickeln | aktiv | alle |
| D014 | Keine vorzeitige Framework- oder Infrastrukturentwicklung | aktiv | alle |
| D015 | Integriertes, modular erweiterbares Hardwaregehäuse | aktiv (Konzept); Entwicklergehäuse ab M1, CAD/Netzteilplatine **nicht** in M0 | ab M1 |
| D016 | Keine Firmware-Binaries im Git | aktiv | alle |
| D017 | M1 nutzt die Standard-AMYboard-Firmware und AMYs eingebautes Karplus-Strong | aktiv | M1 |
| D018 | M1-Prototyp zuerst gegen Tulips lokale AMY-Engine, dann Umschaltung auf AMYboard | aktiv | M1 |

---

### D001 – Hardware-only
Das Instrument funktioniert ohne Host-Computer. Kein JUCE, kein VST3/AU, keine Desktop-Synthesizer, keine DAW-Integration als Ziel. Der PC dient nur zum Entwickeln, Cross-Compilen, Testen und Flashen.
*Klarstellung:* Vorhandene Werkzeuge wie Tulip Desktop/Web, AMYboard Web oder das AMYboard-VCV-Plugin dürfen als **Entwicklungshilfe** genutzt werden. Host-Unit-Tests für plattformneutralen DSP-Code (ab M3) sind erlaubt. Daraus wird nie ein Produkt.

### D002 – C++17 für eigene native DSP-Engines
Eigene Engines und Firmware in C++17. C-Bibliotheken (AMY) werden direkt eingebunden. Die Tulip-GUI bleibt MicroPython/LVGL; keine C++-Neuentwicklung der Tulip-Firmware.

### D003 – Tulip als GUI- und Steuerzentrale
Tulip: GUI, Instrumentauswahl, Parameter, Presets, MIDI, Kommunikation. Tulip überträgt keine Audiodaten zu den DSP-Modulen.

### D004 – AMYboard als erste Syntheseplattform
Dokumentierte Tulip-Anbindung (I²C `0x3f`), fertige Engine (AMY) mit Karplus-Strong. Kürzester Weg zu einem spielbaren Instrument.

### D005 – Daisy als erweiterte DSP-Plattform
Mehr Rechenleistung und Speicher; DaisySP und Mutable-Portierungen (Torus, Nimbus) verfügbar. Voraussetzung: eigene Firmware mit USB-MIDI (Stock-Audrey hat keine, BELEGT).

### D006 – Gemeinsamer DSP-Code, wo sinnvoll
Algorithmen teilen, Hardwareschicht trennen. Kein Zwang zur Gleichheit: Wenn AMY oder DaisySP direkt passt, wird es direkt genutzt. Ist eine Cross-Portierung unverhältnismäßig, wird der gemeinsame Teil begrenzt und die Begründung dokumentiert.

### D007 – Plattformabhängige Leistungsprofile
Base (AMYboard) und Extended (Daisy). Daisy wird nicht künstlich begrenzt. Grenzwerte entstehen durch Messung. Profile sind **statische** Definitionen.

### D008 – Hardwareunabhängiges Parametermodell
Logische Parameter-IDs; Transportzuordnung je Plattform an einer Stelle. Nicht unterstützte Parameter verursachen keine Fehler und bleiben in Presets erhalten. Siehe PARAMETER_MODEL.md.

### D009 – Erweiterbarkeit auf mehrere DSP-Module (langfristig)
Wird nur architektonisch berücksichtigt (Trennung Instrument/Engine/Modul, Steuerweg ≠ Audioweg). **Keine Implementierung vor M7.**

### D010 – DSP-Rollen und Audio-Routing (langfristig)
Voice-, Layer-, FX- und Hybrid-Rollen sind denkbar. Audio-Routing zwischen Modulen gilt als **ungelöst** (Clock-Sync, Latenz, Mischung). **Keine Implementierung vor M7.**

### D011 – Bestehende Bibliotheken zuerst
Reihenfolge: AMY → DaisySP/libDaisy → DaisyExamples (MI-Portierungen) → `pichenettes/eurorack` → Eigenentwicklung. Eigenentwicklung nur mit dokumentierter Begründung.

### D012 – Keine Firmwareänderung ohne Backup/Recovery
Vor jedem Flash: Ausgangszustand dokumentiert, Backup lokal gesichert, Recovery-Weg beschrieben, Freigabe des Eigentümers. Siehe HARDWARE.md, Abschnitt 4.

### D013 – Instrumente nacheinander
Reihenfolge: Resonator (M1/M4) → Physical Modeling (M5) → Granular (M6). Ein neues Instrument erst, wenn das vorige spielbar ist.

### D014 – Keine vorzeitige Infrastruktur
Keine Engine-Manager, Scheduler, Routing-Matrizen, Plugin-Systeme, eigenen Protokolle, CI/CD-Pipelines oder Build-Frameworks, solange kein konkreter Bedarf belegt ist.

### D015 – Integriertes, modular erweiterbares Hardwaregehäuse
Tulip Synth entsteht als **zusammenhängendes Desktopinstrument**, nicht als lose Sammlung von Platinen.

- **Während der Entwicklung:** Tulip, AMYboard und ggf. Daisy sitzen in einem gemeinsamen, **provisorischen und leicht zugänglichen Entwicklergehäuse** (offene Bauweise, alle Programmier-/Reset-Zugänge erreichbar). Aufbau ab M1.
- **Endgültiges Gehäuse:** 3D-gedruckt, mit Platz für **zusätzliche DSP-Module**, **Audioanschlüsse** und eine **gemeinsame Stromversorgung**.
- **Von Anfang an zu berücksichtigen:** mechanische Befestigung (keine Last auf Steckern/Kabeln), sichere Stromversorgung, Wartungszugang (USB, BOOT/RST, SD-Karte, Firmware-Recovery ohne Zerlegen), Erweiterbarkeit (Modulsteckplätze, Kabelwege, Belüftung).
- **Nicht Bestandteil von M0:** konkrete CAD-Entwicklung und eine eigene Stromversorgungsplatine.
- **Vorzug Stromversorgung (10.10.2026):** ausgebautes RackBrute-6U-Netzteilmodul mit Bus für die Eurorack-fähigen DSP-Boards; Tulip (kein Eurorack-Format) als eigene Einheit mit eigener 5-V-Versorgung. Vor G2 am Gerät zu verifizieren (HARDWARE.md §6.4).

Anforderungen und offene Punkte: HARDWARE.md, Abschnitt 6 „Gehäuse und Mechanik“. Das Gehäuse ist Teil des Instruments, aber **kein Grund, M1 zu verzögern**: Das Entwicklergehäuse darf improvisiert sein (D014).

### D016 – Keine Firmware-Binaries im Git
Kompilierte Images, Herstellerfirmware, Flash-Dumps und Backups werden nicht committet (auch nicht via LFS). `.gitignore` schließt `*.bin`, `*.hex`, `*.elf`, `*.dfu`, `*.uf2` aus. Übernommen aus der Policy von `sscheidl/Custom-Firmware`. Eine spätere Veröffentlichung eigener, getesteter Builds erfolgt nur als separates Release-Artefakt nach ausdrücklicher Freigabe.

### D017 – M1 ohne eigene AMYboard-Firmware
AMY bietet Karplus-Strong als Oszillator-Wellenform `KS` (BELEGT). M1 steuert ausschließlich die vorhandene AMYboard-Firmware über AMY-Wire. Eigene native Firmware (AMY-Hooks) frühestens ab M3. `xcc700`-On-Device-C wird nur für kleine Experimente genutzt (keine floats/structs/`for`, „very alpha“).

### D018 – Erst lokal auf dem Tulip, dann AMYboard
Tulip CC hat eine eigene AMY-Engine mit Karplus-Strong (BELEGT, tulipcc README). GUI und Parametermodell werden zuerst gegen die lokale Engine entwickelt. Die Umschaltung auf das AMYboard erfolgt über `amy.override_send` (I²C). So lassen sich GUI-Fehler und Verbindungsfehler getrennt finden. Das Erfolgskriterium von M1 bleibt der Betrieb **mit** AMYboard.
