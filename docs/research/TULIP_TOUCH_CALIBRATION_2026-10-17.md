# Tulip-Touch-Kalibrierungsversuch – 17.10.2026

Gerät: TULIP4_R11, Firmware `82e69df-dirty on 2026-10-14`, COM9. Auftrag: Touch messen und gegebenenfalls kalibrieren. WLAN auf Wunsch eingeschaltet belassen. Keine Firmwareänderung.

## Methode

Eigene kleine LVGL-Messoberfläche: [touch_calibration.py](../../devices/tulip/touch_calibration.py). Fünf Zielpunkte, Berührung beim Loslassen über `tulip.touch()` erfasst. Ganzer Hintergrund nimmt Eingaben an; dadurch erfordert das Messen noch keine korrekt zugeordneten kleinen Buttons. Keine Touch-Callback-Übernahme und keine gespeicherten Zugangsdaten in der Messsoftware. API-Herkunft: bestehende Tulip-/LVGL-Schnittstellen; eigener Code, keine Upstream-Implementierung kopiert.

Erster Startversuch hatte falschen LVGL-Methodennamen `clear_flag`; auf das vorhandene `remove_flag` korrigiert. Eigentümer meldete nach seriellen Code-/Scrollausgaben erneut unsynchrones Bild. Auf Wunsch vor jeder tatsächlichen Messung sauberer Neustart mit temporärem Autostart des Tests. Zwei Durchgänge erfolgreich abgeschlossen. Damit Eingabeereignisse an fünf Bildpositionen BELEGT, nicht die Stabilität unter beliebiger Last.

## Messwerte (BELEGT, Positionen in Pixeln)

| Ziel x,y | Originalmessung x,y | Kontrollmessung mit Testwerten x,y |
|---|---|---|
| 120,100 | 134,91 | 131,110 |
| 904,100 | 906,100 | 902,96 |
| 512,300 | 523,296 | 516,295 |
| 120,500 | 130,508 | 131,492 |
| 904,500 | 897,508 | 893,491 |

Originalparameter `tulip.touch_delta()` = `(-2, -12, 0.8)`.

Aus den vier äußeren Originalpunkten berechnet: mittlere X-Korrektur und lineare Regression für Y; der mittlere Punkt dient zur zusätzlichen Kontrolle. Upstream-Zuordnung ist `x = raw_x + dx`, `y = (raw_y + dy) * scale` mit anschließender Begrenzung aufs Display. Daraus Testparameter `(-7, -2, 0.775573)`. X-Skalierung kann diese API nicht einstellen. Quelle: [gt911_touchscreen.c](https://github.com/shorepine/tulipcc/blob/17d1ef1d14aa0a51520fced04c87c1328f79bbd0/tulip/esp32s3/gt911_touchscreen.c).

Radialer RMS-Abstand Ziel zu Messung: Original 11,79 Pixel, Kontrollmessung 11,57 Pixel. Maximale Einzelachsenabweichung 14 bzw. 11 Pixel. Die kleine Änderung liefert bei einem Fingertipp pro Punkt keine belastbare praktische Verbesserung; keine Wiederholstatistik und keine Laborgenauigkeit behauptet. Kein großer einheitlicher Versatz in diesen fünf Punkten nachgewiesen. Ursachen des weiterhin gemeldeten Menüproblems und der Glitches bleiben offen.

## Abschluss

Temporären Kalibrierungsblock aus `/user/boot.py` wieder entfernt und Datei bytegenau geprüft; WLAN und Menüstart unverändert erhalten. Normaler Neustart durchgeführt. Abschließend BELEGT: Firmware-Standard `(-2,-12,0.8)` wieder aktiv, aktueller Bildschirm `repl`, kein automatischer Test mehr. WLAN hatte bei dieser Abfrage keine IP; seine Startkonfiguration wurde nicht entfernt oder deaktiviert. Messmodul verbleibt als manuell startbare Datei unter `/user/lib`.
