# Tulip Synth

Offene, experimentelle **Hardware-Synthesizer-Plattform** als zusammenhängendes Desktopinstrument: Ein [Tulip CC](https://github.com/shorepine/tulipcc) mit Touchscreen übernimmt GUI, Presets und Steuerung. **Tulip + AMYboard und das Daisy Seed3 Desktop Dev Kit werden zunächst parallel eigenständig erprobt.** Danach wird ihre Verknüpfung und Erweiterung bewertet (D019). Eine Synthux Audrey II ist als weiteres Gerät vorhanden.

> **Groß denken, klein bauen.**
> Zwei praktische Wege: **Tulip + AMYboard spielbar machen und parallel das Daisy Desktop Dev Kit erproben.**
> Verbindung und Erweiterung folgen aus den Erfahrungen.

## Projektstatus

| Meilenstein | Inhalt | Status |
|---|---|---|
| M0 | Repository, Dokumentation, Architektur, Roadmap | abgeschlossen (siehe [ROADMAP](docs/ROADMAP.md)) |
| M1 / M2a | Tulip + AMYboard / Daisy Desktop Dev Kit eigenständig | **parallel als Nächstes** |
| M2b | Verknüpfung bewerten und Daisy integrieren | nach M1 + M2a |
| M3–M7 | Gemeinsame C++-Engine, Resonator, Physical Modeling, Granular, Multi-DSP (optional) | geplant |
| G1/G2 | Entwicklergehäuse (mit M1) / endgültiges 3D-gedrucktes Gehäuse (nach M4) | geplant |

Es gibt noch **keinen Code**. Das ist Absicht (M0 = nur Dokumentation).

## Geplante Instrumente

1. **Resonator / Modal Synth**: Karplus-Strong, modale Resonatoren, Erregungsmodelle (Vorbild: Mutable Instruments Rings/Elements)
2. **Polyphonic Granular Synth** (Vorbild: Tasty Chips GR-1)
3. **Physical Modeling Synth**: Plucked/Bowed/Blown, Waveguides, Ziel acht Stimmen

## Grundregeln

- **Hardware-only.** Kein JUCE, kein VST3/AU, keine Desktop-Synthesizer. Der PC ist nur Entwicklungswerkzeug.
- **C++17** für eigene native DSP-Engines und Firmware. Die Tulip-GUI nutzt MicroPython/LVGL.
- **Bestehende Bibliotheken zuerst** (AMY, DaisySP, libDaisy, Mutable-Portierungen).
- **Keine Firmware-Binaries im Git** (siehe [D016](docs/DECISIONS.md)).
- Verbindliche Arbeitsregeln für Agenten: [AGENTS.md](AGENTS.md).

## Dokumentation

| Dokument | Inhalt |
|---|---|
| [docs/PROJECT_OVERVIEW.md](docs/PROJECT_OVERVIEW.md) | Vision, Ziele, Abgrenzung |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Instrument/Engine/Modul, DSP-Kern, Profile, Erweiterbarkeit |
| [docs/HARDWARE.md](docs/HARDWARE.md) | Tulip CC, AMYboard, Daisy/Audrey II, Strom, Recovery, Gehäuse |
| [docs/PARAMETER_MODEL.md](docs/PARAMETER_MODEL.md) | Hardwareunabhängiges Parameter- und Preset-Modell |
| [docs/DECISIONS.md](docs/DECISIONS.md) | Architekturentscheidungen D001 ff. |
| [docs/ROADMAP.md](docs/ROADMAP.md) | Meilensteine M0–M7, Prüfkriterien, Risiken |
| [docs/OPEN_QUESTIONS.md](docs/OPEN_QUESTIONS.md) | Offene technische Fragen |
| [docs/DEV_ENVIRONMENT.md](docs/DEV_ENVIRONMENT.md) | Werkzeuginventur (Windows-Host / Cloud-Container) |
| [docs/REFERENCES.md](docs/REFERENCES.md) | Quellen mit Versionsständen |
| [docs/CLAUDE_REVIEW_2026-10-09.md](docs/CLAUDE_REVIEW_2026-10-09.md) | Konsolidierung der Claude-Analyse und Dokumentationskorrekturen |
| [docs/handovers/](docs/handovers/) | Archiv der Projektübergaben (Originale + Rekonstruktion) |
| [docs/research/](docs/research/) | Quellenprüfungen und Messergebnisse |

## Kennzeichnung von Aussagen

- **BELEGT**: durch Quelle (Datei, Commit, Datenblatt) nachgewiesen
- **GESCHÄTZT**: technische Hochrechnung
- **UNGEPRÜFT**: Hardwaretest erforderlich

## Lizenz

Noch nicht festgelegt (siehe [OPEN_QUESTIONS](docs/OPEN_QUESTIONS.md), Q-ORG-1). Eingebundene Fremdbibliotheken behalten ihre Lizenzen (siehe [REFERENCES](docs/REFERENCES.md)).
