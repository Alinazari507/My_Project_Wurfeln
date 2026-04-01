# 🧹 Clean Code Structure für P2.3.5 - Würfelspiel

## ✅ Saubere Ordner-Struktur

```
My_Project/
│
├── 📁 domain/                          ← Domain Layer (Geschäftslogik)
│   ├── GameRound_P2_3_2.py
│   ├── GameState_P2_3_4.py
│   ├── FinalRanking_P2_3_5.py          ← P2.3.5 NEU
│   └── ...
│
├── 📁 application/                      ← Application Layer (Koordination)
│   ├── SiegerehrungApp_P2_3_5.py       ← P2.3.5 NEU
│   ├── Test_Siegerehrung_P2_3_5.py    ← P2.3.5 NEU
│   ├── demos/                          ← Demo-Skripte (neu organisiert!)
│   │   └── siegerehrung_quick.py
│   └── ...
│
├── 📁 infrastructure/                   ← Infrastructure Layer (Storage)
│   ├── ExtendedGameStorage_P2_3_4.py
│   └── ...
│
├── 📁 docs/                            ← Dokumentation (neu organisiert!)
│   ├── P2_3_5_DOKUMENTATION.md
│   ├── LERNPFAD.md
│   └── CODE_QUALITY.md
│
├── 📁 archive/                         ← Automatische Spielstände
│   └── save_auto_*.json
│
├── 📄 .flake8                          ← Flake8 Konfiguration
├── 📄 .pylintrc                        ← Pylint Konfiguration
├── 🐚 check_code_quality.sh            ← Bash-Script für QA
├── 🐍 check_code_quality.py            ← Python-Script für QA
│
└── 📄 venv/                           ← Virtual Environment (ignoriert)
```



## 🎯 Designprinzipien

| Prinzip | Umsetzung | Vorteil |
|---------|-----------|---------|
| **Separation of Concerns** | 3 Layer (Domain, App, Infra) | Klare Verantwortungen |
| **DRY** | Wiederverwendbare Komponenten | Kein Code-Duplikat |
| **KISS** | Klare, einfache Interfaces | Wartbar und verständlich |
| **SOLID** | Single Responsibility | Flexibel erweiterbar |
| **No Clutter** | Dateien in Richtordnern | Übersichtlich |

## 🔒 Code-Standards

### Flake8 (.flake8)
- Max Line Length: 100 Zeichen
- Max Complexity: 10
- PEP 8 Compliance

### Pylint (.pylintrc)
- Max Attributes: 10 pro Klasse
- Max Arguments: 8 pro Funktion
- Logging Format: new style

## 🚀 Verwendung

### Code-Qualität überprüfen (Bash)
```bash
bash check_code_quality.sh
```

### Code-Qualität überprüfen (Python)
```bash
python check_code_quality.py
```

### Demo ausführen
```bash
python application/demos/siegerehrung_quick.py
```

## 📋 Checkliste für neue Teile

Bevor Sie Code hinzufügen:

- [ ] Gehört der Code zu domain/, application/, oder infrastructure/?
- [ ] Keine Dateien im Root-Ordner (außer `check_code_quality.*`)?
- [ ] Dokumentation in `docs/`?
- [ ] Code läuft Flake8-Check?
- [ ] Imports sind sauber und spezifisch?
- [ ] Keine zirkulären Abhängigkeiten?

## 💡 Best Practices

✅ **Richtig:**
```python
# application/SiegerehrungApp_P2_3_5.py
from domain.FinalRanking_P2_3_5 import FinalRanking  # Clear path
from infrastructure.ExtendedGameStorage_P2_3_4 import ExtendedGameStorage
```

❌ **Falsch:**
```python
# In Random Root File
from .domain.FinalRanking_P2_3_5 import FinalRanking  # Bad location!
```

## 🎓 Ergebnis

Mit dieser Clean Code Struktur erhalten Sie:

✅ **Wartbarkeit** - Klare Ordnerstruktur  
✅ **Skalierbarkeit** - Leicht neue Features hinzufügen  
✅ **Qualität** - Automatische Code-Checks  
✅ **Dokumentation** - Alles an einem Ort  
✅ **Professionell** - Enterprise-Grade Struktur  
