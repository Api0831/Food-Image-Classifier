# Model card

- Architecture: YOLOv8s classification; 100 UEC-FOOD100 classes.
- File: `models/food100.pt` (10,520,470 bytes).
- SHA-256: `ef0c6b13073f09ec13754cca990efb37683f8cdfb7eb6cc6b48c374f88552244`.
- Source: unchanged checkpoint from the original graduation-project Streamlit application.
- Checkpoint producer version: Ultralytics 8.1.4.
- Checkpoint timestamp: 2024-03-14T01:10:47.207996 (timezone not recorded).
- Current inference: CPU, RGB input, image size 128, modern pinned runtime in requirements.txt.
- Label mapping: all 100 model label names match labels.py.

## Intended use

Educational food-classification demo and local experimentation. One dominant food category per image; no object localization or nutrition estimates. Non-food inputs still receive food labels. Scores are not calibrated correctness probabilities.

## Evidence and limitations

The checkpoint is unchanged; the runtime was modernized for installation compatibility. Historical preprocessing and scores may differ from modern inference. Original data provenance, split reproducibility and overlap were not independently audited. See experiments/README.md for the inconsistent archived epoch counts. No verified dataset-wide test accuracy is claimed.

Three local test images were used for inference smoke checks. Their filenames and actual predictions are in prediction_examples.json; images themselves are excluded. This tiny sample is not a benchmark and includes failures if any occur.

Source code is AGPL-3.0. Dataset and dependency rights are separate; see THIRD_PARTY_NOTICES.md. Load only trusted model files: this checkpoint uses Python-based serialization.
