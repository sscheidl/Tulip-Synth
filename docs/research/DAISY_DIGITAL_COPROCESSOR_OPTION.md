# Forschungsoption: Seed3 + Seed 1.2 als digitaler DSP-Koprozessor

Stand: 11.10.2026. **UNGEPRÜFT – Machbarkeitsoption für M7 (optional), keine Bauanleitung, keine bestätigte Funktion und keine Architekturentscheidung.** D009/D010/D014 gelten weiter; M1 und Version 1.0 hängen nicht davon ab.

## 1. Zu prüfende Idee

Der Daisy Seed3 im Desktop Dev Kit könnte die analogen Audioein-/ausgänge über seinen Codec bedienen und digital mit einem älteren Daisy Seed 1.2 kommunizieren. Der Seed 1.2 wäre ausschließlich DSP-Koprozessor für zusätzliche Stimmen, Layer oder Effekte. Sein eigener Codec wäre im Zielbild nicht Teil des Audiowegs; ob und wie dessen Initialisierung und Taktversorgung entfallen können, ist **UNGEPRÜFT**. Es müssen konzeptionell nicht beide Codecs für analoge Audio-I/O genutzt werden. Ein Qualitätsvorteil des Seed3-Codecs wird hier nicht behauptet.

```text
Analog In → [Seed3: Codec, lokale Engine, digitales Mixing] → Analog Out
                              ⇅ digitaler Audiotransfer (UNGEPRÜFT)
                  [Seed 1.2: zusätzliche Engine / FX]

Seed3 ⇄ bidirektionale Steuerdaten (UNGEPRÜFT) ⇄ Seed 1.2
```

Bei zusätzlichen Stimmen könnte zunächst Seed 1.2 → Seed3 genügen; für Send-/Return-Effekte wäre Audio in beiden Richtungen erforderlich. Steuerdaten bleiben ein eigener logischer Weg. Tulip bleibt GUI-/Steuerzentrale und transportiert gemäß D003 kein Audio. Es gibt weder einen automatischen Verbund noch einen implementierten Scheduler.

## 2. SAI2/I²S und Pin-Kandidaten

**BELEGT nur als Software-Referenz:** Das offizielle libDaisy-Beispiel [ExternalCodec.cpp](https://docs.daisy.audio/libDaisy-Examples/ExternalCodec_8cpp_source/) konfiguriert SAI2 mit `D26` als `sa`, `D27` als `fs` und `D28` als `sck`; außerdem `D25` als `sb` und `D24` als `mclk`. Es verbindet den externen SAI-Handle mit dem lokalen Audio-Handle. Das Beispiel ist kein Nachweis für die Kombination Seed3 Desktop Dev Kit + Seed 1.2.

| Kandidat | Denkbare Rolle aus dem Beispiel | Offener Konflikt am Desktop Dev Kit |
|---|---|---|
| D26 | Datenleitung (`sa`) | MUX-/Schalter-Belegung aus der bisherigen Diskussion; genaue Netze **UNGEPRÜFT** |
| D27 | Frame-/Word-Clock (`fs`) | MUX-/Schalter-Belegung aus der bisherigen Diskussion; genaue Netze **UNGEPRÜFT** |
| D28 | Bit-Clock (`sck`) | MUX-/Schalter-Belegung aus der bisherigen Diskussion; genaue Netze **UNGEPRÜFT** |
| D25, ggf. D24 | zweite Datenrichtung, ggf. Master-Clock | Erreichbarkeit, Belegung und tatsächlicher Bedarf **UNGEPRÜFT** |

**D26/D27/D28 sind keine freigegebene Anschlussbelegung.** Drei Kandidaten allein belegen weder einen vollständigen Duplex-Audioweg noch eine passende Clock-Topologie. `sa`/`sb` bezeichnen SAI-Blockdaten; die Richtung folgt erst aus der gewählten Konfiguration. Die konkrete Verbindung TX → RX ist separat festzulegen.

Auf beiden Modulen ist eine Tabelle **Daisy-Pin → Steckkontakt → MCU-Pin → Alternate Function (AF) → SAI-Instanz/Block → Dev-Kit-Netz** anhand der jeweiligen Datenblätter und Schaltpläne anzulegen. Mechanische Pinkompatibilität beweist weder gleiche AF-Belegung noch gleiche Codec-, Clock- oder Versorgungsbeschaltung. Die genaue Seed-/Trägerplatinenrevision bleibt deshalb relevant.

Mögliche Alternativen, alle **UNGEPRÜFT**:

- Andere herausgeführte MCU-Pins mit passender SAI-AF verwenden, sofern Blockkombination, libDaisy-Unterstützung und bestehende Belegung passen.
- MUX-/Schalterfunktionen auf freie GPIOs oder eine geeignete Erweiterung umlegen; Auswirkungen auf Bedienung, Scan-Timing und Steuerbus prüfen.
- Betroffene Funktionen für einen späteren Versuch entfallen lassen; ihre angeschlossene Hardware muss trotzdem elektrisch verträglich sein.
- Mit Adapter/Zwischenplatine oder gezieltem Umlöten Netze trennen und neu führen. Reine Firmware-Umbelegung entfernt keine Leiterbahn, Pull-Widerstände oder angeschlossenen Treiber. Eingriff erst nach dokumentierter Netzprüfung und gesondertem Hardwareauftrag; hier wurde nichts verändert.
- Falls SAI2 nicht praktikabel ist: einen anderen digitalen Transport separat auf Bandbreite, Latenz und Synchronisierung untersuchen oder den Koprozessor verwerfen. SPI o. Ä. ist kein automatisch gleichwertiger Audioersatz.

## 3. Erforderliche Machbarkeitsprüfungen

Die folgende Liste ist ein Plan für spätere Forschung, kein Bericht über durchgeführte Tests. **Alle Ergebnisse sind offen.**

| Bereich | Prüfung / erforderlicher Nachweis |
|---|---|
| Hardware und KiCad | Tatsächliche Revisionen beider Seeds und des Desktop Dev Kits erfassen. Passende KiCad-Schaltpläne einschließlich hierarchischer Blätter und PCB-Netze prüfen: Pin-AF, MUX, Schalter, Pulls, Treiber, Steckzugang, Codec-Verbindungen. Exakte Quelldateien/Revisionen dokumentieren. |
| SAI-Clocks | Eindeutigen Master für BCLK/FS und ggf. MCLK festlegen; I²S-Format, Samplerate, Wort-/Slotbreite und SAI-A/B-Synchronisierung prüfen. Clock-Beziehung zwischen Seed3-Codec-SAI und intermodularem SAI2 nachweisen. Zwei unabhängig auf denselben Nennwert gesetzte Sampleraten garantieren keine Synchronität. |
| DMA und Firmware | Gleichzeitigen Betrieb von lokalem Codec und zusätzlichem SAI prüfen: DMA-Streams/Requests, Interruptprioritäten, zugängliche Speicherbereiche, Cache-Kohärenz, Double-Buffering, Blockgrößen und CPU-Budget. Codec-unabhängigen Audio-Callback auf Seed 1.2 sowie unterstützten libDaisy-Stand klären. Kein Firmware-Build oder Flash in diesem Dokumentationsschritt. |
| Signalpegel | GPIO-Spannungen und Toleranzen beider Revisionen, gemeinsame Masse, Pinrichtung, Ausgangskonflikte und Verhalten beim ausgeschalteten Partner prüfen. Leitungslänge, Rückleitung und Signalqualität für die Clock-Frequenzen bewerten; ggf. Schutz/Terminierung dimensionieren. Keine direkte 5-V-Logikverbindung annehmen. |
| Audio-Synchronisierung | Gemeinsamen Audio-Zeitbezug oder ausdrücklich begründete Clock-Domain-Überbrückung vorsehen. Start/Reset, Drift, Buffer-Unter-/Überläufe, Kanalzuordnung und gemessene Roundtrip-Latenz prüfen. Langzeittest ohne Sample-Slips; nötige asynchrone Resampling-/Pufferlösung mit Aufwand neu bewerten. |
| Bidirektionale Steuerung | Separaten Transport (z. B. UART, SPI oder I²C) erst nach Pin-/Busprüfung wählen. Parameter/Noten zum Koprozessor, Status/Fehler zurück; Ereigniszeitpunkt zum Audio, Queue-Grenzen, Überlast, Reset und Wiederverbindung klären. Steuerungs-Duplex ersetzt keinen Audio-Duplex. |
| Audio-Mixing | Seed3 als vorgesehener Mischpunkt: lokale Stimmen + empfangene Stimmen bzw. Dry/Wet-Return. Gain/Headroom, Sättigung/Limiter, Kanalzahl, Latenzausgleich und unbeabsichtigte Feedback-Schleifen festlegen. Messung unter DSP- und Steuerlast; kein analoger Umweg über den Seed-1.2-Codec im Zielbild. |
| Versorgung / USB-Backfeeding | Strombudget für beide Seeds und Dev-Kit-Peripherie mit Reserve messen. Zulässige Versorgungspins, Regler und USB-VBUS-/Power-Path-Schaltung jeder Revision prüfen. Keine ungeprüfte Parallelschaltung von USB- und externer Versorgung; Rückspeisung in PC, Netzteil oder ausgeschaltetes Modul auch über GPIO prüfen. Ein-/Ausschaltreihenfolge, Masse und Recovery-Zugänge dokumentieren (Q-MECH-8, D012). |

## 4. Späterer Entscheidungspunkt

Zuerst Quellen-/Netzprüfung ohne Hardwareeingriff; dabei ein überprüfbares Pin- und Clock-Konzept, Konfliktliste, Versorgungsplan sowie Kosten in verlorenen Bedienelementen erstellen. Unauflösbare Pin-/Clock-Konflikte sind ein Grund, die Option zu verwerfen.

Erst nach separatem Auftrag und Backup/Recovery wären Firmware- und Hardwareversuche zulässig: zunächst digitaler Einwegtransfer mit bekanntem Testsignal, anschließend ggf. Duplex, Steuerung und Mixing. Revisionen, Firmware-/Bibliotheks-Hashes, Messaufbau, Latenz, Fehlerzähler, Last und Versorgung in einer neuen Forschungsnotiz festhalten. Erst diese Nachweise erlauben für die konkret getestete Kombination einen Statuswechsel von **UNGEPRÜFT** zu **BELEGT**.

## 5. Quellen und Grenzen dieser Notiz

Am 11.10.2026 wurden diese Primärquellen als Ausgangspunkte gelesen bzw. lokalisiert:

- [Seed3 Desktop Dev Kit – Herstellerdokumentation](https://docs.daisy.audio/product/Seed3-Desktop-Dev-Kit/): beschreibt das Kit und verlinkt Pinout, Schaltplan und KiCad-Dateien.
- [Hersteller-KiCad-Repository, Tag Rev4](https://github.com/daisyaudio/Seed3-DevKit-Desktop/tree/Rev4): Quelldateien vorhanden; keine vollständige Netz-/PCB-Prüfung in diesem Schritt. Der Tag belegt nicht die Revision des bestellten Geräts.
- [libDaisy ExternalCodec.cpp](https://docs.daisy.audio/libDaisy-Examples/ExternalCodec_8cpp_source/): Referenz für SAI2-Konfiguration, keine Seed-zu-Seed-Validierung. Die Online-Dokumentation liefert hier keinen festgehaltenen Quellcommit; vor Experimenten einen reproduzierbaren Bibliotheksstand wählen.

Die MUX-/Schalter-Zuordnung ist eine Arbeitsannahme aus der vorherigen Diskussion und muss noch am revisionsrichtigen Schaltplan bestätigt werden. MCU-Datenblätter/AF-Tabellen und die passenden Seed-Schaltpläne sind noch auszuwerten. **Keine Hardwaremessung, kein Flash und kein Umbau wurden durchgeführt.**
