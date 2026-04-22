# War Prediction & Conflict Simulator

A dual-purpose geopolitical intelligence system combining ML-based conflict prediction with agent-based war simulation.

## Features

### Prediction Engine
- Conflict probability scoring (0-100) for country-dyad pairs
- SHAP-based risk factor explanations
- Hot zone detection for conflict clustering
- Alliance web visualization
- Temporal trend analysis
- Conflict type classification (civil war, interstate, proxy, terrorism)
- News sentiment analysis via NLP pipeline

### Simulation Engine
- Custom scenario builder (select nations, set parameters)
- Agent-based war simulation using Mesa framework
- Alliance cascade modeling (WWI-style chain reactions)
- Outcome forecasting (duration, casualties, economic damage)
- Nuclear deterrence toggle
- Ceasefire probability modeling

### Interfaces
- **React Frontend** - 3D globe dashboard with Three.js
- **Streamlit App** - Analytical interface with charts and SHAP explanations

## Tech Stack

| Layer | Technology |
|-------|------------|
| ML Models | XGBoost, PyTorch, scikit-learn |
| NLP | HuggingFace Transformers |
| Simulation | Mesa (ABM), NetworkX |
| API | FastAPI |
| Frontend | React 18, Three.js, Tailwind CSS |
| Visualization | Plotly, PyDeck, Recharts |

## Project Structure

```
WarPredict1/
├── backend/              # FastAPI backend
│   ├── api/             # Routes & schemas
│   ├── models/          # XGBoost, LSTM, NLP models
│   ├── simulation/     # Mesa ABM, alliance cascade
│   └── utils/           # Data loading, feature engineering
├── frontend/            # React + Vite + Three.js
│   └── src/
│       ├── components/ # Globe, Dashboard, Simulator
│       ├── store/       # Zustand state
│       └── api/         # Axios client
├── streamlit_app/        # Analytical UI
│   └── pages/          # Prediction, Simulator, Explorer, Insights
└── data/               # Raw & processed datasets
```

## Quick Start

### Docker (Recommended)

```bash
docker-compose up --build
```

- Frontend: http://localhost:5173
- API: http://localhost:8000
- Streamlit: http://localhost:8501

### Manual Setup

```bash
# Backend
pip install -r requirements.txt
uvicorn backend.api.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

## Data Sources

The project includes sample data for testing. For production use, download real datasets:

| Dataset | Source | Notes |
|---------|-------|-------|
| UCDP Conflict | ucdp.uu.se/downloads/ | CSV format |
| SIPRI Military | milex.sipri.org/ | Excel format |
| Fragile States | fragilestatesindex.org/ | Excel format |
| Global Peace Index | visionofhumanity.org/ | GPI-2024.csv |
| Polity V | systemicpeace.org/ | Excel format |

Run data loader:
```bash
python backend/utils/data_loader.py
```

## Ethical Considerations

- This system is for academic research and conflict prevention awareness
- Predictions are probabilistic, not deterministic
- Model biases must be acknowledged
- Not intended for actual military planning