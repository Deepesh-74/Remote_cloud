from __future__ import annotations

import os
from io import BytesIO
from statistics import mean

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image, UnidentifiedImageError

MAX_UPLOAD_MB = int(os.getenv("AIMFS_MAX_UPLOAD_MB", "20"))
MAX_UPLOAD_BYTES = MAX_UPLOAD_MB * 1024 * 1024
MAX_IMAGE_PIXELS = int(os.getenv("AIMFS_MAX_IMAGE_PIXELS", "20000000"))
Image.MAX_IMAGE_PIXELS = MAX_IMAGE_PIXELS

app = FastAPI(
    title="AI Media Forensics System",
    version="0.1.0",
    description="Explainable baseline analysis for uploaded images.",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv(
        "AIMFS_ALLOWED_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000"
    ).split(","),
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _read_upload(raw: bytes) -> bytes:
    if not raw:
        raise HTTPException(status_code=400, detail="Upload cannot be empty.")
    if len(raw) > MAX_UPLOAD_BYTES:
        raise HTTPException(
            status_code=413, detail=f"Upload exceeds the {MAX_UPLOAD_MB} MB limit."
        )
    return raw


def _inspect_image(raw: bytes) -> dict[str, object]:
    try:
        with Image.open(BytesIO(raw)) as image:
            image.load()
            rgb = image.convert("RGB")
            pixels = list(rgb.resize((32, 32)).getdata())
            channel_values = [value for pixel in pixels for value in pixel]
            average = mean(channel_values)
            spread = mean(abs(value - average) for value in channel_values)
            metadata_present = bool(image.getexif())
            return {
                "width": image.width,
                "height": image.height,
                "format": image.format,
                "metadata_present": metadata_present,
                "pixel_variation": round(spread, 3),
            }
    except (Image.DecompressionBombError, UnidentifiedImageError, OSError) as exc:
        raise HTTPException(
            status_code=400, detail="Upload must be a valid image within allowed limits."
        ) from exc


def _prediction(signals: dict[str, object]) -> dict[str, object]:
    variation = float(signals["pixel_variation"])
    metadata_present = bool(signals["metadata_present"])
    suspicion = min(
        0.85, max(0.1, 0.52 - variation / 255 + (0.08 if not metadata_present else -0.04))
    )
    label = "ai_enhanced" if suspicion >= 0.55 else "real"
    return {
        "label": label,
        "confidence": round(max(suspicion, 1 - suspicion), 3),
        "probabilities": {
            "real": round(1 - suspicion, 3),
            "ai_generated": round(suspicion * 0.45, 3),
            "ai_enhanced": round(suspicion * 0.4, 3),
            "hybrid": round(suspicion * 0.15, 3),
        },
        "generator_estimate": "unknown",
        "mode": "heuristic_baseline",
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "ai-media-forensics"}


@app.post("/analyze")
async def analyze(file: UploadFile = File(...)) -> dict[str, object]:
    raw = _read_upload(await file.read())
    return {"filename": file.filename, "signals": _inspect_image(raw)}


@app.post("/predict")
async def predict(file: UploadFile = File(...)) -> dict[str, object]:
    raw = _read_upload(await file.read())
    signals = _inspect_image(raw)
    return {"filename": file.filename, "signals": signals, "prediction": _prediction(signals)}


@app.post("/report")
async def report(file: UploadFile = File(...)) -> dict[str, object]:
    raw = _read_upload(await file.read())
    signals = _inspect_image(raw)
    return {
        "filename": file.filename,
        "prediction": _prediction(signals),
        "forensic_indicators": signals,
        "limitations": [
            "This is an explainable heuristic baseline, not a trained detector.",
            "Use results as investigative signals rather than proof.",
        ],
    }
