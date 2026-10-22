# Verification record

Verified on 22 October 2026, Windows, Python 3.11.7, CPU inference.

## Passed

- Python syntax checks for application, labels and evaluation script.
- Original checkpoint SHA-256 unchanged.
- Model loads with the pinned runtime; all 100 English model labels have Chinese mappings.
- Three real local test images produce Top-5 predictions (including one incorrect Top-1 prediction). See prediction_examples.json.
- Browser test: application opens, a JPG can be uploaded, the classify button produces a success message and Top-5 results without a Streamlit exception.
- Browser test: invalid PNG content produces the expected readable error.
- Application homepage captured in app-preview.png; no dataset image included.
- `pip check` reports no broken requirements; `pip install --dry-run -r requirements.txt` resolves the installed core versions.
- Evaluation command `--help` works. Full dataset evaluation was not run.

## Runtime decisions

PyTorch 2.14.1 failed DLL initialization on the verification machine. The release uses official CPU wheels for torch 2.7.1 and torchvision 0.22.1, with Ultralytics 8.4.183 and Streamlit 1.65.0. The original checkpoint reports Ultralytics 8.1.4; it was not retrained or modified.

Dependencies are installed explicitly. Runtime automatic package installation is disabled in the application and evaluation command. The complete verified Windows environment is recorded in requirements-lock-windows.txt; macOS/Linux have not been exercised.

## Scope

This is a local functionality check, not a performance, deployment, security or data-leakage audit. No whole-dataset accuracy is claimed. Historical training results remain separately documented in experiments/README.md.
