from io import BytesIO

from fastapi.testclient import TestClient
from PIL import Image

from backend.app.main import app

client = TestClient(app)


def image_bytes() -> bytes:
    buffer = BytesIO()
    Image.new("RGB", (12, 12), color=(32, 120, 220)).save(buffer, format="PNG")
    return buffer.getvalue()


def test_health() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "ai-media-forensics"}


def test_report_returns_baseline_for_valid_image() -> None:
    response = client.post(
        "/report",
        files={"file": ("sample.png", image_bytes(), "image/png")},
    )

    assert response.status_code == 200
    assert response.json()["prediction"]["mode"] == "heuristic_baseline"


def test_report_rejects_invalid_image() -> None:
    response = client.post(
        "/report",
        files={"file": ("not-image.txt", b"not an image", "text/plain")},
    )

    assert response.status_code == 400
