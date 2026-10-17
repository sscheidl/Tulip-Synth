# Voices: Notenhänger bei Touch – 17.10.2026

Aktueller Endstand: Korrektur direkt in der bearbeitbaren App /sys/ex/voices.py installiert. Kein Voices-Eintrag in boot.py, kein zusätzlicher Laufzeitadapter erforderlich. Frühere Laufzeittestabschnitte unten dokumentieren die Vorgeschichte.

Hardware: Tulip CC TULIP4_R11, COM9/115200, Firmware 82e69df-dirty vom 14.10.2026, AMY 1.2.200. Keine Firmwareänderung.

## Beobachtungen

BELEGT durch Eigentümer: Menü öffnet nach Callback-Korrektur per Finger („geht soweit“). In Voices treten bei schnellen Touch-Tastenfolgen sofort Notenhänger auf, vor allem beim Gleiten und mit mehreren Fingern. Vermutung des Eigentümers: Überlastung durch erhöhte Bildwiederholrate.

BELEGT durch kurze REPL-Abfragen in laufender Voices-App: Displaytakt 36 MHz, 43,61099 FPS (Standardtakt), CPU 22,99505 und GPU 38,59573 Prozent. Einzelwerte außerhalb kontrollierter Spiellast; keine Aussage über Lastspitzen. Kanalindex 0, Polyphonieindex 5, Hold-Schalter Zustand 0. app.held_note enthält vier wahre Einträge: 65, 67, 69, 71. Das belegt verbliebene Softwarezustände, keine eigene Audiomessung.

## Quellcodebefund

[Upstream Voices](https://github.com/shorepine/tulipcc/blob/main/tulip/shared/py/voices.py), main abgerufen 17.10.2026: touch(up) interpretiert die aktuellen Koordinaten als Noten; play_note_from_coord() schaltet bei Freigabe nur diese Noten aus. Beim Gleiten können frühere Noten eingeschaltet bleiben. Der GT911-Treiber aktualisiert laufend die Koordinaten; beim Übergang auf keine Finger wird eine globale Freigabe gemeldet. Der Notenbestand muss auch beim Gleiten und abnehmender Fingerzahl abgeglichen werden.

Voices ist auf dem Gerät eingefroren (Suchpfad .frozen); kein bytegleicher Vergleich mit Upstream erfolgt. Kein physischer Ereignisverlauf aufgezeichnet. Befund passt zur Eigentümerbeobachtung, beweist aber nicht die Ursache sämtlicher Hänger. Einfluss von Last, WLAN oder verlorenen Ereignissen weiterhin UNGEPRÜFT.

## Begrenzter Laufzeittest

Eigene Anpassung devices/tulip/voices_touch.py verwendet vorhandene Geometrie, Touch-Callback und Synth-API; kein Upstream-Code kopiert. Gleicht pro Touch-Snapshot gewünschte und aktive Noten ab. Globale Freigabe beendet alle eigenen Noten. Note-Off geht an die ursprüngliche Synth-Instanz. Deaktivieren/Beenden gibt eigene Noten frei. Beim einmaligen Installieren werden die bisher als gehalten markierten Noten des ausgewählten Kanals freigegeben.

Vier Hosttests bestanden: Gleiten/Endfreigabe, Teilfreigabe eines Akkords und wiederholte Samples, Kanalwechsel mit Freigabe des ursprünglichen Synths, Verlassen der Tastatur einschließlich rechter Randgrenze. Simulierte Koordinaten; keine Echtzeit-/Audioprüfung.

BELEGT am Gerät: neue Datei /user/lib/voices_touch.py installiert, SHA-256 verglichen, apply() ohne Ausnahme ausgeführt, anfänglich null eigene aktive Noten. Bootdatei, WLAN, Displaytakt und Touchkalibrierung unverändert. Kein automatischer Start. Neustart entfernt die Laufzeitinstallation; die unbenutzte Datei verbleibt. Erneuter Test: zuerst Voices öffnen, dann import voices_touch; voices_touch.apply().

**Ausstehend / UNGEPRÜFT:** Eigentümer wiederholt schnelle Folge, Gleiten und Mehrfingerbedienung bei unverändertem Standardtakt. Keine erfolgreiche praktische Fehlerbehebung behauptet. Erst danach gegebenenfalls kontrollierter Taktvergleich mit identischem Patch, Polyphonie und WLAN-Zustand.

## Praktische Bestätigung

BELEGT durch Eigentümer nach aktiviertem Laufzeittest: „super - fehler behoben. Liegt nicht an Displayfrequenz“. Die Touch-Notenkorrektur beseitigt den gemeldeten Fehler bei unverändertem Displaytakt; eine Taktreduktion ist für diesen Fehler nicht erforderlich. Kein zusätzlicher Taktvergleich nötig. Damit praktische Wirksamkeit für den gemeldeten Bedienfall bestätigt, kein allgemeiner Last- oder Dauertest. Das separate Grafik-/WLAN-Problem bleibt offen. Korrektur weiterhin nur zur Laufzeit aktiv; keine Bootintegration vorgenommen.

## Dauerhafte direkte App-Korrektur

Eigentümer beauftragt dauerhafte Integration und präzisiert: App direkt verbessern, keine Voices-Anpassung in boot.py. Ein zwischenzeitlich ergänzter Voices-Boot-Aufruf wurde vollständig zurückgenommen. SHA-256 der verbleibenden Bootdatei stimmt mit der unmittelbar zuvor lokal gesicherten Datei überein. Sicherung mit persönlichen Einstellungen ausschließlich lokal unter C:/Users/ssche/Tulip-Synth-Backups/Tulip-menu-2026-10-17/boot-before-voices.py. Keine Zugangsdaten ausgegeben oder ins Repository übernommen.

Tulips run() entfernt bestehende Modulimporte und lädt die App neu; ein Boot-Monkeypatch ist deshalb auch technisch ungeeignet. Der vorhandene Startweg wählt /sys/ex als Arbeitsverzeichnis, wenn dort voices.py liegt, und importiert die bearbeitbare Datei vor dem eingefrorenen Modul. BELEGT am Gerät durch Vorhandensein der neuen _active-Notenverwaltung und durch nicht geladenen voices_touch-Adapter.

Direkte App basiert auf shorepine/tulipcc@17d1ef1d14aa0a51520fced04c87c1328f79bbd0, tulip/shared/py/voices.py, MIT. Lizenz vollständig in devices/tulip/LICENSE.tulipcc. Eingefrorener Gerätecode nicht bytegleich verglichen. Nur Touch-Notenverwaltung und Freigabe bei Aktivieren/Deaktivieren/Beenden geändert; UI und Synth-Auswahl aus Upstream übernommen. Die vier Hosttests prüfen jetzt die Funktionen der direkten App statt des früheren Adapters.

BELEGT: /sys/ex/voices.py und LICENSE.voices-tulipcc neu angelegt (vorher keine bearbeitbare voices.py vorhanden), Übertragung jeweils per SHA-256 geprüft. Nach Neustart normaler Aufruf tulip.run('voices') erfolgreich, neue Notenverwaltung und Aktivierungscallback vorhanden. Schließen und erneutes Öffnen ebenfalls erfolgreich. voices_touch nicht in sys.modules. Display weiterhin 36 MHz / 43,60719 FPS. Kein Firmwareflash, WLAN unverändert. Nach Systemdatei-Updates lokale App prüfen und bei Überschreiben erneut installieren. Abschließender erneuter Finger-/Dauertest der direkt integrierten Variante bleibt UNGEPRÜFT; die zugrunde liegende Notenlogik wurde zuvor praktisch bestätigt.
