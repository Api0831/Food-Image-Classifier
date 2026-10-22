"""Evaluate the included checkpoint against a separately obtained dataset."""
import argparse
from pathlib import Path
import os

# Install dependencies explicitly, never during a prediction.
os.environ["YOLO_AUTOINSTALL"] = "false"
from ultralytics import YOLO


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, required=True,
                        help="Dataset root with train/, val/ and optionally test/ class folders")
    parser.add_argument("--split", choices=["val", "test"], default="test")
    args = parser.parse_args()
    if not (args.data / args.split).is_dir():
        parser.error(f"Missing split directory: {args.data / args.split}")
    root = Path(__file__).resolve().parents[1]
    model = YOLO(root / "models" / "food100.pt")
    expected = set(model.names.values())
    actual = {p.name for p in (args.data / args.split).iterdir() if p.is_dir()}
    if actual != expected:
        parser.error("Class folder names must match all 100 model labels exactly.")
    metrics = model.val(data=str(args.data.resolve()), split=args.split,
                        imgsz=128, batch=32, device="cpu", workers=0,
                        project=str(root / "runs"), name="evaluation")
    print(f"Top-1: {metrics.top1:.4%}; Top-5: {metrics.top5:.4%}")


if __name__ == "__main__":
    main()
