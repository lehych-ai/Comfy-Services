# ComfyUI · Vast.ai Template

A two-repo setup for running ComfyUI on Vast.ai with preset-based model downloading.

---

## Repository structure

### `comfy-services` (this repo)
Contains the preset downloader service and a minimal static frontend.

```
services/
├── __init__.py
├── preset_downloader.py   ← define your presets here
└── static/
    └── script.js
```

### `Start-Command`
Contains the raw startup script with custom node definitions — already configured.

---

## Vast.ai template config

**Docker image**
```
vastai/comfy:v0.15.1-cuda-13.1-py312
```

**Exposed ports**

| Port | Service           |
|------|-------------------|
| 8188 | ComfyUI           |
| 8888 | JupyterLab        |
| 8081 | Preset downloader |

---

## Adding models to presets

Open `services/preset_downloader.py` and locate `PRESET_FILES`.

For each preset, add tuples in the following format:

```python
("https://huggingface.co/username/repo/resolve/main/file.safetensors", "destination_folder", None),
```

**Available destination folders**

- `diffusion_models`
- `loras`
- `vae`
- `text_encoders`
- `checkpoints`
- `clip_vision`
- `upscale_models`
- `controlnet`

> If your models are gated on Hugging Face, set the `HF_TOKEN` environment variable before running.
