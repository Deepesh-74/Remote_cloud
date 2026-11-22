# AI Media Forensics System

A runnable baseline for inspecting uploaded images and reporting simple forensic signals. It is designed as a transparent starting point for a stronger trained detector, not as proof that an image is authentic or synthetic.

## Current Features

- FastAPI backend with health, analysis, prediction, and report endpoints
- Image validation with file-size and image-pixel limits
- Explainable heuristic baseline classification for `real` or `ai_enhanced`
- Next.js upload dashboard that works locally, in Docker, and in Codespaces
- Docker Compose setup for backend and frontend
- GitHub Actions API health checks
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

Frontend, in another terminal:

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

Use `multipart/form-data` with an image field named `file`. The default maximum upload size is 20 MB.

## Use From Mobile

1. Open this repository in GitHub on your phone.
2. Select **Code** then **Codespaces**.
3. Create a codespace on `main`.
4. In one terminal, run `uvicorn backend.app.main:app --host 0.0.0.0 --port 8000`.
5. In a second terminal, run `cd frontend && npm run dev`.
6. Open the forwarded port 3000 preview. The dashboard will reach the backend through its server-side proxy.
7. Run `codex` whenever you want to work with Codex in that cloud workspace.

The development container installs Codex CLI and project dependencies automatically. Authenticate through the prompt, or configure `OPENAI_API_KEY` as a GitHub Codespaces secret. The laptop does not need to remain online.

## Limitations And Next Work

The current detector is a heuristic baseline. It should be used only as an investigative signal. The next meaningful technical step is adding a trained model, calibration, robust evaluation data, and heatmap explainability before relying on predictions.

## Environment Variables

Copy `.env.example` to `.env` when you need to override application settings.
