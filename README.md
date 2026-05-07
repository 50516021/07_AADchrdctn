# 07_AADchrdctn
Channel reduction optimization of AAD method (non-linear)

This repository now includes a compact non-linear channel reduction helper:

- `optimize_aad_channels_nonlinear(...)` in `aad_channel_reduction.py`
- keeps the smallest set of channels that meets a non-linear retention target
- supports:
  - `retention_target` in `(0, 1]`
  - non-linear emphasis `gamma > 0`
  - mandatory floor `min_channels`

## Run tests

```bash
python -m unittest discover -s tests -p "test_*.py"
```
