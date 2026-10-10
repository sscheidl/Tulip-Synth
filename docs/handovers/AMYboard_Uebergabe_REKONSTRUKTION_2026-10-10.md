# AMYboard – Projektübergabe (REKONSTRUKTION)

> **Dies ist keine Originalübergabe.** Die Datei `Tulip_AMYboard_Projektuebergabe_2026-10-09.md` war in der Bootstrap-Sitzung nicht verfügbar (vermutet: Sie enthielt versehentlich die Daisy-Übergabe, Befund 1).
> Diese Rekonstruktion stützt sich **ausschließlich** auf Primärquellen: `shorepine/tulipcc@36e6332`, `shorepine/amy@69a1469`. Erfundene oder aus dem Original übernommene Inhalte gibt es nicht. Was im Original stand, ist unbekannt.
> Erstellt: 10.10.2026 im Rahmen von M0.

## 1. Was das AMYboard ist

ESP32-S3-Board (10 HP Eurorack-Format, Makerfabs) mit MicroPython und der Synth-Engine AMY. Juno-6-, DX7-, Piano-, Drum- und weitere Patches eingebaut; Karplus-Strong als Oszillator-Wellenform `KS`. Bootet standardmäßig mit Juno-6-Patch #0 auf MIDI-Kanal 1. (BELEGT, `docs/amyboard/README.md`)

## 2. Anschlüsse (BELEGT)

| Anschluss | Ort | Funktion |
|---|---|---|
| Line In / Line Out | Front | Stereo 3,5 mm; Pegel per 4 DIP-Schaltern (alle OFF = Line) |
| S/PDIF In / Out | Front | Stereo 3,5 mm, digital; Verkettung mehrerer Boards |
| TRS-MIDI In/Out | Front | 3,5 mm TRS Typ A oder B |
| CV1/CV2 In, CV1/CV2 Out | Front | ±10 V (ADS1015-ADC, GP8413-DAC) |
| I²C (Grove) | Front | Zubehör (Encoder, OLED) |
| I²C „host“ | Rückseite | **Anschluss an Tulip** (AMYboard als I²C-Slave) |
| USB-C | Seite | Strom, Serial-REPL, USB-MIDI (nur Gadget, **kein Host**), Firmware-Update |
| 10-Pin-Eurorack | Rückseite | +12 V |
| MicroSD | Seite | Samples, Patches |
| Debug-Header | Rückseite | Firmware-Entwicklung |

## 3. Anbindung an Tulip (BELEGT)

```python
# auf dem Tulip
from machine import I2C
i2c = I2C(0, freq=400000)
amy.override_send = lambda x: i2c.writeto(0x3f, x)
# ab jetzt gehen alle amy.send(...) an das AMYboard
amy.override_send = None   # zurück zur lokalen Tulip-Engine
```

Alternative über MIDI: `amy.override_send = midi.sysex_amy`.

## 4. Strom (BELEGT)

- Versorgung über USB-C (5 V), Eurorack (+12 V) oder I²C-Host-Port (3,3 V vom Tulip); höchste Spannung gewinnt.
- Über den Tulip versorgt: ~350 mA aus dessen 3,3-V-Schiene, zusätzlich zu ~575 mA des Tulip → Gefahr von **Boot-Loops des Tulip**.
- **Empfehlung für dieses Projekt:** AMYboard über eigenes USB-C versorgen; Tulip an 1–2-A-Netzteil, gutes Datenkabel, kein Hub.

## 5. Leistungsgrenzen (BELEGT, FAQ)

- CPU-Richtwerte pro Stimme: Juno ~12 %, DX7 ~8 %, PCM/Drum ~2 % → etwa 8 Juno-Stimmen.
- AMY max. ~250 Oszillatoren; 16 MIDI-Kanäle gleichzeitig nutzbar.
- ~3 MB SPIRAM für Samples (~30 s mono 44,1 kHz); SD-Karte nur 1-Bit-SPI.
- Zu häufige I²C-Displayupdates können Audio aushungern.
- KS-Kosten: **nicht dokumentiert, UNGEPRÜFT**.

## 6. Eigene DSP-Erweiterungen (BELEGT)

| Weg | Möglichkeiten | Grenzen |
|---|---|---|
| `tulip.install_c_process` / `install_c_osc` (`xcc700`, on-device) | Effekte/Oszillatoren zur Laufzeit, ohne Flash | „very alpha“; nur `int`/`int16_t`, keine floats/structs/`for`/Präprozessor; 8 Slots; S8.23-Fixed-Point |
| Eigene Firmware mit AMY-Hooks (`amy_external_render_hook`, `amy_external_bus_postprocess_hook`) | volles C/C++ | eigener ESP-IDF-Build nötig, Aufwand UNGEPRÜFT |

Die Grenzen der Standard-Firmware sind **nicht** die Grenzen des ESP32-S3.

## 7. Firmware und Recovery (BELEGT, `docs/amyboard/firmware.md`)

Bootloader-Modus: beide Tasten halten, RST zuerst loslassen, dann BOOT. Web-Upgrader auf amyboard.com: „Upgrade“ (behält Dateien) oder „Fully erase and re-flash“. Nur ein USB-JTAG-Gerät sichtbar → Board steht im DFU-Modus, BOOT drücken.

## 8. Verkettung (BELEGT, FAQ; Relevanz erst M7)

Audio über S/PDIF, Steuerung über I²C oder MIDI. Kein eingebautes Voice-Splitting; eigenes `override_send` möglich. ~4 Boards über die I²C-Kette mit Strom versorgbar.

## 9. Offene Punkte für M1

Firmwareversion am eigenen Gerät · KS-Polyphonie · sinnvolle KS-Parameter · I²C-Parameterrate · Brummschleifen bei getrennter Versorgung. Siehe `../OPEN_QUESTIONS.md`.
