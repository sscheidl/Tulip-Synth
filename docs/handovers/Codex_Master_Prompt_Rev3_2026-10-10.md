# TULIP SYNTH
## Codex Master Prompt – Revision 3
### Projektinitialisierung, skalierbare Architektur und pragmatische Entwicklungsplanung

**Stand:** 10.10.2026  
**Auftrag:** Milestone 0 – Repository, Dokumentation und Architektur  
**Zielplattformen:** Tulip CC, AMYboard (ESP32-S3), Daisy Seed (STM32H750)  
**Entwicklung:** C++17 für native DSP-Engines und Firmware  
**Grundsatz:** Groß denken, klein bauen.

---

# 1. Projektidee

Wir entwickeln mit **Tulip Synth** eine offene, experimentelle Hardware-Synthesizer-Plattform.

Ein Tulip CC mit Touchscreen übernimmt die grafische Bedienoberfläche, Presets, Parametersteuerung und Kommunikation.

Die eigentliche Klangerzeugung erfolgt auf externen DSP-Modulen:

- AMYboard mit ESP32-S3
- Daisy Seed, zunächst in der vorhandenen Synthux Audrey II
- Langfristig möglicherweise mehrere Module unterschiedlicher Art

Unser erstes Ziel ist ein einzelnes funktionierendes Hardwareinstrument.

Langfristig möchten wir eine flexible, skalierbare Architektur entwickeln, die unterschiedliche Syntheseverfahren, DSP-Leistungsstufen und mehrere Prozessoren unterstützt.

Als konzeptionelles Vorbild kann die modulare DSP-Architektur der früheren Creamware-SCOPE-Systeme dienen.

**Wichtig: Das ist eine langfristige Vision, kein Implementierungsauftrag für eine vollständige modulare DSP-Workstation.**

## 1.1 Die drei geplanten Instrumente

**Instrument 1 – Resonator / Modal Synth**

Inspiriert von Mutable Instruments Rings und Elements.

- Karplus-Strong
- Modale Resonatoren
- Unterschiedliche Erregungsmodelle
- Damping, Brightness und weitere Parameter
- Polyphonie
- Eigene Touch-GUI

**Instrument 2 – Polyphonic Granular Synth**

Inspiriert von Tasty Chips GR-1 und GR-MEGA.

- Sample-basierte Granularsynthese
- Grain-Position, Größe, Dichte und Pitch
- Polyphonie
- Modulation
- Wellenform- und Grain-Visualisierung

**Instrument 3 – Physical Modeling Synth**

Ziel ist ein achtstimmiger Synthesizer mit verschiedenen physikalischen Modellen.

- Plucked Strings
- Bowed Strings
- Wind-/Blown-Modelle
- Modal Resonators
- Waveguide-Algorithmen

Die technischen Grenzen werden durch Tests auf realer Hardware ermittelt.

Keines dieser Instrumente muss von Beginn an den vollen Funktionsumfang bieten.

---

# 2. Verbindliche Entwicklungsprinzipien

## 2.1 Hardware-only

Das fertige Instrument muss ohne Host-Computer funktionieren.

Nicht Bestandteil des Projekts:

- JUCE
- VST3/AU-Plugins
- Desktop-Synthesizer
- Eigenständige Windows-Audioanwendungen
- DAW-Integration als Entwicklungsziel

Der Windows-PC dient ausschließlich der Entwicklung, zum Cross-Compiling, Testen, Debuggen und Flashen.

## 2.2 C++ als primäre Entwicklungssprache

Native DSP-Engines und eigene Firmware werden bevorzugt in **C++17** entwickelt.

C-Bibliotheken wie AMY dürfen selbstverständlich integriert werden.

Für die Tulip-GUI sollen zunächst die vorhandenen MicroPython-, LVGL- und Tulip-Schnittstellen genutzt werden.

Eine vollständige Neuentwicklung der Tulip-Firmware in C++ ist nicht vorgesehen, solange die vorhandenen APIs ausreichen.

## 2.3 Bestehende Entwicklungsumgebung verwenden

Die C++-Entwicklungsumgebung ist auf dem Windows-Host bereits installiert.

Untersuche zunächst die vorhandenen Werkzeuge:

- C++-Compiler und Versionen
- CMake
- ARM-Cross-Compiler
- ESP32-Toolchains und ESP-IDF
- Daisy-/STM32-Build-Werkzeuge
- Git und GitHub-Zugang
- Debugging- und Flash-Werkzeuge

Nutze vorhandene Installationen.

Während des Bootstraps keine unnötigen SDKs, Compiler oder Frameworks nachinstallieren.

Fehlende Werkzeuge dokumentieren.

## 2.4 Bestehende DSP-Bibliotheken bevorzugen

Vor eigenen Implementierungen geeignete Bibliotheken untersuchen:

- AMY
- DaisySP
- libDaisy
- DaisyExamples
- Mutable-Instruments-Portierungen

Eine eigene Engine ist erlaubt, wenn bestehende Lösungen funktional oder technisch nicht ausreichen.

Keine unnötige Neuentwicklung bereits verfügbarer Algorithmen.

---

# 3. Zentrale Architekturidee: Skalierbarer DSP-Kern

Die Synthese-Engines sollen möglichst aus einer gemeinsamen, plattformneutralen C++-Codebasis entstehen.

Die beiden Zielplattformen unterscheiden sich erheblich hinsichtlich Speicher, CPU-Leistung und Peripherie.

Deshalb gilt:

**Gemeinsame Algorithmen, aber unterschiedliche Leistungs- und Funktionsprofile.**

## 3.1 Gemeinsame DSP-Basis

Soweit sinnvoll gemeinsam verwendbar:

- Oszillatoren
- Filter
- Hüllkurven
- Resonatoren
- Modulation
- Stimmenverwaltung
- Parameterverarbeitung
- Granular-Algorithmen
- Physical-Modeling-Algorithmen

Hardwareabhängige Funktionen werden getrennt behandelt:

- Audio-I/O
- MIDI und I²C
- Speicherverwaltung
- Interrupts und DMA
- Clocking
- Hardwareinitialisierung
- Plattformoptimierungen

Es muss nicht jeder Algorithmus auf beiden Plattformen identisch implementiert werden.

Insbesondere darf die Verwendung bestehender AMY- oder DaisySP-Funktionen nicht durch eine künstlich vereinheitlichte Softwarearchitektur erschwert werden.

## 3.2 Unterschiedliche Leistungsprofile

Wir unterscheiden konzeptionell zunächst:

**Base Profile – AMYboard**

Ressourcenschonende Konfiguration mit begrenzter Polyphonie, Resonatoranzahl, Grain-Dichte und optional eingeschränkten Algorithmen.

**Extended Profile – Daisy**

Größere Polyphonie, zusätzliche Resonatoren, aufwendigere Physical-Modeling-Algorithmen, größere Sample-Puffer und zusätzliche Funktionen.

Die Daisy-Plattform darf nicht künstlich durch die Leistungsgrenzen des AMYboards beschränkt werden.

Beispiele möglicher Unterschiede:

| Eigenschaft | AMYboard | Daisy |
|---|---|---|
| Polyphonie | Reduziertes Maximum | Höheres Maximum |
| Resonatormoden | Weniger Moden | Mehr Moden |
| Granularsynthese | Kleinere Grain-Wolken | Größere Grain-Wolken |
| Samples | Begrenzte Puffer | Größere Puffer |
| Physical Modeling | Einfachere Modelle | Komplexere Modelle |
| Parameter | Grundfunktionen | Erweiterte Funktionen |

Dies sind keine festgelegten Grenzwerte.

Die tatsächlichen Möglichkeiten werden später durch Messungen ermittelt.

## 3.3 Capability-Modell

Die Softwarearchitektur soll unterschiedliche Hardwarefähigkeiten berücksichtigen können.

Ein DSP-Modul kann beispielsweise beschreiben:

- Unterstützte Synthese-Engines
- Unterstützte Algorithmen
- Maximale Polyphonie
- Anzahl der Resonatormoden
- Maximale Grain-Anzahl
- Unterstützte Parameter
- Verfügbare Audio-Ein- und -Ausgänge
- Verfügbare Effektfunktionen

Tulip soll diese Informationen später verwenden können, um die Benutzeroberfläche passend anzupassen.

Beispiel:

Ein Physical-Modeling-Synth zeigt auf AMYboard nur die verfügbaren Standardparameter.

Auf Daisy erscheinen gegebenenfalls zusätzliche Parameter zur Resonatorstruktur oder zu erweiterten Erregungsmodellen.

**Wichtig:** Für die erste Version reicht eine einfache statische Profildefinition. Keine komplexe automatische Capability-Erkennung implementieren.

---

# 4. Langfristige Multi-DSP-Erweiterbarkeit

Die Plattform soll perspektivisch mehrere DSP-Module unterstützen können.

Ein logisches Instrument soll nicht grundsätzlich auf einen einzigen Prozessor beschränkt sein.

## 4.1 Mögliche Modulrollen

**Voice Engine**

Ein Modul berechnet einen Teil der verfügbaren Stimmen.

Beispiel:

- Daisy 1: Stimmen 1–8
- Daisy 2: Stimmen 9–16

**Layer Engine**

Mehrere Module erzeugen gleichzeitig unterschiedliche Klangschichten.

Beispiel:

- AMYboard: Karplus-Strong
- Daisy 1: Modal Resonators
- Daisy 2: Granular Textures

**FX Engine**

Ein Modul übernimmt ausschließlich Effekte.

Beispiel:

- Daisy 1: Physical-Modeling-Synthese
- Daisy 2: Reverb, Delay und Modulationseffekte

**Hybrid Engine**

Ein Modul übernimmt Synthese und Effekte gleichzeitig.

## 4.2 Audio-Routing

Langfristig denkbar:

- Parallele Audioerzeugung
- Serielle Effektketten
- Voice-Stacks
- Layer-Mixing
- Separate Effektprozessoren
- Sends und Returns
- Gemeinsame Audioausgabe

Eine wichtige technische Voraussetzung ist die Trennung zwischen Steuerprotokoll und Audioverbindungen.

Die Tulip-GUI verwaltet logische Instrumente und Parameter.

Audiosignale werden über geeignete Hardwareverbindungen und gegebenenfalls Mischstufen verarbeitet.

Zu beachten sind:

- Audiolatenz
- Sample-Clock-Synchronisation
- Audio-Pufferung
- Analoge oder digitale Mischverfahren
- Grenzen der physisch verfügbaren Schnittstellen

Multi-DSP-Audio-Routing darf nicht als bereits gelöst betrachtet werden.

## 4.3 Architekturregel

Unterscheide konzeptionell zwischen:

1. **Instrument:** Das musikalische Gerät mit Parametern und Presets.
2. **Engine:** Ein Algorithmus beziehungsweise eine Synthese- oder Effektinstanz.
3. **Module:** Der physische DSP-Prozessor, auf dem Engines laufen.

Diese Trennung soll spätere Erweiterungen erleichtern.

Allerdings gilt ausdrücklich:

**Noch keinen Engine Manager, Cluster-Scheduler, verteilten Voice-Allocator oder eine dynamische Audio-Routing-Matrix entwickeln.**

Für Version 1 reicht ein Instrument mit einer Engine auf einem DSP-Modul.

Die Erweiterbarkeit muss zunächst lediglich architektonisch berücksichtigt und dokumentiert werden.

Keine künstliche Unterstützung beliebig vieler Module implementieren.

---

# 5. Tulip-GUI und Kommunikation

Tulip übernimmt:

- Touchscreen-GUI
- Auswahl der Instrumente
- Parametersteuerung
- Presets
- MIDI-Verarbeitung
- Kommunikation mit DSP-Modulen
- Gegebenenfalls grafische Visualisierungen

## 5.1 Gemeinsames Parametermodell

Die GUI soll möglichst unabhängig von der zugrunde liegenden Hardware sein.

Parameter sollen logisch definiert werden:

- Parameter-ID
- Name
- Typ
- Wertebereich
- Default-Wert
- Einheit
- Skalierung
- Glättung
- Unterstützte Plattformen
- Kommunikationszuordnung

Zusätzliche Daisy-Parameter sind ausdrücklich zulässig.

Nicht unterstützte Funktionen sollen nicht zu Fehlern oder inkonsistenten Zuständen führen.

## 5.2 Presets

Presets beschreiben primär ein Instrument und seine Klangparameter.

Sie sollen möglichst nicht an eine konkrete Prozessoranzahl gebunden sein.

Ein Preset mit erweiterten Daisy-Parametern darf auf AMYboard mit reduzierter Funktionalität geladen werden, sofern das sinnvoll möglich ist.

Nicht unterstützte Parameter sollen nach Möglichkeit erhalten bleiben, damit bei einem erneuten Wechsel zu Daisy keine Einstellungen verloren gehen.

Eine vollständige plattformübergreifende Preset-Implementierung ist noch nicht Bestandteil des Bootstraps.

## 5.3 Kommunikation

Mögliche Transportwege:

- AMY-Wire über I²C
- MIDI-CC
- MIDI-NRPN
- SysEx
- Später gegebenenfalls eigene Nachrichtenformate

Parametersemantik und physisches Übertragungsprotokoll sollen möglichst getrennt bleiben.

Für Version 1 vorhandene Schnittstellen bevorzugen.

Keine eigene komplexe Protokollschicht entwickeln, solange AMY-Wire beziehungsweise MIDI die Anforderungen erfüllen.

---

# 6. Technische Ausgangslage nach Claude

Die bereits vorliegende Untersuchung

`claude/Tulip_Synth_Machbarkeit_Roadmap_2026-10-09.md`

ist eine zentrale technische Referenz.

Sie basiert auf Untersuchungen der Original-Repositories.

Referenzstände:

- `shorepine/tulipcc`: `36e6332`
- `shorepine/amy`: `69a1469`
- `Synthux-Academy/Audrey-II`: `e5ab799`
- `DaisyExamples`: `259ed82`

Prüfe zunächst, ob der vollständige Bericht verfügbar ist.

Lies ihn vollständig, bevor du Architektur oder Roadmap konsolidierst.

Nicht verfügbare Dokumente oder Erkenntnisse ausdrücklich kennzeichnen.

## 6.1 AMYboard

Wesentliche Ergebnisse:

- Dokumentierte I²C-Verbindung über Grove
- I²C-Adresse `0x3f`
- Übertragung mit 400 kHz
- Alternative Kommunikation über AMY-SysEx/MIDI
- Leistungsaufnahme von etwa 350 mA
- Separates USB-C-Netzteil für erste Versuche empfohlen
- Standard-AMY unterstützt bereits unterschiedliche Synthesealgorithmen
- Eingeschränkte Möglichkeiten des On-Device-C-Compilers `xcc700`
- Komplexe eigene DSP-Engines benötigen gegebenenfalls native C/C++-Firmware

Die Grenzen der Standard-Firmware dürfen nicht mit den grundsätzlichen Möglichkeiten des ESP32-S3 gleichgesetzt werden.

Prüfe zusätzlich die existierende AMY-Portierung für Daisy als Referenz für Cross-Platform-DSP.

Die dokumentierte AMYboard-Verkettung über I²C/MIDI und S/PDIF ist als mögliche spätere Multi-DSP-Option zu erfassen.

## 6.2 Daisy / Audrey II

Wesentliche Ergebnisse:

- Die untersuchte Audrey-Stock-Firmware besitzt keinen USB-MIDI-Code.
- Für USB-MIDI ist voraussichtlich eine angepasste Firmware erforderlich.
- Daisy besitzt bereits einen Stereo-Audiocodec.
- Audrey verwendet im untersuchten Firmwarestand 48 kHz und eine Blockgröße von vier Samples.
- Elf Potentiometer und ein Schalter sind verfügbar.
- Ein Audioeingang ist vorhanden.
- Flash-/Bootloader-Grenzen müssen berücksichtigt werden.
- Firmware-Backup und Recovery sind vor Änderungen erforderlich.
- Die Performance komplexer Engines ist bislang nicht auf Hardware nachgewiesen.

Interessante DSP-Referenzen:

- DaisyExamples `patch/Torus`
- DaisyExamples `patch/Nimbus`
- DaisySP `StringVoice`
- DaisySP `ModalVoice`
- DaisySP `Resonator`
- DaisySP `KarplusString`

Die tatsächliche Portierbarkeit vorhandener DSP-Algorithmen nach ESP32-S3 soll untersucht und nicht einfach vorausgesetzt werden.

## 6.3 Dokumentationskorrekturen

Claude hat unter anderem folgende Probleme identifiziert:

- Die AMYboard-Projektübergabe enthält möglicherweise versehentlich die Daisy-Übergabe.
- Falsche Aussagen über die Notwendigkeit eines externen Daisy-Audiocodecs.
- Nicht ausreichend dokumentierte USB-MIDI-Beschränkungen.
- Unklare USB-Buchsentypen und Boardrevisionen.
- Uneindeutige Audrey-Firmware-Dateinamen.
- Fehlende Flash-/Bootloader-Hinweise.
- Fehlende Beschreibung der nutzbaren Audrey-Bedienelemente.
- Unklare Aussagen zur Verfügbarkeit eigener C-DSP-Erweiterungen.
- Fehlende Quellenverweise auf vorhandene DSP-Portierungen.

Arbeite die zehn konkreten Befunde aus Abschnitt 5 der Claude-Analyse einzeln ab.

Bewahre ursprüngliche Dokumente unverändert auf.

Unterscheide:

**BELEGT:** Durch Quellen nachgewiesen.

**GESCHÄTZT:** Technische Hochrechnung.

**UNGEPRÜFT:** Hardwaretest erforderlich.

---

# 7. Repository und Projektstruktur

Gewünschtes Repository:

`sscheidl/Tulip-Synth`

Lokales Arbeitsverzeichnis:

`D:\Eigene Dateien\Eigene Dokumente\Playground\Tulip-Synth`

Prüfe, ob Repository und Verzeichnis bereits existieren.

Falls nicht, erstelle ein privates GitHub-Repository mit passender lokaler Arbeitskopie, soweit Zugriff und Berechtigungen vorhanden sind.

Bestehende Inhalte nicht überschreiben.

Das Repository `sscheidl/Custom-Firmware` bleibt unangetastet.

## 7.1 Vorgeschlagene Struktur

```text
Tulip-Synth/
│
├── README.md
├── AGENTS.md
├── .gitignore
│
├── docs/
│   ├── PROJECT_OVERVIEW.md
│   ├── ARCHITECTURE.md
│   ├── HARDWARE.md
│   ├── PARAMETER_MODEL.md
│   ├── ROADMAP.md
│   ├── DECISIONS.md
│   ├── OPEN_QUESTIONS.md
│   ├── REFERENCES.md
│   ├── CLAUDE_REVIEW_2026-10-09.md
│   ├── handovers/
│   └── research/
│
├── tulip/
│   ├── gui/
│   ├── communication/
│   └── presets/
│
├── dsp/
│   ├── common/
│   ├── amyboard/
│   └── daisy/
│
├── instruments/
│   ├── resonator/
│   ├── granular/
│   └── physical_modeling/
│
├── tests/
└── tools/
```

Dies ist ein Vorschlag, keine starre Vorgabe.

Nicht benötigte Verzeichnisse müssen noch nicht angelegt werden.

Die Struktur soll einfach bleiben und später organisch wachsen.

Keine unnötigen Platzhalterklassen, Dummy-Bibliotheken oder umfangreichen Build-Systeme erstellen.

## 7.2 Dokumentationsübernahme

Suche nach:

- `Tulip_AMYboard_Projektuebergabe_2026-10-09.md`
- Daisy-/Audrey-II-Projektübergabe vom 09.10.2026
- `claude/Tulip_Synth_Machbarkeit_Roadmap_2026-10-09.md`
- Weiteren relevanten Projektunterlagen

Originaldateien unverändert archivieren.

Bei Duplikaten Inhalt und Dateihashes vergleichen.

Falls die AMYboard-Übergabe fehlt, anhand vorhandener Quellen rekonstruieren und als Rekonstruktion kennzeichnen.

Keine fehlenden Informationen erfinden.

---

# 8. Architekturentscheidungen

Erstelle `docs/DECISIONS.md`.

Dokumentiere mindestens:

| ID | Entscheidung |
|---|---|
| D001 | Hardware-only, keine Desktop-Synthesizer |
| D002 | C++17 für eigene native DSP-Engines |
| D003 | Tulip als GUI- und Steuerzentrale |
| D004 | AMYboard als erste Syntheseplattform |
| D005 | Daisy als erweiterte DSP-Plattform |
| D006 | Gemeinsamer DSP-Code, wo sinnvoll |
| D007 | Plattformabhängige Leistungsprofile |
| D008 | Hardwareunabhängiges Parametermodell |
| D009 | Erweiterbarkeit auf mehrere DSP-Module |
| D010 | Unterschiedliche DSP-Rollen und Audio-Routing langfristig möglich |
| D011 | Bestehende Bibliotheken vor Eigenimplementierung |
| D012 | Keine Firmwareänderung ohne Backup/Recovery |
| D013 | Instrumente nacheinander entwickeln |
| D014 | Keine vorzeitige Framework- oder Infrastrukturentwicklung |

Die Architektur muss Erweiterbarkeit ermöglichen, aber nicht bereits sämtliche späteren Funktionen implementieren.

Insbesondere D009 und D010 ausdrücklich als **langfristige Architekturziele, nicht als Anforderungen an Version 1.0** kennzeichnen.

---

# 9. Entwicklungsroadmap

Die Roadmap muss kleine, überprüfbare Meilensteine enthalten.

## M0 – Projekt-Bootstrap

**Einziger Implementierungsumfang dieses Auftrags.**

- Bestandsaufnahme
- Repository initialisieren
- Dokumentation übernehmen
- Claude-Ergebnisse konsolidieren
- Bekannte Fehler dokumentieren und korrigierte Fassungen erstellen
- Architekturentscheidungen festhalten
- Entwicklungsumgebung inventarisieren
- Roadmap erstellen
- AGENTS.md erstellen

Ergebnis: Vollständig nutzbare Entwicklungsbasis.

## M1 – Erstes Hardwareinstrument

**Tulip + ein AMYboard**

- I²C-Kommunikation
- Sichere Stromversorgung
- Einfache Touch-GUI
- Steuerung vorhandener AMY-Parameter
- Karplus-Strong beziehungsweise erster Resonator-Klang
- MIDI-Notenverarbeitung
- Einfaches Preset

Erfolgskriterium:

Ein spielbarer Hardware-Synthesizer mit funktionierender grafischer Bedienung.

Zusätzlich mindestens 30 Minuten stabiler Betrieb ohne Reboot.

Dies ist die erste wichtige Fertigstellungsgrenze.

Ein funktionierender M1 ist bereits ein eigenständig nutzbares Ergebnis.

## M2 – Daisy-Kompatibilität

- Audrey-Hardware und Firmwarestand dokumentieren
- Original-Firmware sichern
- Recovery-Verfahren vorbereiten
- Minimale eigene USB-MIDI-Firmware
- Note-On/Off und Parameterübertragung
- Audioausgabe testen

Ergebnis:

Daisy lässt sich grundsätzlich als alternativer DSP-Klangerzeuger verwenden.

Keine umfangreiche Synthese-Engine portieren, bevor die Verbindung funktioniert.

## M3 – Erste gemeinsame C++-Engine

- Geeigneten einfachen Resonator-Algorithmus auswählen
- Möglichst gemeinsame C++-DSP-Basis
- Builds für ESP32-S3 und STM32H750
- Plattformabhängige Audiotreiber
- CPU- und Speicherverbrauch messen
- Unterschiede der Leistungsprofile dokumentieren

Ergebnis:

Ein Algorithmus läuft auf beiden Hardwareplattformen.

Wenn die Cross-Portierung unverhältnismäßig aufwendig wird, die Ursachen dokumentieren und die gemeinsame Codebasis entsprechend begrenzen.

## M4 – Erweiterter Resonator-Synth

- Vorhandene DSP-Portierungen nutzen
- Unterschiedliche Resonatormodelle
- Plattformabhängige Polyphonie
- Zusätzliche Daisy-Funktionen
- GUI erweitern
- Presets integrieren

Ergebnis:

Ein vollständigeres, musikalisch nutzbares Resonator-Instrument.

## M5 – Physical Modeling

- Zusätzliche Synthesemodelle
- Polyphonie optimieren
- Acht Stimmen als Entwicklungsziel
- CPU- und Speicherverbrauch messen
- Gemeinsame Parameter und Presets

## M6 – Granular Synth

- Sample-Verwaltung
- Grain-Engine
- Modulation
- Polyphonie
- Wellenformdarstellung
- Plattformabhängige Leistungsprofile

## M7 – Optionale Multi-DSP-Experimente

Erst nach erfolgreichen Einzelmodul-Instrumenten.

Mögliche Experimente:

- Zwei AMYboards
- Zwei Daisy Seeds
- Voice-Stacking
- Unterschiedliche Synthese-Layer
- Ein dediziertes Effektmodul
- Audio-Routing zwischen Modulen

Dies ist ausdrücklich **kein verpflichtender Entwicklungsschritt für Version 1.0**.

Vor jeder Umsetzung Aufwand, Nutzen und technische Voraussetzungen neu bewerten.

---

# 10. AGENTS.md – Leitlinien für Codex

Erstelle eine kurze und verbindliche `AGENTS.md`.

Wichtige Regeln:

1. Vor wesentlichen Änderungen die aktuelle Projektdokumentation lesen.
2. GitHub dient als zentrale technische Wissensbasis.
3. Kleine, nachvollziehbare Entwicklungsschritte.
4. C++17 für eigene native DSP-Entwicklung bevorzugen.
5. Bestehende Bibliotheken und APIs wiederverwenden.
6. Keine JUCE-, VST3- oder Desktop-Synthesizer-Projekte.
7. Hardwarezugriffe möglichst vom DSP-Code trennen.
8. Plattformabhängige Optimierungen ausdrücklich erlauben.
9. Daisy nicht künstlich auf das Leistungsniveau des AMYboards beschränken.
10. Parameter und GUI möglichst hardwareunabhängig halten.
11. Multi-DSP-Erweiterbarkeit berücksichtigen, aber nicht vorzeitig implementieren.
12. Keine Firmware ohne ausdrücklichen Auftrag flashen.
13. Vor Firmwareänderungen Backup und Recovery dokumentieren.
14. Keine destruktiven Git-Operationen.
15. Keine unnötigen Frameworks, Build-Systeme oder Abhängigkeiten.
16. Tests und Messergebnisse dokumentieren.
17. Fremdlizenzen respektieren.
18. Funktionierende Instrumente haben Vorrang vor architektonischer Perfektion.

### Wichtigste Projektregel

**Dieses Projekt ist gefährdet, durch übermäßige Architekturplanung niemals fertiggestellt zu werden.**

Bevorzuge funktionierende, spielbare Instrumente gegenüber theoretisch perfekter Erweiterbarkeit.

Skalierbarkeit soll durch einfache Schnittstellen und saubere Trennung von Verantwortlichkeiten ermöglicht werden.

Implementiere keine Infrastruktur für Anforderungen, die noch nicht praktisch benötigt werden.

---

# 11. Technische Referenzen

Primärquellen:

**Tulip / AMY**

- https://github.com/shorepine/tulipcc
- https://github.com/shorepine/amy
- https://github.com/shorepine/tulipcc/blob/main/docs/amyboard/README.md
- https://github.com/shorepine/tulipcc/blob/main/docs/amyboard/faq.md
- https://github.com/shorepine/tulipcc/blob/main/docs/user_c_dsp.md
- https://github.com/shorepine/amy/blob/main/docs/api.md

**Daisy**

- https://github.com/Synthux-Academy/Audrey-II
- https://github.com/daisyaudio/DaisyExamples
- https://github.com/electro-smith/DaisySP
- https://daisy.audio/

**Mutable Instruments**

- https://github.com/pichenettes/eurorack

Ergänze bei Bedarf weitere technische Referenzen.

Dokumentiere Quellen und Versionen.

Vermeide unnötige Mehrfachrecherche bereits gesicherter Erkenntnisse.

---

# 12. Konkreter Arbeitsauftrag – jetzt ausführen

Dieser Auftrag umfasst ausschließlich **Milestone 0**.

Arbeite selbstständig in folgenden Schritten:

### Schritt 1 – Bestandsaufnahme

- Lokales Arbeitsverzeichnis prüfen
- GitHub-Repository prüfen
- Vorhandene Dokumente suchen
- Entwicklungswerkzeuge erfassen
- Keine bestehenden Daten verändern

### Schritt 2 – Dokumentation analysieren

- Claude-Bericht vollständig lesen
- Projektübergaben vergleichen
- Dokumentationsfehler erfassen
- Fehlende AMYboard-Übergabe suchen
- Gegebenenfalls rekonstruieren

### Schritt 3 – Repository vorbereiten

- Private GitHub-Repository-Struktur erstellen
- Dokumente übernehmen
- README erstellen
- .gitignore erstellen
- AGENTS.md erstellen

### Schritt 4 – Architektur dokumentieren

Erstelle:

- `docs/PROJECT_OVERVIEW.md`
- `docs/ARCHITECTURE.md`
- `docs/HARDWARE.md`
- `docs/PARAMETER_MODEL.md`
- `docs/DECISIONS.md`
- `docs/OPEN_QUESTIONS.md`
- `docs/CLAUDE_REVIEW_2026-10-09.md`

Die Dokumentation soll präzise und verständlich bleiben.

Insbesondere keine unnötigen umfangreichen Schnittstellenspezifikationen für Multi-DSP-Funktionen erstellen.

### Schritt 5 – Roadmap

- Meilensteine festlegen
- Technische Abhängigkeiten kennzeichnen
- Prüfkriterien definieren
- Risiken dokumentieren
- Optionale langfristige Erweiterungen klar abgrenzen

### Schritt 6 – Konsistenzprüfung

Prüfe:

- Widersprüche zwischen den Dokumenten
- Vollständigkeit der bekannten Claude-Ergebnisse
- Plausibilität der Roadmap
- Trennung zwischen Anforderungen und langfristigen Ideen
- Versehentlich eingeführte Abhängigkeiten von JUCE/VST3
- Unnötig komplexe Architekturvorschläge

### Schritt 7 – Git-Abschluss

- Änderungen kontrollieren
- Initial-Commit erstellen
- Ins vorgesehene Repository pushen, soweit möglich
- Commit-ID dokumentieren

Keine Force-Pushes und keine Änderungen an anderen Repositories.

---

# 13. Was ausdrücklich nicht umgesetzt werden soll

Während Milestone 0:

- Keine Synthese-Engine implementieren.
- Keine GUI programmieren.
- Keine Hardware flashen.
- Keine neuen Frameworks entwickeln.
- Keine Multi-DSP-Verwaltung implementieren.
- Keine Audio-Routing-Matrix entwickeln.
- Keine dynamische Lastverteilung programmieren.
- Keine komplexen Kommunikationsprotokolle entwickeln.
- Keine unnötigen SDKs installieren.
- Keine umfangreiche CI/CD-Infrastruktur einrichten.

Die Architektur soll vorbereitet, nicht vorzeitig implementiert werden.

---

# 14. Erwartetes Ergebnis und Abschlussbericht

Nach Abschluss sollen folgende Ergebnisse vorliegen:

1. Ein privates GitHub-Repository `sscheidl/Tulip-Synth`, sofern zugänglich.
2. Eine nutzbare lokale Arbeitskopie.
3. Übernommene und unverändert archivierte Originaldokumente.
4. Konsolidierte Claude-Erkenntnisse.
5. Dokumentierte Architekturentscheidungen.
6. Ein einfaches, erweiterbares Parameter- und Hardwarekonzept.
7. Eine Roadmap mit klaren Meilensteinen.
8. Eine präzise `AGENTS.md`.
9. Eine Bestandsaufnahme der vorhandenen C++-Entwicklungswerkzeuge.
10. Ein nachvollziehbarer Git-Commit.

Berichte kompakt über:

- Repository und Arbeitsverzeichnis
- Branch und Commit-ID
- Übernommene und erstellte Dateien
- Erkannte Dokumentationsfehler
- Offene technische Fragen
- Vorhandene und gegebenenfalls fehlende Entwicklungswerkzeuge
- Empfohlenen nächsten Entwicklungsschritt

Bewerte abschließend, ob wir unmittelbar mit **M1: Tulip + AMYboard, erste Touch-GUI und Karplus-Strong-Synthese** beginnen können.

## Abschließende Priorität

Die langfristige Vision ist eine skalierbare Multi-DSP-Synthesizer-Plattform.

Unser unmittelbares Ziel ist jedoch viel kleiner:

**Ein Tulip, ein AMYboard, eine funktionierende GUI und ein spielbarer Synthesizer.**

Alles Weitere soll darauf aufbauen.

**Beginne jetzt mit der Bestandsaufnahme und führe ausschließlich Milestone 0 durch.**
