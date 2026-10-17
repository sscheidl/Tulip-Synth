# Größeres Tulip-Menü und WLAN-Startkonfiguration – 17.10.2026

Hardware: Tulip `TULIP4_R11`, USB-REPL COM9, Firmware `82e69df-dirty on 2026-10-14`. Auftrag: Menü unten rechts fingerfreundlicher machen; später zusätzlich WLAN-Zugang dauerhaft auf dem Gerät einrichten.

## Menü

Originalbutton 52 × 37 Pixel; Originalmenü laut passendem Upstream-Code 195 × 140 Pixel mit Schriftgröße 12. Eigene Anpassung [large_menu.py](../../devices/tulip/large_menu.py) nutzt vorhandene Aktionen und LVGL; installiert nach `/user/lib`, Aufruf aus vorhandener `/user/boot.py` ergänzt. Originalstartdatei vor Änderung lokal gesichert (siehe Geräte-README), sonstige Inhalte erhalten. Keine Firmware geflasht.

BELEGT am Gerät: Button 96 × 72 Pixel, 12 Pixel Abstand vom unteren/rechten Rand; Liste 340 × 480 Pixel, Eintragsmindesthöhe 52 Pixel. Schrift Montserrat 24 vorhanden. LVGL drückte Einträge zunächst auf 38 Pixel zusammen; Mindesthöhe korrigiert und erneut 52 Pixel gemessen. Sofort nach Stiländerungen erfasste Größen waren teils noch alt; verifiziert nach `update_layout()`.

Installation auf dem Gerät bytegenau zurückgelesen. Nach Neustart `ui._large_menu_installed` wahr. Letzte Mindesthöhenkorrektur anschließend live und als Datei installiert. Menü zur Benutzerprüfung geöffnet. Fingertest, App-Wechsel und Neustart mit letzter Korrektur noch UNGEPRÜFT.

## WLAN

Auf ausdrücklichen Auftrag Netzwerkfunktion und automatischer Aufruf im persönlichen Startskript eingerichtet; temporäres Passwort ausschließlich auf dem Gerät, nicht im Repository. `ui.wifi` auf die Funktion gesetzt, damit der bestehende Wi-Fi-Menüeintrag sie ebenfalls nutzen kann. Keine Zugangsdaten in Prüfausgaben oder Repository übernommen.

Verbindung nach Neustart nicht hergestellt. Wiederholter Verbindungsversuch während bereits laufendem Versuch ergibt `Wifi Internal Error`. WLAN anschließend deaktiviert/aktiviert und erneut versucht: keine IP. Späterer Scan des Tulip findet den gewünschten Netzwerknamen nicht; Status zuvor 201, später 1001. Ursache UNGEPRÜFT, Eigentümer um Bestätigung von Netzname und 2,4-GHz-Verfügbarkeit gebeten. Persistente Einrichtung ist gespeichert, erfolgreicher WLAN-Betrieb noch nicht bestätigt.
