# Referenzen

Versionsstände wurden am 10.10.2026 geprüft (siehe `research/SOURCE_VERIFICATION_2026-10-10.md`). Bei neuen Recherchen Commit-Hash angeben.

## Tulip / AMY

| Quelle | Stand | Lizenz | Relevanz |
|---|---|---|---|
| [shorepine/tulipcc](https://github.com/shorepine/tulipcc) | `36e6332` (2026-10-06); AMY-Submodul dort `3e1c573` | MIT | Tulip-Firmware, GUI-API, AMYboard-Doku |
| ├ [docs/amyboard/README.md](https://github.com/shorepine/tulipcc/blob/main/docs/amyboard/README.md) | 〃 | | Anschlüsse, Strom, I²C `0x3f` |
| ├ [docs/amyboard/faq.md](https://github.com/shorepine/tulipcc/blob/main/docs/amyboard/faq.md) | 〃 | | CPU-Budget, Verkettung, Speicher |
| ├ [docs/amyboard/firmware.md](https://github.com/shorepine/tulipcc/blob/main/docs/amyboard/firmware.md) | 〃 | | Firmware-Update/Recovery |
| ├ [docs/user_c_dsp.md](https://github.com/shorepine/tulipcc/blob/main/docs/user_c_dsp.md) | 〃 | | On-Device-C (`xcc700`) |
| ├ [docs/tulip_api.md](https://github.com/shorepine/tulipcc/blob/main/docs/tulip_api.md) | 〃 | | LVGL/UI, MIDI, I²C |
| ├ [docs/amyboard/modular.md](https://github.com/shorepine/tulipcc/blob/main/docs/amyboard/modular.md) + `docs/pcbs/amyboard/amyboard_front_panel.{3mf,dxf,svg,eps}` | 〃 | | Frontplatte 10 HP, Vorlage für Gehäuse (D015) |
| └ `docs/pcbs/tulip4_r11/case.lbrn2` | 〃 | | Tulip-Gehäusevorlage (Laserschnitt), Inhalt ungeprüft |
| [shorepine/amy](https://github.com/shorepine/amy) | `69a1469` (2026-10-08) | MIT | Synth-Engine, KS, Hooks |
| ├ [docs/api.md](https://github.com/shorepine/amy/blob/main/docs/api.md) | 〃 | | Wire-Protokoll, Hooks |
| └ [daisy/](https://github.com/shorepine/amy/tree/main/daisy) | 〃 | | **AMY-Portierung auf Daisy** (Cross-Platform-Referenz) |

## Daisy

| Quelle | Stand | Lizenz | Relevanz |
|---|---|---|---|
| [Synthux-Academy/Audrey-II](https://github.com/Synthux-Academy/Audrey-II) | `e5ab799` (2026-08-03); libDaisy `694fc55`, DaisySP `7f67768` | MIT | Stock-Firmware der Audrey II |
| [electro-smith/DaisyExamples](https://github.com/electro-smith/DaisyExamples) (Masterprompt nennt `daisyaudio/DaisyExamples`) | `259ed82` (2026-06-12); libDaisy `85172e2`, DaisySP `a0494a3` | MIT (Beispiele); MI-Ports siehe Dateiköpfe | `patch/Torus` (Rings), `patch/Nimbus` (Clouds) |
| [electro-smith/DaisySP](https://github.com/electro-smith/DaisySP) | HEAD `2c72eaf` (2026-09-28) | MIT; Submodul `DaisySP-LGPL` = LGPL | `Source/PhysicalModeling/`: `stringvoice`, `modalvoice`, `resonator`, `KarplusString` |
| [electro-smith/libDaisy](https://github.com/electro-smith/libDaisy) | – | MIT | Hardwareschicht, USB-MIDI |
| [daisy.audio](https://daisy.audio/) | – | – | Doku, Web Programmer |

## Stromversorgung (Gehäuse G2, Kandidaten)

| Quelle | Stand | Relevanz |
|---|---|---|
| [4ms Row Power 45 (Perfect Circuit)](https://www.perfectcircuit.com/4ms-row-power-45.html), [Row Power 40](https://www.perfectcircuit.com/4ms-row-power-40.html) | Händlerangabe 10.10.2026 | Eurorack-Netzteil mit +5 V |
| [ModularGrid: Arturia RackBrute 6UPower](https://modulargrid.net/e/arturia-rackbrute-6upower) | Community-Datenbank, 10.10.2026 | Netzteilmodul 5 HP, 80 mm, 15 V/3 A; Vorzugslösung G2 |
| [Cre8audio NiftyCase (Scan)](https://www.scan.co.uk/products/cre8audio-niftycase-powered-modular-case-with-midi-to-cv), [zZounds](https://zzounds.com/item--CTANIFTYCASE) | Händlerangabe 10.10.2026 | Kompaktes Eurorack-Gehäuse, Option G2 |
| [Befaco Trolley Bus (Perfect Circuit)](https://www.perfectcircuit.com/befaco-trolley-bus.html), [Befaco Powskiff](https://www.perfectcircuit.com/befaco-powskiff.html) | Händlerangabe 10.10.2026 | Busplatine + Netzteil mit +5 V |

## Mutable Instruments

| Quelle | Stand | Lizenz | Relevanz |
|---|---|---|---|
| [pichenettes/eurorack](https://github.com/pichenettes/eurorack) | nicht geprüft | Code MIT (Hardware CC-BY-SA) | Rings, Elements, Clouds, Plaits als Originalquelle |

## Lokal beim Eigentümer (nicht im Git)

Aus dem Inventar `sscheidl/Custom-Firmware@255f3ea` (`inventory/firmware-index.csv`), nur Metadaten:
- `audrey II/Firmware/audrey-ii-v3.bin` (92 192 B, CRC32 `73655DBD`)
- `audrey II/Daisy Seed/ES_Daisy_Seed_Rev7.pdf`, `Daisy_Seed_datasheet_v1-1-5.pdf`, `Daisy_Seed_pinout.pdf`
- `audrey II/Tools/DaisyExamples-master.zip`, `oopsy.zip`, `zadig-2.9.exe`

## SD-Karten-Recherche (11.10.2026)

Tulip-Menüanpassung (17.10.2026): eigene LVGL-/Python-Anpassung in `devices/tulip/large_menu.py`, vorhandene Launcher-API aus [ui.py, Tulip-Stand 17d1ef1](https://github.com/shorepine/tulipcc/blob/17d1ef1d14aa0a51520fced04c87c1328f79bbd0/tulip/shared/py/ui.py), MIT. Kein Fremdcode kopiert.

Quellen, Abrufstand und Abgrenzung von Herstellerangaben, Rechnungen und ungeprüfter Hardware: [research/SD_CARDS_2026-10-11.md](research/SD_CARDS_2026-10-11.md). Ergänzende Primärquellen: [Daisy Seed Datenblatt](https://daisy.nyc3.cdn.digitaloceanspaces.com/products/seed/Daisy_Seed_datasheet.pdf), [libDaisy SDMMC](https://github.com/electro-smith/libDaisy/blob/master/src/per/sdmmc.h), [FatFs-Konfiguration](https://github.com/electro-smith/libDaisy/blob/master/src/sys/ffconf.h), [SD Association Speed Class](https://www.sdcard.org/developers/sd-standard-overview/speed-class/) und [A1/A2](https://www.sdcard.org/developers/sd-standard-overview/application-performance-class/). Kein Fremdcode übernommen.

## Nicht verfügbare Originaldokumente

Voices-Touch-Diagnose (17.10.2026): [Voices](https://github.com/shorepine/tulipcc/blob/main/tulip/shared/py/voices.py) und [GT911-Treiber](https://github.com/shorepine/tulipcc/blob/main/tulip/esp32s3/gt911_touchscreen.c), MIT, main abgerufen 17.10.2026. Eigene Anpassung devices/tulip/voices_touch.py verwendet Geometrie und APIs, kein Upstream-Code kopiert. Eingefrorener Gerätecode nicht bytegleich verglichen.

- `claude/Tulip_Synth_Machbarkeit_Roadmap_2026-10-09.md`
- `Tulip_AMYboard_Projektuebergabe_2026-10-09.md`
- Daisy-/Audrey-II-Projektübergabe vom 09.10.2026

Siehe `handovers/README.md`.
