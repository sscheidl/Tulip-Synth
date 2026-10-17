# Persönliche Tulip-Anpassung: größeres Menü

`large_menu.py` kommt auf den Tulip nach `/user/lib/large_menu.py`. In `/user/boot.py`:

```python
import large_menu
large_menu.apply()
```

Vergrößert den vorhandenen REPL-Launcher auf 96 × 72 Pixel (12 Pixel Rand), die Liste auf 340 × 480 Pixel und ihre Zeilen auf mindestens 52 Pixel. Nutzt die vorhandenen Menüaktionen, Schrift bevorzugt Montserrat 24. Die Liste bleibt scrollbar. Änderung wird auch nach Rückkehr aus Apps auf die Menüschaltfläche angewandt. Keine Firmwareänderung.

Am 17.10.2026 auf Tulip `TULIP4_R11`, Build `82e69df-dirty on 2026-10-14`, geometrisch per REPL geprüft; Startintegration und 52-Pixel-Zeilen nach Neustart bestätigt. Fingertest, App-Wechsel und Dauerbetrieb noch UNGEPRÜFT. `ui`-Interna sind versionsabhängig; bei künftigem Firmwareupdate erneut prüfen.

Rücknahme: die beiden Aufrufe aus `/user/boot.py` entfernen und neu starten. Nicht das gesamte Startskript ersetzen: es kann persönliche Einstellungen und WLAN-Zugangsdaten enthalten. Bei Startproblemen BOOT halten und Reset auslösen, um den ESP32-ROM-Downloadmodus zu erreichen; dadurch lässt sich die Bootdatei allerdings noch nicht direkt reparieren. Ein vollständiger Firmware-Recovery-Flash wäre ein separater, datenlöschender Rückfallweg. Vor Startskriptänderungen lokal sichern.

Die ursprüngliche Startdatei liegt lokal außerhalb des Git unter `C:\Users\ssche\Tulip-Synth-Backups\Tulip-menu-2026-10-17\boot-before.py`. Sie entstand vor Einrichtung des WLAN-Passworts. Keine Zugangsdaten in dieses Repository übernehmen.

API-Herkunft: eigene dünne Anpassung um die vorhandenen Klassen/Funktionen aus [shorepine/tulipcc ui.py](https://github.com/shorepine/tulipcc/blob/17d1ef1d14aa0a51520fced04c87c1328f79bbd0/tulip/shared/py/ui.py) (MIT). Kein Upstream-Code kopiert. Keine neue Abhängigkeit.

Callback-Korrektur 17.10.2026: Der Originalbutton wird ersetzt, weil `remove_event_cb()` auf dem Gerätebuild die Python-Callbacks nicht entfernt. Synthetisches Öffnen/Schließen nach Neustart und erneutes REPL-Anzeigen geprüft; tatsächliche Touchbedienung weiterhin **UNGEPRÜFT**. Details im [Prüfbericht](../../docs/research/TULIP_MENU_WIFI_2026-10-17.md).
