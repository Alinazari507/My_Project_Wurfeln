# 🎲 Dice Game Project (DDD & Persistence Implementation)

This project is a professional dice game built using **Domain-Driven Design (DDD)** principles, featuring a robust persistence layer and a terminal-based UI.

## 🏗️ Architecture (Layered Pattern)
- **Domain:** Core game logic, dice visualization, and ranking systems (`FinalRanking`, `GameRound`, `DiceVisualizer`).
- **Application:** Orchestration of game flow and interactive lobby management (`SiegerehrungApp`).
- **Infrastructure:** Relational database management using **SQLite**, handling game sessions and real-time roll tracking.

## ✨ Key Features (Module P2.5)
- **Interactive Lobby:** Resume paused games or start new tournaments.
- **Data Safety:** Real-time persistence of every dice roll to prevent data loss.
- **Professional UI:** Rich-formatted tables and ASCII dice art for an immersive experience.
- **Verified Quality:** Comprehensive unit tests for the infrastructure layer.

## 🚀 Quick Start
1. **Activate Environment:** `source venv/bin/activate`
2. **Install Dependencies:** `pip install rich pyhamcrest`
3. **Run the Game:** `python application/SiegerehrungApp_P2_3_5.py`
4. **Run Tests:** `python3 -m unittest discover test`

## 📁 Project Structure
- `/application`: App controllers and Lobby logic.
- `/domain`: Pure business logic and visualizers.
- `/infrastructure`: SQLite storage and schema management.
- `/test`: Unit tests and TDD suite.