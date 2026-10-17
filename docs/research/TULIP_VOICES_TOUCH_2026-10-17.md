# Voices: Notenhänger bei Touch – 17.10.2026

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
