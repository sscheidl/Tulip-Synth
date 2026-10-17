# Größeres Tulip-Menü und WLAN-Startkonfiguration – 17.10.2026

Hardware: Tulip `TULIP4_R11`, USB-REPL COM9, Firmware `82e69df-dirty on 2026-10-14`. Auftrag: Menü unten rechts fingerfreundlicher machen; später zusätzlich WLAN-Zugang dauerhaft auf dem Gerät einrichten.

## Menü

Originalbutton 52 × 37 Pixel; Originalmenü laut passendem Upstream-Code 195 × 140 Pixel mit Schriftgröße 12. Eigene Anpassung [large_menu.py](../../devices/tulip/large_menu.py) nutzt vorhandene Aktionen und LVGL; installiert nach `/user/lib`, Aufruf aus vorhandener `/user/boot.py` ergänzt. Originalstartdatei vor Änderung lokal gesichert (siehe Geräte-README), sonstige Inhalte erhalten. Keine Firmware geflasht.

BELEGT am Gerät: Button 96 × 72 Pixel, 12 Pixel Abstand vom unteren/rechten Rand; Liste 340 × 480 Pixel, Eintragsmindesthöhe 52 Pixel. Schrift Montserrat 24 vorhanden. LVGL drückte Einträge zunächst auf 38 Pixel zusammen; Mindesthöhe korrigiert und erneut 52 Pixel gemessen. Sofort nach Stiländerungen erfasste Größen waren teils noch alt; verifiziert nach `update_layout()`.

Installation auf dem Gerät bytegenau zurückgelesen. Nach Neustart `ui._large_menu_installed` wahr. Letzte Mindesthöhenkorrektur anschließend live und als Datei installiert. Menü zur Benutzerprüfung geöffnet. Fingertest, App-Wechsel und Neustart mit letzter Korrektur noch UNGEPRÜFT.

## WLAN

Auf ausdrücklichen Auftrag Netzwerkfunktion und automatischer Aufruf im persönlichen Startskript eingerichtet; temporäres Passwort ausschließlich auf dem Gerät, nicht im Repository. `ui.wifi` auf die Funktion gesetzt, damit der bestehende Wi-Fi-Menüeintrag sie ebenfalls nutzen kann. Keine Zugangsdaten in Prüfausgaben oder Repository übernommen.

Verbindung nach Neustart nicht hergestellt. Wiederholter Verbindungsversuch während bereits laufendem Versuch ergibt `Wifi Internal Error`. WLAN anschließend deaktiviert/aktiviert und erneut versucht: keine IP. Späterer Scan des Tulip findet den gewünschten Netzwerknamen nicht; Status zuvor 201, später 1001. Ursache UNGEPRÜFT, Eigentümer um Bestätigung von Netzname und 2,4-GHz-Verfügbarkeit gebeten. Persistente Einrichtung ist gespeichert, erfolgreicher WLAN-Betrieb noch nicht bestätigt.

Nachtrag Eigentümer/Screenshot: 2,4 GHz und 5 GHz aktiv, Autokanal, Wi-Fi 6, Option Autokanal inklusive 12/13 nicht ausgewählt. Screenshot zeigt keinen aktuellen Betriebskanal und keine Verschlüsselungseinstellung. Eigentümer vermutet WPA2/WPA3-Mischbetrieb oder Kanalproblem; keine bestätigte Ursache. Tulip-Scan nach `disconnect()` findet das Ziel weiterhin nicht; weitere Scans sehen 3–6 andere Einträge, darunter Kanäle 6 und 13. `network.country()` meldet `XX`, keine Änderung vorgenommen. Damit Funk grundsätzlich aktiv; kein Beleg, dass Kanal 13 generell unsichtbar wäre. Router nicht verändert.

Nächster vorgeschlagener Isolationstest: Eigentümer stellt nur die Verschlüsselung vorübergehend auf WPA2 (CCMP), dann erneut scannen/verbinden. Espressif dokumentiert grundsätzlich WPA3-/Transition-Unterstützung des ESP32-S3; daraus folgt kein Nachweis für diesen Tulip-Build. [Espressif](https://docs.espressif.com/projects/esp-idf/en/v5.1.2/esp32s3/api-guides/wifi-security.html), [FRITZ-Kompatibilitätshinweise](https://at.fritz.com/apps/knowledge-base/FRITZ-Box-4690/1079_WLAN-Sicherheitseinstellungen-der-FRITZ-Box-andern). Kein Bedarf, das Netz dafür zu öffnen.

Weitere Screenshots bestätigen getrennten 2,4-GHz-Netznamen, WPA2/WPA3 und aktivierte Kompatibilitätsoption. Späterer Tulip-Scan sieht das gewünschte Netz erstmals wieder: Kanal 13, RSSI ca. -80 dBm, Authentifizierung 3 gemeldet. Damit Netzname korrekt, Empfang jedoch schwach; Screenshot der Autokanalauswahl beweist nicht den tatsächlichen aktuellen Kanal aller Zugangspunkte. Erneuter Verbindungsversuch ohne Routeränderung: keine IP, Status 201. Laufzeit-Ländercode testweise von `XX` auf `DE` gesetzt, WLAN neu aktiviert: weiterhin keine IP. Keine Änderung der dauerhaften Länder-/Routerkonfiguration. Ursache weiterhin offen. Daher nächster Vorschlag geändert: zuerst Router-2,4-GHz testweise fest auf Kanal 1 stellen, Verschlüsselung zunächst beibehalten, um Kanal und Verschlüsselung getrennt zu prüfen. Noch nicht durchgeführt.

## Erfolgreicher Abschluss nach Neustart

Eigentümer korrigiert das temporäre Passwort und bestätigt Kanal 1. Zugangsdaten ausschließlich im lokalen Geräte-Startskript korrigiert und bytegenau geprüft; überholtes lokales temporäres Konfigurationsskript mit altem Passwort entfernt. Direktes Verbinden zunächst weiter ohne IP. Einmaliger kurzzeitiger COM9-Zugriffsfehler, anschließend Port wieder erreichbar.

Auf Wunsch Neustart mit `machine.reset()`. Danach BELEGT: automatische Verbindung aus `/user/boot.py`, DHCP-Adresse vorhanden, Station-Status 1010; `ui._large_menu_installed == True`. Erfolg bei vom Eigentümer auf Kanal 1 gesetztem Router und zuletzt gezeigtem WPA2/WPA3-Modus (keine spätere Änderung der Verschlüsselung mitgeteilt). Passwortkorrektur, Kanaländerung und Neustart nicht einzeln isoliert; keine eindeutige Fehlerursache behauptet. WLAN-Dauerbetrieb und Grafikstabilität bei WLAN weiter durch Eigentümer zu beobachten. Kein Kennwort im Repository.

Menü nach Neustart geöffnet: Eintragsmindesthöhe erneut 52 Pixel bestätigt; bei verbundenem WLAN `tulip.fps()` = 43,59198. Menü bleibt zur Fingerprüfung geöffnet. Das ist kein Nachweis eines glitchfreien Bildes.

## Erneute Grafik- und Touchprobleme

Eigentümer meldet Menü per Finger nicht nutzbar, Touch reagiert falsch, erneut Display-Glitches. WLAN ausschließlich zur Laufzeit ausgeschaltet, Menü und Displaytakt unverändert. Abschließende eindeutige Auswahl des Eigentümers: „Glitches weg, Touch weiterhin falsch“ (ersetzt die zuvor gesendete Zahl 3). Das spricht für getrennt zu prüfende Probleme, beweist jedoch noch keine bestimmte WLAN-/Displayursache.

Auf ausdrücklichen Wunsch WLAN aktiviert belassen und erneut neu gestartet. Danach BELEGT: automatische WLAN-Verbindung mit IP, 43,61289 FPS, Menüanpassung geladen. Ausgelesene unveränderte Touch-Kalibrierung `(-2, -12, 0.8)` entspricht den voreingestellten GT911-Werten des Upstream-Codes; ohne gezielte Koordinatenmessung keine Korrektur vorgenommen. Visuelle Grafikstabilität nach diesem Neustart und Ursache des Touchfehlers weiterhin UNGEPRÜFT. Menüanpassung damit noch nicht als praktisch nutzbar abgenommen.


## Menü öffnet per Touch nicht: Callback-Korrektur

Eigentümer meldet ausdrücklich: Menü lässt sich per Touch nicht öffnen. BELEGT am Tulip TULIP4_R11, COM9, unveränderte Firmware vom 14.10.2026: alter Button hat drei Ereignisregistrierungen; `remove_event_cb()` liefert sowohl für den Original- als auch den Ersatzcallback `False`. Synthetisches `button.send_event(lv.EVENT.CLICKED, None)` lässt das Menü geschlossen. Zusammen mit der Registrierung im eigenen Code spricht dies für doppeltes Umschalten; ein physischer Touch-Ereignisverlauf wurde nicht aufgezeichnet.

Korrektur: Originalbutton löschen und durch einen Button mit einmal registriertem Menücallback ersetzen. Vor erneutem `draw_task_bar()` den bisherigen REPL-Button löschen, da Upstream jedes Mal einen neuen erzeugt. Keine Änderung an Bootdatei, WLAN, Touchkalibrierung oder Firmware. Vorherige Menüdatei lokal unter `C:/Users/ssche/Tulip-Synth-Backups/Tulip-menu-2026-10-17/large_menu-before-fix.py` gesichert. Neue Datei bytegenau auf dem Gerät verifiziert.

BELEGT nach Neustart: zwei gesamte Ereignisregistrierungen am neuen Button (eins weniger als zuvor); synthetischer Klick öffnet, zweiter schließt. Nach `ui.repl_screen.present()` genau ein Kind im REPL-Container und weiterhin zwei Ereignisregistrierungen. Die Gesamtzahl enthält LVGL-interne Registrierungen und ist nicht mit der Zahl eigener Menücallbacks gleichzusetzen. Praktische Fingerbedienung, echter App-Wechsel und Dauertest weiterhin **UNGEPRÜFT**. Grafikproblem bleibt separat offen.
