# weldlytics

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![Hackathon](https://img.shields.io/badge/Beyond%20Transformers%20Hackathon-purple)]()

---

##  Problem Statement

In MSMEs, workers often increase welding current to finish faster, resulting in **weak, rejected welds** that fail quality inspection. The core problem: **no real‑time feedback** – a weld is only declared bad after it's finished and inspected, wasting time, material, and money.

**Weldlytics** solves this by retrofitting old welding machines with a low‑cost IoT device (ESP32 + current sensor) and using ai based system to predict weld quality **during the weld** and provide instant **GOOD / REJECTED** feedback with explainable reasons.

---

##  Key Features

| Module | Description |
|--------|-------------|
| 👨‍🏭 **Worker Screen** | Extremely simple interface – big colored circle, GOOD/BAD/ADJUST, one‑line suggestion (no charts, no numbers) |
| 📊 **Real‑time Monitor** | Live current graph with spike/drop detection, stability indicator, machine ON/OFF status |
| 🧠 **AI Insight Panel** | Explainability: why a weld failed (e.g., "current dropped at 1.2s"), confidence score, root cause analysis |
| 💰 **Cost Savings Dashboard** | Material saved, rework saved, defects prevented – shows business value (₹12,500 saved this week) |
| 🧵 **Consumable Tracker** | Electrode usage, gas consumption, low stock alerts |
| 📈 **Learning Status (BDH)** | Continuous learning – accuracy improves from 70% → 90% over days |
| 🚨 **Alert Center** | Severity‑based alerts (HIGH/MEDIUM/LOW), machine risk assessment |
| ⚙️ **Settings & Integration** | Machine selection, sensor calibration, PLC/SCADA connectivity |
| 📋 **Analytics** | Historical quality distribution, confidence trends, export to CSV |
| 💬 **AI Co‑pilot** | LLM‑powered chat (mock LLM ready for Pathway integration) – ask about current, costs, accuracy, consumables |

---

- **Data generator** simulates ESP32 readings (current, temp, vibration)
- **BDH model** uses a Random Forest classifier trained on synthetic welding data
- **Real‑time queue** passes data between pipeline and dashboard
- **No external database** – all state kept in memory (easily extendable to TimescaleDB)

---

##  Getting Started

### Prerequisites

- Python 3.10 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/Weldlytics.git
   cd Weldlytics

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
3. **Run the application**
   ```bash
   streamlit run app.py
