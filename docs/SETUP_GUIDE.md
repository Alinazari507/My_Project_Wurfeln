# 🎯 P2.3.5 - Setup & Verwendung

## ⚡ Quick Start

```bash
# 1. Virtual Environment aktivieren
source venv/bin/activate

# 2. Demo ausführen
python application/demos/siegerehrung_quick.py

# 3. Tests runnen
python application/Test_Siegerehrung_P2_3_5.py

# 4. Code-Qualität überprüfen
bash check_code_quality.sh
```

## 📦 Installation (erste Mal)

```bash
# Virtual Env erstellen
python3 -m venv venv

# Aktivieren
source venv/bin/activate

# Dependencies
pip install PyYAML flake8 pylint
```

## 🏗️ Projekt-Struktur

```
My_Project/
├── domain/                  ← Geschäftslogik (3er Gleichstand-Handling)
├── application/
│   ├── demos/              ← Hier: siegerehrung_quick.py
│   └── Test_Siegerehrung_P2_3_5.py
├── infrastructure/         ← Storage & Persistierung
├── docs/                   ← Dokumentation
├── .flake8                 ← Code-Standards
└── check_code_quality.*    ← QA-Tools
```

## 🎮 Code-Beispiel

```python
from application.SiegerehrungApp_P2_3_5 import SiegerehrungApp
from infrastructure.ExtendedGameStorage_P2_3_4 import ExtendedGameStorage

# Setup
storage = ExtendedGameStorage(storage_path="archive")
app = SiegerehrungApp(storage=storage, max_rounds=3)

# Spiel
app.start_new_game(["Alice", "Bob"])
for _ in range(6):  # 3 Runden × 2 Spieler
    app.execute_player_turn()

# Finale Siegerehrung ★★★
app.display_final_ranking()
```

## ✨ Funktionen 

- ✅ Rundenlimit-Überprüfung
- ✅ Intelligente Gleichstand-Verwaltung (1,1,1,4,4,6)
- ✅ Podium-Anzeige (🥇🥈🥉)
- ✅ Auto-Save nach jeder Runde
- ✅ Mehrere Gewinner möglich

## 🧪 Tests ausführen

```bash
# Akzeptanztests
python application/Test_Siegerehrung_P2_3_5.py

# Quick Demo (alle 3 Szenarien)
python application/demos/siegerehrung_quick.py
```

## 📊 Ordnerstruktur Standards

| Folder | Inhalt | Regel |
|--------|--------|-------|
| `domain/` | Geschäftslogik | Funktioniert unabhängig |
| `application/` | App-Logik | Koordiniert Domain + Infrastructure |
| `application/demos/` | Demo-Skripte | Nur für Demonstrationen |
| `infrastructure/` | Storage | Datenpersistierung |
| `docs/` | Dokumentation | Markdown-Dateien |
| `archive/` | Auto-Saves | Programme erstellen dies |
| Root | Nur Config/Tools | `.flake8`, `check_code_quality.*` |

## 🚨 Troubleshooting

**Problem:** `ModuleNotFoundError`
```bash
# Lösung: PATH-Setup in Code prüfen
export PYTHONPATH=/home/d3002/My_Project:$PYTHONPATH
```

**Problem:** Flake8/Pylint nicht installiert
```bash
pip install flake8 pylint
```

**Problem:** Archive-Ordner fehlt
```bash
# Auto-erstellt, aber manuell möglich:
mkdir -p archive
```

## 📚 Weitere Ressourcen

- Siehe: [docs/CODE_QUALITY.md](docs/CODE_QUALITY.md)
- Siehe: [docs/LERNPFAD.md](docs/LERNPFAD.md)
- Siehe: [LERNPFAD_P2_3_COMPLETE.md](../LERNPFAD_P2_3_COMPLETE.md)
