# Architektur

Grundsatz: **Erweiterbarkeit ermöglichen, aber nicht vorab implementieren.** Dieses Dokument beschreibt Begriffe, Schnitte und die Form von Version 1. Langfristige Ideen sind deutlich als solche markiert.

## 1. Drei Begriffe

| Begriff | Bedeutung | Beispiel |
|---|---|---|
| **Instrument** | Das musikalische Gerät aus Sicht der Bedienung: Parameter, Presets, GUI | „Resonator“ |
| **Engine** | Ein Algorithmus bzw. eine Synthese- oder Effektinstanz | AMY-Karplus-Strong, DaisySP `StringVoice` |
| **Modul** | Der physische DSP-Prozessor, auf dem Engines laufen | AMYboard #1, Daisy Seed in Audrey II |

**Version 1 ist genau: 1 Instrument → 1 Engine → 1 Modul.**
Die Begriffe werden nur in Dokumentation, Namensgebung und Preset-Format verwendet. Es gibt dafür keine Klassen, keinen Manager und keine Registry.

**Physische Ebene:** Module sind auch mechanisch Einheiten im gemeinsamen Gehäuse (D015). Ein späteres zusätzliches Modul braucht einen Steckplatz, Strom, eine Steuerverbindung und einen Audioweg. Diese vier Dinge sind beim Gehäuse einzuplanen, nicht in der Software.

## 2. Form von Version 1 (M1)

```text
            MIDI-Keyboard (USB-Host am Tulip oder TRS-MIDI)
                          │
┌─────────────────────────▼─────────────────────────┐
│ Tulip CC (MicroPython + LVGL)                     │
│  GUI (Touch) ─► Parametermodell ─► Transport      │
│  Presets (JSON auf Tulip-Dateisystem)             │
└─────────────────────────┬─────────────────────────┘
                          │ Steuerung: AMY-Wire über I²C (Grove, 0x3f, 400 kHz)
                          │ (Alternative: AMY-SysEx über MIDI)
┌─────────────────────────▼─────────────────────────┐
│ AMYboard (Standard-Firmware, AMY)                 │
│  Engine: AMY-Oszillator wave=KS (Karplus-Strong)  │
└─────────────────────────┬─────────────────────────┘
                          │ Audio: analoger Line-Out (3,5 mm)
                          ▼
                     Mischpult / Kopfhörer
```

Wesentliche Eigenschaften:

- **Steuerweg und Audioweg sind getrennt.** Tulip transportiert nur Steuerdaten, nie Audio.
- In M1 läuft **keine eigene Firmware** auf dem AMYboard (D017). AMY bringt Karplus-Strong als Wellenform `KS` bereits mit (BELEGT, `amy/src/oscillators.c` `render_ks`, `ks_note_on`).
- Stromversorgung des AMYboards in M1 **über eigenes USB-C** (siehe HARDWARE.md).

## 3. Schichten und Verantwortlichkeiten

| Schicht | Ort | Verantwortung | Sprache |
|---|---|---|---|
| GUI | Tulip | Darstellung, Touch-Bedienung, Visualisierung | MicroPython/LVGL |
| Parametermodell | Tulip | Logische Parameter, Wertebereiche, Skalierung, Presets | MicroPython (Daten als JSON/Python-Dict) |
| Transport | Tulip | Abbildung logischer Parameter auf AMY-Wire / MIDI CC / NRPN / SysEx | MicroPython |
| Engine | DSP-Modul | Klangerzeugung | AMY (C) bzw. eigene C++17-Engines |
| Plattformschicht | DSP-Modul | Audio-I/O, MIDI, I²C, DMA, Interrupts, Clocking, Speicher | C/C++ (ESP-IDF, libDaisy) |

Regel: **GUI kennt keine Transportdetails, Engine kennt keine Hardware.** Die Zuordnung „logischer Parameter → Nachricht“ liegt an genau einer Stelle (Transport).

## 4. Skalierbarer DSP-Kern (ab M3)

### 4.1 Gemeinsamer Code, wo sinnvoll

Plattformneutraler C++17-Code (später `dsp/common/`) für Oszillatoren, Filter, Hüllkurven, Resonatoren, Voice-Handling, Parameter-Glättung, Granular- und PM-Algorithmen.

Regeln für gemeinsamen DSP-Code:

- Keine Hardware-Header, keine Betriebssystemaufrufe, keine Allokation im Audio-Callback.
- Speicher wird von außen übergeben (Puffergrößen sind profilabhängig).
- Verarbeitung blockweise, `float` als Standard-Sampleformat. Konvertierung in plattformspezifische Formate erfolgt in der Plattformschicht (AMY arbeitet intern mit Fixed-Point S8.23 in `int32_t`, BELEGT `amy/docs/api.md` Hooks-Abschnitt).
- Header-zentriert und einfach; kein eigenes Build-Framework.

### 4.2 Plattformschicht

| Aufgabe | AMYboard (ESP32-S3) | Daisy Seed (STM32H750) |
|---|---|---|
| Audio-I/O | AMY/ESP-IDF I²S | libDaisy `AudioHandle` |
| Einbindung eigener Engine | AMY-Hooks `amy_external_render_hook` / `amy_external_bus_postprocess_hook` in einer eigenen Firmware-Build (UNGEPRÜFT) | eigenes `AudioCallback` |
| MIDI | AMY-MIDI (USB-Gadget, TRS) | libDaisy `MidiUsbHandler` / `MidiUartHandler` |
| Speicher | SPIRAM (~3 MB frei für Samples, BELEGT FAQ) | externes SDRAM (laut Daisy-Seed-Datenblatt 64 MB, für das eigene Board UNGEPRÜFT); Audrey nutzt `Source/memory/sdram_alloc` |

**Es muss nicht jeder Algorithmus auf beiden Plattformen identisch sein.** Wenn AMY- oder DaisySP-Funktionen direkt passen, werden sie direkt genutzt. Eine künstlich vereinheitlichte Abstraktion darüber ist verboten (D006, D011).

### 4.3 Leistungsprofile (statisch)

| Profil | Plattform | Charakter |
|---|---|---|
| **Base** | AMYboard | begrenzte Polyphonie, weniger Moden, kleinere Grain-Wolken, einfachere Modelle |
| **Extended** | Daisy | höhere Polyphonie, mehr Moden, größere Puffer, aufwendigere Modelle, Zusatzparameter |

Konkrete Grenzwerte werden **gemessen** (M3–M6) und erst dann eingetragen. Daisy wird nicht auf Base-Niveau beschränkt (D007).

### 4.4 Capability-Modell (minimal)

Für Version 1 genügt eine **statische Profildatei pro Plattform** auf dem Tulip (z. B. ein Python-Dict), etwa:

```python
PROFILE_AMYBOARD = {
    "module": "amyboard",
    "engines": ["amy_ks"],
    "max_voices": None,   # wird in M1 gemessen
    "params": ["feedback", "filter_freq", "resonance", "volume"],  # Beispiel; endgültige Liste in M1
}
```

Die GUI zeigt nur Parameter, die im aktiven Profil stehen. **Keine** automatische Capability-Erkennung, kein Aushandlungsprotokoll.

## 5. Geplante Verzeichnisstruktur

Verzeichnisse werden erst angelegt, wenn sie Inhalt bekommen.

```text
tulip/gui/            Touch-GUI (ab M1)
tulip/communication/  Transport AMY-Wire/MIDI (ab M1)
tulip/presets/        Preset-Dateien und -Code (ab M1)
dsp/common/           plattformneutraler C++17-DSP-Code (ab M3)
dsp/amyboard/         ESP32-S3-Plattformschicht (ab M3)
dsp/daisy/            Daisy-Plattformschicht und Firmware (ab M2)
instruments/<name>/   instrumentspezifische Parameterdefinitionen und Presets
tests/                Host-Unit-Tests für dsp/common (ab M3, nur Testhilfe, kein Desktop-Synth)
tools/                kleine Hilfsskripte
docs/research/        Messergebnisse und Quellenprüfungen
```

## 6. Langfristig: Multi-DSP (NICHT Teil von Version 1.0)

> Alles in diesem Abschnitt ist ein **langfristiges Architekturziel** (D009, D010). Nichts davon wird vor M7 implementiert, und M7 selbst ist optional.

Mögliche Modulrollen: **Voice Engine** (Stimmen aufgeteilt), **Layer Engine** (verschiedene Klangschichten), **FX Engine** (nur Effekte), **Hybrid Engine**.

Was die heutige Architektur dafür bereits richtig macht, ohne Zusatzaufwand:

- Steuerweg und Audioweg sind getrennt.
- Presets beschreiben Instrumente, nicht Prozessoren.
- Der Transport ist an einer Stelle gekapselt; ein zweites Modul wäre ein zweites Transportziel.

Bekannte Bausteine (BELEGT, `tulipcc/docs/amyboard/faq.md`, Abschnitt „Chaining multiple AMYboards“):

- AMYboards lassen sich verketten: Audio über **S/PDIF** in→out, Steuerung über **I²C** oder **MIDI**.
- Es gibt **kein eingebautes Voice-Splitting**; eine eigene `amy.override_send`-Funktion kann Noten auf Boards verteilen.
- Etwa 4 Boards sind über die I²C-Kette mit Strom versorgbar (~350 mA je Board, Spannungsabfall auf ~2,94 V am 4. Board gemessen).

Ungelöste Probleme (bewusst offen gelassen): Sample-Clock-Synchronisation zwischen Modulen, Latenz, analoges vs. digitales Mischen, physisch begrenzte Schnittstellen (ob und wie ein Daisy Seed digital mit einem AMYboard-S/PDIF-Pfad verbunden werden kann, ist UNGEPRÜFT). Siehe OPEN_QUESTIONS.md.

## 7. Ausdrücklich nicht gebaut

Engine-Manager, Cluster-Scheduler, verteilter Voice-Allocator, dynamische Audio-Routing-Matrix, Lastverteilung, eigenes Protokoll, automatische Capability-Erkennung, CI/CD-Infrastruktur, Plugin-/Desktop-Varianten.
