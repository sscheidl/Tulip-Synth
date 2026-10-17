# Tulip USB-REPL geprüft – 17.10.2026

## Aufbau und Verfahren

Windows-Host, Tulip laut Eigentümer an COM9. Windows erkennt `USB-SERIAL CH340K (COM9)`, VID 1A86 / PID 7522. Verbindung über .NET `System.IO.Ports.SerialPort`: 115200 Baud, 8 Datenbits, keine Parität, 1 Stopbit, DTR/RTS deaktiviert. Port nach Prüfung geschlossen.

Nur Leerzeile und lesender REPL-Befehl ausgeführt:

```python
import sys, os; print('TULIP_PROBE', sys.implementation, os.uname())
```

## Ergebnis (BELEGT am Gerät)

- MicroPython-Prompt `>>>` erreichbar; Befehl erfolgreich beantwortet.
- Gerätekennung: `TulipCC with ESP32S3`.
- MicroPython: `1.24.0-preview`.
- `os.uname().version`: `82e69df-dirty on 2026-07-08`.
- Beim ersten Öffnen kam eine ESP32-S3-Bootmeldung mit `rst:0x1 (POWERON)` und anschließender USB-Host-/Displayinitialisierung. Ob Portöffnung oder ein zeitnaher Einschaltvorgang der Auslöser war, ist UNGEPRÜFT. Kein Reset-Befehl gesendet; keine Garantie eines resetfreien Verbindungsaufbaus aus diesem Test ableitbar.
- Keine Firmware geflasht und keine Dateien auf dem Gerät verändert.

Hardware-Revision, AMY-Version, Audio, AMYboard-Verbindung, Dateitransfer und Dauerstabilität bleiben UNGEPRÜFT. COM9 ist die aktuelle Windows-Zuordnung, keine dauerhafte Geräteidentität.
