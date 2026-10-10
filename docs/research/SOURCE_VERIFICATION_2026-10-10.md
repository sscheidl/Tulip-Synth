# Quellenprüfung 10.10.2026

**Zweck:** Der Claude-Bericht vom 09.10.2026 war nicht verfügbar. Die im Masterprompt zusammengefassten Kernaussagen wurden deshalb direkt an den Original-Repositories mit **denselben Referenzständen** geprüft. Es wurde nur gelesen, kein Code gebaut, keine Hardware angesprochen.

## Geprüfte Stände

| Repository | angefragt | aufgelöst | Commit-Datum |
|---|---|---|---|
| shorepine/tulipcc | `36e6332` | `36e6332c05bfc410fb487eba75706cc4c5fb0112` | 2026-10-06 |
| shorepine/amy | `69a1469` | `69a146930cbf2c52abb5ad92c26d2157f9095a6d` | 2026-10-08 |
| Synthux-Academy/Audrey-II | `e5ab799` | `e5ab79910eb7ccbac5bbc865fae5459d65f5b5e3` | 2026-08-03 |
| electro-smith/DaisyExamples | `259ed82` | `259ed82c7d4c0d7699f695945e6e111b7dc7cb27` | 2026-06-12 |
| electro-smith/DaisySP | (HEAD) | `2c72eaf` | 2026-09-28 |
| sscheidl/Custom-Firmware (nur lesend) | (HEAD) | `255f3eac90ffafe58f2245122897290e4ed854e1` | – |

## Belege (Datei → Aussage)

### tulipcc `36e6332`
- `docs/amyboard/README.md`: I²C-Beispiel `I2C(0, freq=400000)`, `i2c.writeto(0x3f, x)`; Stromaufnahme ~350 mA bei Tulip-Versorgung, Tulip ~575 mA; Boot-Loop-Warnung; USB-C „gadget mode, NOT HOST“; I²C front = Zubehör, I²C back = Tulip-Host; Versorgung USB-C/Eurorack/I²C, höchste Spannung gewinnt; DIP-Schalter OFF = Line; Boot mit Juno-6 Patch #0, MIDI-Kanal 1.
- `docs/amyboard/faq.md`: „Chaining multiple AMYboards“ (S/PDIF + I²C/MIDI, kein Voice-Splitting, ~4 Boards über I²C-Strom, 2,94 V am 4. Board); USB-Host nur auf Tulip; CPU-Budget (Juno ~12 %, DX7 ~8 %, PCM ~2 %); ~250 Oszillatoren; ~3 MB SPIRAM für Samples; I²C-Displaylast kann Audio aushungern; On-Board-C-Compiler „new, very alpha“.
- `docs/amyboard/firmware.md`: Bootloader-Modus und Web-Upgrader (Upgrade vs. Fully erase).
- `docs/user_c_dsp.md`: `xcc700` auf ESP32-S3; S8.23; 8 Slots; „no floats, structs, `for`, or preprocessor“.
- `README.md`: Tulip CC: 8,5 MB RAM, 32 MB Flash, 1024×600, Multi-Touch, USB-Keyboard/MIDI inkl. Hubs, I²C/Grove, AMY lokal mit Karplus-Strong, 575 mA.
- `docs/tulip_api.md`: LVGL 9, `UIScreen`, `UISlider`, `UIButton` usw.

### amy `69a1469`
- `src/amy.h`: `AMY_SAMPLE_RATE` 48000 bei `AMY_DAISY`, sonst 44100; `BLOCK_SIZE_BITS` 7 (Daisy) bzw. 8.
- `src/oscillators.c`: `render_ks` (nutzt `feedback`), `ks_note_on` (Ringpuffer je Oszillator beim ersten KS-Note-On).
- `src/api.c`: Standardkonfiguration (`ks_oscs = 1` aktiviert KS, `max_oscs = 250`, `max_voices = 64`).
- `docs/api.md`, Abschnitt Hooks: `amy_external_render_hook`, `amy_external_bus_postprocess_hook` (S8.23 in `int32_t`).
- `daisy/Makefile`, `daisy/amy_daisy.cpp`: AMY auf Daisy, `APP_TYPE = BOOT_SRAM`, `SetAudioBlockSize(128)`, `MidiUartHandler`.
- `LICENSE`: MIT.

### Audrey-II `e5ab799`
- `FeedbackSynth_main.cpp`: `SAI_48KHZ`, `kBlockSize = 4`, `IN_L` → Engine → `OUT_L/OUT_R`, Limiter.
- `Source/FeedbackSynthControls.{h,cpp}`: `kNumAdcChannels = 11`, Pins A0–A10 bzw. Simple-Pins 30–40, Toggle-Schalter D14.
- `Makefile`: kein `APP_TYPE` (Standard).
- Suche nach `midi`/`usb` in eigenem Code (ohne `lib/`): keine Treffer.
- `README.md`: zwei unterschiedliche Firmware-Links (`audrey-ii-v3.bin`, `audrey-ii.bin`); Flashen per Web Programmer oder `make program-dfu`.
- `.gitmodules` / Submodule: libDaisy `694fc55`, DaisySP `7f67768`. `LICENSE`: MIT.

### DaisyExamples `259ed82`
- `patch/Torus/` (Rings-Port, Ben Sergentanis; `OPT = -Os`), `patch/Nimbus/` (Clouds-Port) vorhanden.

### DaisySP `2c72eaf`
- `Source/PhysicalModeling/`: `stringvoice`, `modalvoice`, `resonator`, `KarplusString`. Submodul `DaisySP-LGPL`. `LICENSE`: MIT.

### Custom-Firmware `255f3ea` (nur gelesen, nicht verändert)
- `inventory/firmware-index.csv`: Audrey-Archiv mit `audrey-ii-v3.bin` (92 192 B, CRC32 `73655DBD`), Daisy-Seed-Datenblätter (u. a. Rev7), Tools.
- `README.md`/`docs/repository-policy.md`: Policy „keine Firmware-Binaries im Git“ → übernommen als D016.

## Nicht geprüft

- `pichenettes/eurorack` (keine Aussage im Projekt hängt derzeit davon ab).
- Datenblätter Daisy Seed / STM32H750 (liegen lokal beim Eigentümer).
- Jegliches Verhalten auf echter Hardware.
