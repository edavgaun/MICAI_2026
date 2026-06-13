# 🇲🇽 Evolution of the Mexican AI Ecosystem

This Streamlit application explores the evolution of the Artificial Intelligence research ecosystem in Mexico using bibliometric and network analysis techniques. The project is based on proceedings data (MICAI and related sources) and visualizes how institutions, researchers, and collaborations have evolved over time.

---

## 📊 Project Overview

This dashboard allows users to explore:

- 🧠 Evolution of AI research in Mexico over time  
- 🏛️ Institutional collaboration networks  
- 🌍 International vs national collaboration patterns  
- 📚 Research areas and their temporal dynamics  
- 🧩 Key institutions and their connectivity in the ecosystem  

The analysis is based on:
- Co-authorship networks  
- Institution-level aggregation  
- Country normalization  
- Temporal segmentation of AI development eras

🧱 Project Structure
## 🧱 Project Structure

```text
mexican-ai-ecosystem/
│
├── app.py
├── requirements.txt
├── README.md
│
├── data/
│   └── metadata_extraida.csv
│
├── Moudules/
│   ├── Ecosystem_Setup.py
│   ├── Inicio.py
│
├── assets/
│   └── (imagenes, logos si quieres)
│
└── pages/
    ├── Network.py
    └── 
```

---

## 🧬 Key Features

### 🕸️ Collaboration Network

Interactive network where:

- **Nodes** = institutions  
- **Edges** = co-authorship relationships  
- **Node size** = number of papers  
- **Edge weight** = collaboration frequency  
- **Colors** = domestic vs international collaboration  

### ⏳ Temporal Evolution

The ecosystem is divided into four analytical eras:

- Era 1: The Islands (1997–2008)  
- Era 2: The Bridges (2009–2019)  
- Era 3: Forced Virtualization (2020–2022)  
- Era 4: Solid Networks (2023–2026)  

---

## 🏫 Institutional Analysis

Includes:

- Normalized institution names  
- Unified research centers (ITESM, UNAM, IPN, etc.)  
- Country-level aggregation  
- Standardized collaboration mapping  

---

## 📁 Data Sources

The dataset is derived from:

- MICAI conference metadata  
- Research paper author affiliations  
- Institutional and country metadata enrichment  

> Note: Data preprocessing includes extensive normalization of institution names and country extraction.

---


👤 Author
Edgar Avalos Gauna, Rice University
Research in AI systems, data science, and complex networks applied to scientific ecosystems.


⚠️ Disclaimer
This project is for academic and research purposes. Institution normalization is heuristic-based and may contain approximations.
