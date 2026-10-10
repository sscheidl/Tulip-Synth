# Parametermodell und Presets

Ziel: GUI und Presets sind **hardwareunabhängig**. Die Abbildung auf AMY-Wire/MIDI liegt an genau einer Stelle (Transport). Dieses Dokument legt das *Konzept* fest. Die Implementierung entsteht in M1 so einfach wie möglich (ein Python-Dict pro Instrument).

## 1. Parameterdefinition

| Feld | Bedeutung | Beispiel |
|---|---|---|
| `id` | stabile, eindeutige Kennung (snake_case, nie umbenennen) | `damping` |
| `name` | Anzeigename | „Damping“ |
| `type` | `float` \| `int` \| `enum` \| `bool` | `float` |
| `min`, `max` | Wertebereich in Benutzer-Einheit | `0.0`, `1.0` |
| `default` | Standardwert | `0.5` |
| `unit` | Anzeigeeinheit | `""`, `Hz`, `ms`, `%` |
| `scale` | `lin` \| `log` \| `exp` (GUI-Regler → Wert) | `lin` |
| `smoothing_ms` | Glättung auf dem DSP-Modul (0 = keine) | `10` |
| `platforms` | unterstützte Profile | `["amyboard", "daisy"]` |
| `map` | Transportzuordnung **je Plattform** | siehe unten |

Regeln:
- Die GUI arbeitet nur mit `id` und Benutzerwerten, nie mit CC-Nummern oder AMY-Codes.
- `map` ist das **einzige** plattformspezifische Feld.
- Daisy-only-Parameter sind ausdrücklich erlaubt (`platforms: ["daisy"]`).
- Ein Parameter, der im aktiven Profil fehlt, wird **nicht angezeigt und nicht gesendet**. Das ist kein Fehler.

## 2. Beispiel (Skizze für M1, nicht final)

```python
# instruments/resonator/params.py (entsteht in M1)
PARAMS = [
    {"id": "damping", "name": "Damping", "type": "float",
     "min": 0.0, "max": 1.0, "default": 0.5, "unit": "", "scale": "lin",
     "smoothing_ms": 0, "platforms": ["amyboard", "daisy"],
     "map": {"amyboard": {"amy": "feedback", "invert": True},   # AMY-KS-Abklingen
             "daisy":    {"nrpn": None}}},                       # Zuordnung in M2
    {"id": "exciter_model", "name": "Exciter", "type": "enum",
     "values": ["pluck", "bow", "blow"], "default": "pluck",
     "platforms": ["daisy"], "map": {"daisy": {"nrpn": None}}},
]
```

Die konkrete AMY-Abbildung (welche AMY-Parameter KS-Klang beeinflussen, z. B. `feedback`, Filter, Hüllkurve) wird in M1 am Gerät ermittelt (BELEGT ist nur: `render_ks` verwendet `feedback`, `amy/src/oscillators.c`).

## 3. Transport

| Transport | Einsatz | Status |
|---|---|---|
| AMY-Wire über I²C (`0x3f`) | Tulip → AMYboard, M1 Standard | BELEGT (Doku), UNGEPRÜFT am Gerät |
| AMY-SysEx über MIDI | Tulip → AMYboard, Alternative | BELEGT (Doku) |
| MIDI CC (7 Bit) | einfache Parameter, Daisy M2 | – |
| MIDI NRPN (14 Bit) | feinere Auflösung, Daisy M2+ | – |
| SysEx | Preset-Übertragung, falls nötig | – |

Kein eigenes Protokoll, solange diese ausreichen (D008, D014; [Masterprompt](handovers/Codex_Master_Prompt_Rev3_2026-10-10.md) Abschnitt 5.3).

## 4. Presets

Format: **JSON-Datei pro Preset** auf dem Tulip-Dateisystem.

```json
{
  "format": 1,
  "instrument": "resonator",
  "name": "Warm Pluck",
  "params": { "damping": 0.42, "exciter_model": "bow" }
}
```

Regeln:
1. Ein Preset beschreibt ein **Instrument**, nicht einen Prozessor und nicht eine Modulanzahl.
2. Beim Laden werden nur Parameter gesendet, die das aktive Profil unterstützt.
3. **Nicht unterstützte Parameter bleiben beim Speichern erhalten** (Load → Edit → Save darf `exciter_model` auf einem AMYboard nicht löschen).
4. Unbekannte Parameter-IDs werden ignoriert und ebenfalls erhalten.
5. Fehlende Parameter erhalten ihren `default`.
6. `format` wird nur erhöht, wenn eine Migration nötig ist.

Für M1 reicht **ein** Preset. Plattformübergreifendes Laden wird erst ab M2/M4 tatsächlich geprüft.

## 5. Bewusst nicht Teil des Modells (noch)

Modulationsmatrix, Parameter-Automation, Multi-Modul-Zuordnung, Morphing, Versionierung einzelner Parameter. Wird ergänzt, wenn ein Instrument es konkret braucht.
