"""Download YOLOv8n model for vehicle classification."""

import os


MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "yolov8n.pt")


def download_model():
    """Download YOLOv8n .pt model (lightweight, ~6MB)."""
    os.makedirs(MODEL_DIR, exist_ok=True)

    if os.path.exists(MODEL_PATH):
        print(f"Model already exists: {MODEL_PATH}")
        return

    print("Downloading YOLOv8n model (~6MB)...")

    try:
        import torch

        # Fix for PyTorch 2.6+ weights_only default change
        _original_load = torch.load

        def _patched_load(*args, **kwargs):
            kwargs.setdefault("weights_only", False)
            return _original_load(*args, **kwargs)

        torch.load = _patched_load

        from ultralytics import YOLO

        # Download the model (auto-downloads from ultralytics hub)
        model = YOLO("yolov8n.pt")

        # Move to models directory
        if os.path.exists("yolov8n.pt"):
            os.rename("yolov8n.pt", MODEL_PATH)

        # Restore original torch.load
        torch.load = _original_load

        print(f"Model downloaded successfully: {MODEL_PATH}")

    except ImportError as e:
        print("=" * 60)
        print(f"  Missing package: {e}")
        print("  Install with: pip install ultralytics")
        print("  Then run this script again.")
        print("=" * 60)


if __name__ == "__main__":
    download_model()
