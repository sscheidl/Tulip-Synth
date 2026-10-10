# Entwicklungsumgebung – Inventur

## 1. Wichtiger Hinweis zum Ort der Inventur

Der Bootstrap (M0) lief am 10.10.2026 in einer **Cloud-Sitzung (Linux-Container)**, nicht auf dem Windows-Host des Eigentümers. Die Werkzeuge des Windows-Hosts konnten deshalb **nicht** erfasst werden. Abschnitt 2 beschreibt den Container (nur für Doku-/Analysearbeit relevant), Abschnitt 3 enthält das Prüfskript für den Windows-Host.

Es wurde nichts installiert.

## 2. Cloud-Container (10.10.2026)

| Werkzeug | Version | Bemerkung |
|---|---|---|
| OS | Ubuntu 24.04.5 LTS (x86_64) | flüchtig |
| g++ / gcc | 13.3.0 | C++17 verfügbar, für Host-Tests ab M3 |
| clang / clang++ | 18.1.3 | |
| CMake | 3.28.3 | |
| Ninja | 1.11.1 | |
| GNU Make | 4.3 | |
| Python | 3.13 | |
| Git | 2.43.0 | |
| gh | 2.89.0 | |
| arm-none-eabi-gcc | **fehlt** | Daisy-Builds hier nicht möglich |
| ESP-IDF / xtensa-esp32s3-elf-gcc | **fehlt** | AMYboard-Builds hier nicht möglich |
| dfu-util, openocd, esptool, mpremote | **fehlen** | kein Hardwarezugriff aus der Cloud ohnehin |

Folgerung: Die Cloud eignet sich für Dokumentation, Code-Analyse, Host-Unit-Tests von `dsp/common` und Tulip-Python-Code-Reviews, **nicht** für Firmware-Builds oder Flashen.

## 3. Windows-Host (ausstehend)

Benötigt je Meilenstein:

| Werkzeug | Zweck | ab |
|---|---|---|
| Git, GitHub-Zugang | Arbeitskopie | M0 |
| Python 3 + `mpremote` | Dateien auf Tulip/AMYboard kopieren, REPL | M1 |
| Chrome/Edge (WebSerial) | AMYboard-Online-Editor, Daisy Web Programmer | M1/M2 |
| `arm-none-eabi-gcc`, GNU Make | Daisy-Firmware (Daisy Toolchain) | M2 |
| `dfu-util` (+ ggf. Zadig-Treiber) | Daisy flashen/auslesen | M2 |
| ST-Link / OpenOCD (optional) | Daisy-Debugging | M2+ |
| ESP-IDF (Version passend zu tulipcc) | eigene AMYboard-Firmware | M3 |
| CMake, C++17-Compiler (MSVC/MinGW/clang) | Host-Tests | M3 |

Hinweis aus dem Eigentümer-Archiv: `zadig-2.9.exe`, `DaisyExamples-master.zip` und `oopsy.zip` liegen lokal vor (Inventar in `sscheidl/Custom-Firmware`). Installiert sind sie damit nicht unbedingt.

### Prüfskript (PowerShell, nur lesend)

```powershell
$tools = 'git','gh','python','py','mpremote','cmake','ninja','make','mingw32-make',
         'g++','clang++','cl','arm-none-eabi-gcc','dfu-util','openocd','idf.py','esptool'
foreach ($t in $tools) {
  $c = Get-Command $t -ErrorAction SilentlyContinue
  if ($c) { "{0,-20} {1}" -f $t, $c.Source } else { "{0,-20} NICHT GEFUNDEN" -f $t }
}
arm-none-eabi-gcc --version 2>$null | Select-Object -First 1
cmake --version 2>$null | Select-Object -First 1
if ($env:IDF_PATH) { "IDF_PATH = $env:IDF_PATH" } else { "IDF_PATH nicht gesetzt" }
Get-ChildItem "$env:USERPROFILE\esp", "C:\Espressif" -Directory -ErrorAction SilentlyContinue | Select-Object FullName
```

Ergebnis bitte hier als Tabelle eintragen (Datum, Werkzeug, Version, Pfad).

## 4. Lokale Arbeitskopie

```powershell
cd "D:\Eigene Dateien\Eigene Dokumente\Playground"
# Vorher prüfen, ob "Tulip-Synth" bereits existiert und Inhalte hat (nicht überschreiben!)
git clone https://github.com/sscheidl/Tulip-Synth.git
```
