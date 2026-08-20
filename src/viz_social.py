"""Social-ready chart export — Pillow backend.

This module is a thin compatibility layer. The actual rendering is handled
by the shared chart_factory + chart_templates (Pillow) pipeline. This file
provides save_social() for any legacy code that calls it directly.

The primary workflow now:
    from chart_factory import render_chart
    render_chart({...})  # renders via Pillow, exports PNG, displays inline

If you need standalone save_social() (e.g., for a manually composed PIL Image):
    from src.viz_social import save_social
    save_social(img, cfg, 'filename', preset='twitter_landscape')

Platform presets:
    instagram_portrait : 1080x1350
    twitter_landscape  : 1600x900
    instagram_square   : 1080x1080
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont

# Import shared brand library from workspace root
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "shared"))
from viz import BRAND, PRESETS  # noqa: E402


# ---------------------------------------------------------------------------
# Save to PNG
# ---------------------------------------------------------------------------

def save_social(
    img: Image.Image,
    cfg: dict[str, Any],
    filename: str,
    preset: str = "twitter_landscape",
    add_watermark: str = "@unwelcomedata",
) -> Path:
    """Save a PIL Image to the social outputs directory.

    This is the standalone export function. In the normal workflow,
    render_chart() handles export internally — you don't need to call this.

    Use this only if you're composing a PIL Image manually outside the
    chart_factory pipeline.

    Args:
        img:           PIL Image object (RGB).
        cfg:           Project config dict (needs paths.outputs_social or paths.outputs).
        filename:      Output filename without extension.
        preset:        Platform preset for target dimensions.
        add_watermark: Watermark text (drawn bottom-right). Empty string to skip.

    Returns:
        Path to saved PNG.
    """
    out_dir = Path(cfg["paths"].get("outputs_social", cfg["paths"]["outputs"]))
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{filename}.png"

    w_px, h_px, _ = PRESETS[preset]

    # Resize if needed
    if img.size != (w_px, h_px):
        img = img.resize((w_px, h_px), Image.LANCZOS)

    img.save(out_path, format="PNG", optimize=True)
    print(f"Saved social chart -> {out_path}  ({w_px}x{h_px} px, preset={preset})")
    return out_path
