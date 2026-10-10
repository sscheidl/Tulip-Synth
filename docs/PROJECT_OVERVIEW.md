# Projektübersicht

## Idee

Tulip Synth ist eine offene, experimentelle Hardware-Synthesizer-Plattform.

- **Tulip CC** (ESP32-S3, Touchscreen, MicroPython, LVGL) ist die **Bedien- und Steuerzentrale**: GUI, Instrumentauswahl, Parameter, Presets, MIDI, Kommunikation, Visualisierung.
- **DSP-Module** erzeugen den Klang:
  - **AMYboard** (ESP32-S3, AMY-Synthesizer, MicroPython) als erste Syntheseplattform
  - **Daisy Seed** (STM32H750, vorhanden in der Synthux Audrey II) als erweiterte DSP-Plattform
  - langfristig eventuell mehrere Module

Konzeptionelles Vorbild für die langfristige Vision ist die modulare DSP-Architektur der Creamware-SCOPE-Systeme. **Das ist eine Vision, kein Implementierungsauftrag.**

**Bauform:** Tulip Synth ist ein **zusammenhängendes Desktopinstrument** (D015). Während der Entwicklung sitzen die Module in einem provisorischen, gut zugänglichen Entwicklergehäuse. Das spätere Endgehäuse wird 3D-gedruckt und nimmt weitere DSP-Module, Audioanschlüsse und eine gemeinsame Stromversorgung auf.

## Ziele, nach Priorität

1. **Ein spielbares Hardwareinstrument** (M1): Tulip + ein AMYboard, Touch-GUI, Karplus-Strong/Resonator, MIDI-Noten, ein Preset, 30 min stabiler Betrieb.
2. **Daisy als alternative Klangquelle** (M2).
3. **Gemeinsame C++-DSP-Basis** für beide Plattformen, wo sinnvoll (M3).
4. Drei vollwertige Instrumente: Resonator (M4), Physical Modeling (M5), Granular (M6).
5. **Optional:** Multi-DSP-Experimente (M7).
6. **Gehäuse, parallel:** Entwicklergehäuse ab M1 (G1), endgültiges 3D-gedrucktes Gehäuse nach M4 (G2).

## Die drei Instrumente

| Instrument | Vorbild | Kernfunktionen | Erster Meilenstein |
|---|---|---|---|
| Resonator / Modal Synth | MI Rings, Elements | Karplus-Strong, modale Resonatoren, Erregungsmodelle, Damping/Brightness, Polyphonie | M1 (einfach), M4 (erweitert) |
| Physical Modeling Synth | – | Plucked/Bowed/Blown, Modal, Waveguides, Ziel 8 Stimmen | M5 |
| Polyphonic Granular Synth | Tasty Chips GR-1 / GR-MEGA | Grain-Position/Größe/Dichte/Pitch, Modulation, Wellenformanzeige | M6 |

Keines der Instrumente muss von Anfang an den vollen Funktionsumfang haben. Die technischen Grenzen werden auf realer Hardware gemessen.

## Abgrenzung (nicht Bestandteil)

- JUCE, VST3/AU-Plugins, Desktop-Synthesizer, eigenständige Windows-Audioanwendungen, DAW-Integration
- Neuentwicklung der Tulip-Firmware in C++ (solange die vorhandenen APIs reichen)
- Eigene Kommunikationsprotokolle (solange AMY-Wire/MIDI reichen)
- Engine-Manager, Cluster-Scheduler, verteilte Voice-Allocation, Audio-Routing-Matrix (frühestens M7 und nur nach Neubewertung)

Hinweis: AMYboard gibt es auch als VCV-Rack-Plugin und als Web-Version. Diese dürfen als **Entwicklungs- und Testhilfe** genutzt werden, sind aber kein Produktziel (D001).

## Rollen in der Zusammenarbeit

- **Eigentümer** (sscheidl): Ziele, Hardware, Tests am Gerät, Flash-Freigaben
- **Codex / Claude**: Analyse, Code, Dokumentation nach `AGENTS.md`
- **GitHub-Repository**: zentrale Wissensbasis und Übergabe zwischen Sitzungen
