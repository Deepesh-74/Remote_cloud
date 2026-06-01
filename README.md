# AI Media Forensics System

Production-style AI media forensics platform for detecting whether an uploaded image is real, AI-generated, AI-enhanced, or hybrid. The project is structured as a resume/research-grade prototype with a FastAPI backend, modular PyTorch ML package, forensic analysis modules, robustness evaluation scripts, and a modern dashboard frontend.

## What This Project Does

- Classifies images as `real`, `ai_generated`, `ai_enhanced`, or `hybrid`
- Estimates a likely source generator such as Stable Diffusion, Midjourney, DALL-E, FLUX, or GAN-based
- Generates explainability heatmaps for suspicious image regions
- Extracts metadata, EXIF signals, compression indicators, frequency-domain features, and texture inconsistency metrics
- Produces structured forensic reports through REST endpoints
- Includes dataset, training, calibration, robustness testing, and evaluation scaffolding

The default inference mode uses a transparent heuristic ensemble so the application can run before model weights are trained. For research-grade results, train a model with the scripts in `scripts/` and configure `AIMFS_MODEL_CHECKPOINT`.

## Architecture

```text
backend/       FastAPI app, REST endpoints, schemas, report orchestration
frontend/      Next.js dashboard with upload, charts, heatmap, and report panels
ml/aimfs/      Reusable ML, forensics, training, explainability, and evaluation package
scripts/       Training, robustness evaluation, and smoke-test entrypoints
docker/        Backend and frontend Dockerfiles
tests/         Unit and API test scaffolding
models/        Local checkpoint output directory
datasets/      Expected local dataset root
```

## API Endpoints

- `POST /predict` - classification, confidence, probability distribution, generator estimate
- `POST /analyze` - forensic indicators only
- `POST /heatmap` - explainability heatmap as base64 PNG
- `POST /report` - full prediction, heatmap, and forensic report
- `GET /health` - service health

## Quick Start

### Backend

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn backend.app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000` and set `NEXT_PUBLIC_API_URL=http://localhost:8000` if the API is not on the default port.

### Docker

```bash
docker compose up --build
```

## Dataset Layout

Place datasets under `datasets/` using class folders:

```text
datasets/media_forensics/
  real/
  ai_generated/
  ai_enhanced/
  hybrid/
```

Optional generator metadata can be provided as CSV with columns:

```text
path,label,generator
```

## Training

Train a transfer-learning classifier:

```bash
python scripts/train.py --data-root datasets/media_forensics --model efficientnet_b0 --epochs 20
```

Outputs are written to `models/checkpoints/` by default. Configure the backend to use a trained checkpoint:

```bash
AIMFS_MODEL_CHECKPOINT=models/checkpoints/best.pt
```

## Robustness Evaluation

```bash
python scripts/evaluate_robustness.py --data-root datasets/media_forensics --checkpoint models/checkpoints/best.pt
```

The evaluator applies brightness, saturation, blur, JPEG compression, resize, screenshot-like recompression, and noise perturbations.

## Benchmark And False Positive Analysis

```bash
python scripts/benchmark.py --data-root datasets/media_forensics --checkpoint models/checkpoints/best.pt
python scripts/analyze_false_positives.py --benchmark-report storage/benchmark_report.json
```

These scripts generate benchmark metrics and surface high-confidence real-image false positives for manual review.

## Research Notes

This project is designed to be honest about uncertainty:

- The default heuristic detector is explainable but not a substitute for a trained model.
- Confidence calibration is included so logits can be temperature-scaled after validation.
- Robustness scripts help expose false positives under common social-media transformations.
- For publication-style reporting, benchmark against held-out real camera images and multiple generator families.

## Environment Variables

Copy `.env.example` to `.env` and adjust paths or service settings.

## Safety And Limitations

AI media forensics is probabilistic. Results should be treated as investigative signals, not absolute proof. A high-quality detector must be trained and validated on carefully separated datasets that include camera diversity, editing diversity, generator diversity, and real-world compression pipelines.
