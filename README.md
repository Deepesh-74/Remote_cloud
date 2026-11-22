# AI Media Forensics System

A runnable baseline for inspecting uploaded images and reporting simple forensic signals. It is designed as a transparent starting point for a stronger trained detector, not as proof that an image is authentic or synthetic.

## Current Features

- FastAPI backend with health, analysis, prediction, and report endpoints
- Image validation with dimensions, format, EXIF-presence, and pixel-variation signals
- Explainable heuristic baseline classification for `real` or `ai_enhanced`
- Next.js upload dashboard
- Docker Compose setup for backend and frontend
- A GitHub Actions API health check
- GitHub Codespaces support for browser and mobile development

## Run Locally

### Docker

```bash
docker compose up --build
```

Open the dashboard at `http://localhost:3000`. The API is available at `http://localhost:8000`, including interactive docs at `/docs`.

### Development

Backend:

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
pip install -r requirements.txt
uvicorn backend.app.main:app --reload --port 8000
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

## API

- `GET /health` returns service status
- `POST /analyze` extracts forensic signals from an image upload
- `POST /predict` returns the baseline classification and probabilities
- `POST /report` returns a consolidated report

Use `multipart/form-data` with an image field named `file`.

## Use From Mobile

1. Open this repository in GitHub on your phone.
2. Select **Code** then **Codespaces**.
3. Create a codespace on `main`.
4. Open the terminal and run `codex`.

The development container installs Codex CLI automatically. Authenticate through the prompt, or configure `OPENAI_API_KEY` as a GitHub Codespaces secret. The laptop does not need to remain online.

## Limitations And Next Work

The current detector is a heuristic baseline. It should be used only as an investigative signal. The next meaningful technical step is adding a trained model, calibration, robust evaluation data, and heatmap explainability before relying on predictions.

## Environment Variables

Copy `.env.example` to `.env` when you need to override application settings.
