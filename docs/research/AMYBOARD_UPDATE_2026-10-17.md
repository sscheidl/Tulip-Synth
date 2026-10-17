# AMYboard OTA-Update – 17.10.2026

## Auftrag, Ausgangszustand und Recovery

Eigentümer beauftragt Update des separaten AMYboards ausdrücklich und verzichtet anschließend ausdrücklich auf eine Sicherung. Ausgangszustand BELEGT: `AMYBOARD`, COM7, MicroPython `1.24.0-preview`, Build `82e69df-dirty on 2026-06-30`, `amy.version` fehlt. Details im [seriellen Prüfbericht](AMYBOARD_SERIAL_2026-10-17.md).

Vor Verzicht wurde eine Sicherung versucht: `mpremote fs cp` meldete ein nicht kopiertes Verzeichnis, esptool konnte den ROM-Downloadmodus nicht verbinden. Keine erfolgreiche Sicherung, kein Flash durch diese Versuche. Lokal außerhalb des Git wurde ein Backup-Verzeichnis angelegt; keine Backup-Vollständigkeit behauptet.

Geplanter Weg: offizielle `amyboard.upgrade()`-OTA einschließlich Systemdateien über das vorübergehend offene WLAN; keine WLAN-Zugangsdaten ins Git. Quelle: [Herstelleranleitung](https://github.com/shorepine/tulipcc/blob/main/docs/amyboard/firmware.md), geprüft 17.10.2026.

Recovery vor Update dokumentiert: beide seitlichen Tasten halten, RST zuerst loslassen, dann BOOT. Danach über USB mit Web-Upgrader oder esptool das passende vollständige `amyboard-full-AMYBOARD.bin` aus dem [offiziellen Release](https://github.com/shorepine/tulipcc/releases/tag/amyboard) an Adresse `0x0` schreiben. Vollflash löscht Gerätedaten; kein vollständiger Recovery-Test durchgeführt. Manuelle Betätigung der Tasten wäre bei nicht automatisch erreichbarem Bootloader nötig. Keine Sicherung zur Wiederherstellung des alten Stands vorhanden.

## Status

Update über USB abgeschlossen (Abschlussprüfung unten). Audio, CV, SD und Tulip-I²C-Verbindung weiterhin UNGEPRÜFT.

## Vorbereitung USB-Update

WLAN-Scan sieht das gewünschte Netz mit Authentifizierung 3 (WPA2); offene Verbindung daher nicht möglich. Keine Zugangsdaten angefordert/gespeichert. Statt WLAN-OTA offizielles Update über USB mit erhaltener User-Partition vorgesehen.

BELEGT über Partitionsabfrage: laufend `ota_0` bei 0x10000, freie `ota_1` bei 3.801.088 (0x3a0000), jeweils 3.735.552 Bytes; `system` bei 7.536.640 (0x730000), 3.145.728 Bytes; `vfs` bei 10.682.368, 4.390.912 Bytes. Ziel nur freie Firmwarepartition und Systempartition. Bootumschaltung erst nach erfolgreichem Schreiben/Verifizieren; keine Löschung des ganzen Flash.

Offizielle Assets vom 14.10.2026 lokal im Windows-Temp-Verzeichnis heruntergeladen, SHA-256 jeweils identisch zum Release-Digest:

- `amyboard-firmware-AMYBOARD.bin`: `6d64152613604e3c59e46d266e11e8c2ef658c51bfa1544b6029c2d04867ca82`.
- `amyboard-sys.bin`: `bbd7843981c2e2562f9711717f1314893299869e17386b5e3a76c56401c4ff7a`.

Diese Binaries bleiben außerhalb des Git. Wechsel in ROM-Downloadmodus über vorhandenes `machine.bootloader()` vorgesehen; bei USB-Neuerkennung COM-Port neu zuordnen. Vollflash-Recovery mit Tasten bleibt Rückfallweg, kein zusätzlicher Auftrag nötig für das bereits freigegebene offizielle Update.

## USB-Schreibvorgang

`machine.bootloader()` erfolgreich: ROM-Port COM10, VID 303A / PID 0009. esptool 5.6.0 verbindet ESP32-S3, Chiprevision v0.2, 8 MB PSRAM. Offizielle Firmware bei 0x3a0000 und Systemdateien bei 0x730000 geschrieben; esptool bestätigt beide Male `Hash of data verified`. Kein Schreiben in `vfs`, Bootloader oder Partitionstabelle. Automatischer RTS-Reset führt nicht zu wieder erreichbarem COM7; COM10 lässt sich danach nicht konfigurieren. Eigentümer um einmaligen RST-Tastendruck gebeten. Aktivierung von `ota_1` und Abschlussprüfung noch ausstehend; nicht als abgeschlossen melden.

## Relevante Neuerungen laut Upstream (auf unserem Gerät funktional UNGEPRÜFT)

- [I²C-Nachrichtenframing, PR 1345](https://github.com/shorepine/tulipcc/pull/1345): fragmentierte/lange Nachrichten korrekt zusammensetzen, wichtig für spätere Tulip-Steuerung.
- [WAV-Export, PR 1399](https://github.com/shorepine/tulipcc/pull/1399): RAM-PCM-Presets als 16-Bit-WAV speichern; SD bevorzugt, internes Flash kann Audio unterbrechen.
- [GPIO-Interrupt-Korrektur, PR 1361](https://github.com/shorepine/tulipcc/pull/1361): gültigen MicroPython-Taskhandle setzen, vermeidet beschriebenen Reset bei Pin-Interrupts.
- [Encoder, PR 1363](https://github.com/shorepine/tulipcc/pull/1363): kürzere Seesaw-Abfragewartezeiten; Herstellerprüfung auf bestimmtem Zubehör, keine Garantie für jedes Encoderboard.
- [CV-Eingänge, PR 1347](https://github.com/shorepine/tulipcc/pull/1347): zeitnähere Abtastung beider Kanäle und bessere I²C-Fehlerbehandlung.
- Weitere gemeinsame AMY-Änderungen: zwei Modulationsquellen und PCM-Loop-Modi; siehe Tulip-Updatebericht. Alte eigene Skripte müssen ggf. von `time=` auf `ticks=` sowie auf `loop(tick)` umgestellt werden.

## Abschlussprüfung (BELEGT am Gerät)

Nach bestätigtem RST-Tastendruck des Eigentümers lief die alte Firmware wieder an COM7. `get_next_update().set_boot()` und `machine.reset()` aktiviert die zuvor geschriebene `ota_1`. Verbindungsabbruch beim Reset erwartet; Windows vergibt anschließend COM11 (gleiche VID/PID, neue Geräteinstanz).

Per `mpremote connect COM11 resume exec ...` ausgelesen:

- Board `AMYBOARD`, MicroPython `1.24.0-preview`.
- Build `82e69df-dirty on 2026-10-14`.
- `amy.version` = `1.2.200`.
- Laufende Partition `ota_1`, Offset 0x3a0000, Größe 3.735.552 Bytes.
- `tulip.store_sample` vorhanden; kein WAV-Export ausgeführt.
- `/sys` lesbar (`ex`), `/user` weiterhin drei Verzeichniseinträge. Kein vollständiger Vorher-/Nachher-Inhaltsvergleich; User-Partition wurde nicht beschrieben.
- Kein WLAN eingerichtet; kein Backup gemäß ausdrücklichem Verzicht. Port nach Prüfung freigegeben.

Funktionale Audio-/CV-/SD-/I²C-Prüfung und Dauertest stehen aus. Updateerfolg bedeutet hier verifiziertes Schreiben und erfolgreichen Start/REPL des neuen Builds.
