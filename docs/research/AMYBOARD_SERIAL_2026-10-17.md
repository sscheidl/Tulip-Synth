# AMYboard USB-REPL – 17.10.2026

Eigentümer hat das separate AMYboard per USB an den Windows-PC angeschlossen. BELEGT: eigenes serielles USB-Gerät an COM7, USB VID CAF0 / PID 4009 / Interface 00. Tulip-COM9 aktuell nicht vorhanden.

Nur lesende Abfrage über pyserial 3.5 bei 115200 Baud / 8N1, DTR/RTS deaktiviert; Port anschließend geschlossen. Keine Firmware geflasht, keine Dateien auf dem Gerät geändert.

```python
import os, sys, tulip, amy
print(os.uname())
print(tulip.board())
print(getattr(amy, 'version', 'not exposed'))
```

## Ergebnis (BELEGT am Gerät)

- Hardwarekennung `AMYboard with ESP32S3`, Boardtyp `AMYBOARD`.
- MicroPython `1.24.0-preview`.
- Firmware-Build `82e69df-dirty on 2026-06-30`.
- `amy.version` in dieser Firmware nicht vorhanden; konkrete AMY-Version weiterhin UNGEPRÜFT.
- Bootausgabe enthält einzelne I²C-Initialisierungsmeldungen mit `returned 0xff` und eine mit `OK`. Keine Hardwarefehlerdiagnose daraus abgeleitet; Audio/CV nicht getestet.
- REPL antwortet normal. Boardrevision und Dauerstabilität UNGEPRÜFT.

Der zuvor am 17.10.2026 geprüfte [offizielle Rolling-Release](https://github.com/shorepine/tulipcc/releases/tag/amyboard) stellt Firmware und Systemdateien vom 14.10.2026 bereit (Quellstand laut Release `17d1ef1d14aa0a51520fced04c87c1328f79bbd0`). Damit ist ein neuerer offizieller Build verfügbar. Kein Updateauftrag für dieses Gerät aus dem Anschluss-/Ausleseauftrag abgeleitet; keine Sicherung oder Aktualisierung durchgeführt.
