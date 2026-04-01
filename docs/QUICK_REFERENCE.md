# 🧹 Clean Code: Schnellreferenz

## 📁 Wo gehört was hin?

| Element | Ort | Beispiel |
|---------|-----|----------|
| Geschäftslogik | `domain/` | `FinalRanking_P2_3_5.py` |
| App-Koordination | `application/` | `SiegerehrungApp_P2_3_5.py` |
| Demo-Skripte | `application/demos/` | `siegerehrung_quick.py` |
| Tests | `application/` | `Test_Siegerehrung_P2_3_5.py` |
| Storage/Persistierung | `infrastructure/` | `ExtendedGameStorage_P2_3_4.py` |
| Dokumentation | `docs/` | `P2_3_5_DOKUMENTATION.md` |
| Config (Code-Standards) | Root | `.flake8`, `.pylintrc` |
| QA-Tools | Root | `check_code_quality.*` |

## ✅ Checkliste für neue Features

Vor dem Commit:

- [ ] Datei ist in richtigem Folder (domain/app/infra)?
- [ ] Keine fremden Dateien im Root?
- [ ] `python check_code_quality.py` läuft sauber?
- [ ] Imports sind korrekt (keine zirkulären)?
- [ ] Dokumentation in `docs/` aktualisiert?
- [ ] Tests vorhanden und grün?

## 🚀 Standard-Befehle

```bash
# Demo ausführen
python application/demos/siegerehrung_quick.py

# Code-Qualität checken
bash check_code_quality.sh

# Tests ausführen
python application/Test_Siegerehrung_P2_3_5.py

# Aktueller Git-Status
git status

# Zeige alle Python-Dateien
find domain application infrastructure -name "*.py" | sort
```

## 🎓 Lernhierarchie

```
P2.3.1 (Player Mgmt)
  ↓
P2.3.2 (Game Round)
  ↓
P2.3.3 (Ranking)
  ↓
P2.3.4 (Game State)
  ↓
P2.3.5 (Siegerehrung) ← AKTUELL
```

Siehe [docs/LERNPFAD.md](docs/LERNPFAD.md) für Details.

## 📚 Dokumentation

- `docs/CODE_QUALITY.md` - Clean Code Struktur
- `docs/P2_3_5_DOKUMENTATION.md` - Feature-Details
- `docs/LERNPFAD.md` - Lektions-Hierarchie
- `LERNPFAD_P2_3_COMPLETE.md` - Kompletter Überblick

## 💡 Best Practice

✅ **Immer tun:**
- Code in domain/application/infrastructure
- Docs in docs/
- Tests in application/
- Demos in application/demos/

❌ **Nie tun:**
- Dateien im Root-Folder (außer Config & Tools)
- Zirkuläre Abhängigkeiten
- Magische Strings/Zahlen
- Code ohne Dokumentation
