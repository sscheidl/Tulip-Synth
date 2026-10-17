# Entwicklungsumgebung – Inventur

## 1. Wichtiger Hinweis zum Ort der Inventur

Der Bootstrap (M0) lief am 10.10.2026 in einer **Cloud-Sitzung (Linux-Container)**, nicht auf dem Windows-Host des Eigentümers. Die Werkzeuge des Windows-Hosts konnten damals **nicht** erfasst werden. Abschnitt 2 beschreibt den Container (nur für Doku-/Analysearbeit relevant), Abschnitt 3 dokumentiert die lokale Windows-Inventur vom 11.10.2026 und das Prüfskript.

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

## 3. Windows-Host (geprüft am 11.10.2026)

**BELEGT am Windows-Host:** Nur lesende Inventur (PATH, Versionsaufrufe,
Windows-Uninstall-Registry, Visual-Studio-`vswhere`, Dateipfade und `pip show`).
Es wurde nichts installiert und keine Firmware geflasht. Builds und Zugriff auf
Tulip/AMYboard/Daisy sind **UNGEPRÜFT**; Firmwarestände wurden nicht erfasst.

| Werkzeug | Befund | Bedarf |
|---|---|---|
| Git | 2.53.0.windows.1, `C:\Program Files\Git\cmd\git.exe` | vorhanden, M1 |
| GitHub CLI | 2.93.0 laut Registry, nicht im aktuellen PATH | optional |
| Python | 3.12.10, `C:\Users\ssche\AppData\Local\Programs\Python\Python312\python.exe`; `py` ebenfalls erreichbar | vorhanden, M1 |
| CMake | 4.4.2, `C:\Program Files\CMake\bin\cmake.exe` | vorhanden; für M1 nicht erforderlich |
| C/C++ (MSVC) | Build Tools 2022 und 2026; `cl.exe` 14.44.35207 bzw. 14.51.36231 vorhanden; `vswhere` bestätigt x86/x64-C++-Komponente | Windows-Compiler vorhanden; Developer Shell erforderlich; Host-Tests ab M3 |
| GNU Make / MinGW Make | nicht im aktuellen PATH | für M1 nicht erforderlich; Daisy ab M2 |
| ARM GCC/G++, dfu-util, OpenOCD | nicht im aktuellen PATH; kein Daisy-Eintrag in geprüfter Installationsregistry und kein Verzeichnis an drei üblichen DaisyToolchain-Pfaden | Daisy ab M2; OpenOCD optional |
| Daisy-Installer | `D:\Backup\Backup_System\Music Production\Audio Dev\Daisy Seed\tools\DaisyToolchain-1.1.0-win64.exe` vorhanden | Datei ist kein Installationsnachweis; jetzt nicht ausführen |
| mpremote / pyserial | `python -m pip show mpremote pyserial`: beide fehlen in Python 3.12 | mögliche Ergänzung für USB-REPL/Dateitransfer in M1; Gerätekompatibilität UNGEPRÜFT |
| Arduino IDE | `C:\Program Files\Arduino IDE` leer; Arduino15 und weitere Benutzerdaten vorhanden; kein passender Uninstall-Eintrag | nur Reste nachgewiesen, lauffähige IDE nicht bestätigt; für Projekt nicht erforderlich |
| Edge | `C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe` vorhanden | Browser vorhanden; WebSerial am Gerät UNGEPRÜFT |
| ESP-IDF / esptool | nicht im aktuellen PATH | eigene AMYboard-Firmware frühestens M3 |

**Empfehlung für M1:** Git und vorhandenes Python nutzen, zunächst den Zugriff
auf Tulip über Browser/REPL prüfen. Falls der gewählte USB-Dateitransfer es
erfordert, `mpremote` (mit `pyserial` als Abhängigkeit) ergänzen. Kein zusätzlicher
C++-Compiler, keine Arduino IDE und keine Daisy-Toolchain für M1 erforderlich.
CMake ersetzt weder GNU Make noch einen Compiler; MSVC erzeugt Windows-Code
und ersetzt den ARM-Cross-Compiler für Daisy nicht.

### Was das Daisy-Paket mitbringt

**BELEGT laut Herstellerquellen:** Das Toolchain-Repository führt ARM GNU
Toolchain (C/C++ plus zugehörige Binärwerkzeuge), GNU Make, `dfu-util`, OpenOCD
und `clang-format`. Git und Python werden in der Windows-Anleitung separat
behandelt. Das veröffentlichte `windows/install.bat` ergänzt den Benutzer-PATH
um den `bin`-Ordner. libDaisy, DaisySP und Projektquellen werden separat benötigt.

Die Repository-README nennt Make 4.3, OpenOCD 0.11.0, dfu-util 0.10,
clang-format 10.0.0 und ARM 10-2020-q4-major. **UNGEPRÜFT:** exakter Inhalt und
Komponentenversionen der lokalen Installerdatei 1.1.0; sie wurde nicht ausgeführt
oder entpackt. Das Paket wird für den vorgesehenen C++/libDaisy-Weg ab M2
benötigt, sofern seine Werkzeuge nicht anderweitig passend bereitgestellt werden.

Quellen (abgerufen 11.10.2026):
- [Windows Toolchain Install](https://docs.daisy.audio/tutorials/toolchain-windows/)
- [Understanding the Toolchain](https://docs.daisy.audio/tutorials/Understanding-the-Toolchain/)
- [DaisyToolchain README](https://github.com/electro-smith/DaisyToolchain)
- [Windows PATH-Skript](https://github.com/electro-smith/DaisyToolchain/blob/main/windows/install.bat)

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

**Inventarergänzung 11.10.2026:** Ein „STM8 und STM32 Programmer ST-LINK V2 01“ ist laut Eigentümer vorhanden, aber ungenutzt. Erkennung, Funktion und Daisy-Kompatibilität sind **UNGEPRÜFT**; der Eigentümer vermutet keinen Nutzen. Optionaler Zweck als Debugwerkzeug und Eignung werden getrennt betrachtet, siehe [HARDWARE §7](HARDWARE.md#7-weitere-vorhandene-boards-und-werkzeuge--zweck-und-eignung-getrennt) und Q-HW-10. Das Vorhandensein belegt keine installierte Software und keinen funktionierenden Debugzugang.

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

Die Ergebnisse der Inventur stehen oben; das Skript bleibt für spätere Prüfungen.

## 4. Lokale Arbeitskopie

```powershell
cd "D:\Eigene Dateien\Eigene Dokumente\Playground"
# Vorher prüfen, ob "Tulip-Synth" bereits existiert und Inhalte hat (nicht überschreiben!)
git clone https://github.com/sscheidl/Tulip-Synth.git
```
