# Übergabedokumente (Archiv)

Regel: **Originale werden unverändert abgelegt und nie bearbeitet.** Korrekturen stehen in `../CLAUDE_REVIEW_2026-10-09.md` und den Projektdokumenten.

## Bestand

| Datei | Herkunft | Status | SHA-256 |
|---|---|---|---|
| `Codex_Master_Prompt_Rev3_2026-10-10.md` | Auftrag M0 (Chat), inhaltlich unverändert übernommen | vorhanden | `a6d6c27c0dafeb3e13eac3a0a20ad3f0e693a167a159ef4976fe69349b02fedb` |
| `AMYboard_Uebergabe_REKONSTRUKTION_2026-10-10.md` | **Rekonstruktion** aus Primärquellen, kein Original | vorhanden | – |
| `Tulip_AMYboard_Projektuebergabe_2026-10-09.md` | Original | **FEHLT** (Q-DOC-1) | – |
| Daisy-/Audrey-II-Projektübergabe 09.10.2026 | Original | **FEHLT** (Q-DOC-1) | – |
| `claude/Tulip_Synth_Machbarkeit_Roadmap_2026-10-09.md` | Original Claude-Bericht | **FEHLT** (Q-DOC-1); Zielort: `claude/` in diesem Ordner | – |

## Fehlende Originale nachtragen (Eigentümer)

```powershell
# in der lokalen Arbeitskopie
Copy-Item "<Pfad>\Tulip_AMYboard_Projektuebergabe_2026-10-09.md" docs\handovers\
Copy-Item "<Pfad>\<Daisy-Uebergabe>.md" docs\handovers\
New-Item -ItemType Directory docs\handovers\claude -Force
Copy-Item "<Pfad>\claude\Tulip_Synth_Machbarkeit_Roadmap_2026-10-09.md" docs\handovers\claude\
Get-FileHash docs\handovers\*.md, docs\handovers\claude\*.md -Algorithm SHA256
```

Danach: SHA-256 in die Tabelle eintragen. Bei Duplikaten Hashes vergleichen (Befund 1: Enthält die AMYboard-Übergabe die Daisy-Übergabe?). Dann `CLAUDE_REVIEW_2026-10-09.md` mit dem Originalbericht abgleichen.
