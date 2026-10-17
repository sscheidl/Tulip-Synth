# Tulip WLAN und offizielles OTA-Update – 17.10.2026

## Auftrag und Ausgangszustand

Eigentümer beauftragt WLAN-Verbindung und Firmwareupdate ausdrücklich. Sicherung auf ausdrücklichen Folgeauftrag übersprungen: Gerät laut Eigentümer noch blank. Diese Ausnahme gilt für diesen Vorgang; D012 bleibt für weitere Firmwarearbeiten bestehen. Keine Sicherung vorhanden.

Gerät meldet `TULIP4_R11`, COM9 / CH340K, 115200 Baud. Vorher MicroPython `1.24.0-preview`, Build `82e69df-dirty on 2026-07-08` (BELEGT per REPL).

## Verfahren und Wiederherstellung

Offizieller Weg: `tulip.wifi(ssid, '')` für das vorübergehend offene WLAN, danach `tulip.upgrade()`, Firmware und `/sys` jeweils bestätigt. Keine Zugangsdaten ins Repository geschrieben. WLAN-Verbindung mit DHCP-Adresse erfolgreich (BELEGT). Keine Änderung an `boot.py` zur automatischen WLAN-Verbindung vorgenommen.

Quelle: [offizielle Flash-/OTA-Anleitung](https://github.com/shorepine/tulipcc/blob/main/docs/tulip_flashing.md), abgerufen 17.10.2026. Hersteller beschreibt OTA mit Erhalt von `/user` und empfiehlt Firmware und Systemdateien gemeinsam zu aktualisieren.

Recovery bei fehlgeschlagenem Boot: am UART-USB-Port des Makerfabs-Tulip mit Espressif esptool verbinden; erforderlichenfalls BOOT beim Reset halten, um den ROM-Downloadmodus zu erreichen. Passendes vollständiges `tulip-full-TULIP4_R11.bin` aus dem [offiziellen Rolling-Release](https://github.com/shorepine/tulipcc/releases/tag/tulip) an Adresse `0x0` schreiben. Vollflash überschreibt Gerätedaten. Nur nach gesonderter Bewertung bei tatsächlichem Fehler verwenden. BOOT-/Reset-Recovery am eigenen Gerät UNGEPRÜFT; kein Recovery-Flash ausgeführt. Host-Werkzeug esptool 5.6.0 vorhanden.

## Verlauf

- `mpremote ... resume exec` konnte den Raw-REPL nicht erreichen; beendet, danach normale REPL über pyserial 3.5 erfolgreich.
- OTA meldet Firmware und `/sys` jeweils `2026-10-14T18:14:15Z`.
- Firmware und `/sys` zum Update bestätigt. Beide melden `Write done`; Bootpartition auf `ota_1` gesetzt, automatischer Neustart erfolgt (BELEGT).
- Host-Monitor scheiterte beim Ausgeben der Neustartbytes an Windows-cp1252 (`UnicodeEncodeError`). Anschließend Verbindung mit UTF-8-Ausgabe erneut hergestellt; kein erneuter Flash nötig.

## Abschlussprüfung (BELEGT am Gerät)

- REPL nach Neustart wieder erreichbar.
- `os.uname().version`: `82e69df-dirty on 2026-10-14`, MicroPython weiterhin `1.24.0-preview`.
- Board: `TULIP4_R11`; laufende Partition `ota_1`, Größe 3.735.552 Bytes.
- `/sys` lesbar, enthält `ex` und `im`. Keine vollständige Integritätsprüfung aller Systemdateien durchgeführt.
- WLAN nach Neustart zunächst nicht verbunden; erneut erfolgreich mit dem offenen WLAN verbunden. Kein automatischer Wiederverbindungsaufruf in `boot.py` hinterlegt, da das offene Netz nur vorübergehend ist.
- `dirty` ist Teil der Build-Versionskennung, bereits vor dem Update vorhanden. Kein Beleg für beschädigte Firmware; genaue Abweichungen des Build-Quellbaums vom genannten Commit aus der Versionszeile UNGEPRÜFT.
- Audio, Touch-Bedienung und Dauertest noch UNGEPRÜFT.

## Bildwiederholrate nach Update (17.10.2026)

BELEGT am selben Tulip (`TULIP4_R11`, Build `82e69df-dirty on 2026-10-14`), normale REPL an COM9: drei Aufrufe von `tulip.fps()` im Abstand von zwei Sekunden ergeben `43.61099`, `43.60529` und `43.59768` FPS. Damit aktuell rund 43,6 FPS bzw. rechnerisch 22,9 ms pro Frame. Aktueller Bildschirmzustand, kein Animations-/Lastbenchmark; keine Anzeigeeinstellung geändert.

Einordnung aus [modtulip.c](https://github.com/shorepine/tulipcc/blob/main/tulip/shared/modtulip.c) und [esp32s3_display.c](https://github.com/shorepine/tulipcc/blob/main/tulip/esp32s3/esp32s3_display.c), main abgerufen 17.10.2026: `fps()` liefert `reported_fps`, berechnet über Frame-Synchronisationsintervalle. Das ist eine firmwareseitige Displayrate, keine Garantie der Aktualisierungsrate einer bestimmten Python-/LVGL-Animation; keine externe Messung am Panel.
