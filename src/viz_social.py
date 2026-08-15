"""Social-ready chart export using Altair + vl-convert.

Produces publication-quality PNG images for Instagram/Twitter posting.
Uses the @unwelcomedata brand palette (Coolors) and Inter typography.
No browser needed — rendering happens via vl-convert.

Key functions:
    social_scatter()            — X-Y scatter with categorical coloring
    social_ranked_bars()        — Top/bottom N horizontal bars
    social_diverging_bars()     — Deviation from expected (diverging)
    social_comparison()         — Group mean comparison bars
    social_trend()              — Line chart over time
    social_choropleth()         — US state map (heat or category)
    social_bivariate_choropleth() — Two-variable 3x3 color matrix map
    save_social()               — Export Altair chart to PNG with watermark

Platform presets:
    instagram_portrait : 1080x1350
    twitter_landscape  : 1600x900
    instagram_square   : 1080x1080

Usage:
    from src.viz_social import social_scatter, save_social
    chart = social_scatter(df, x='col_a', y='col_b', title='My Chart')
    save_social(chart, cfg, 'my_chart_filename', preset='twitter_landscape')
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import altair as alt
import pandas as pd
import vl_convert as vlc
from PIL import Image, ImageDraw, ImageFont

# Import shared brand library from workspace root
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "shared"))
from viz import (  # noqa: E402
    BRAND, COOLORS, COOLORS_SCALE, PALETTE, PRESETS,
    REGION_COLORS, SOCIAL_THEME,
)

# ---------------------------------------------------------------------------
# Register @unwelcomedata Altair theme
# ---------------------------------------------------------------------------

def _unwelcome_theme() -> dict:
    """Altair theme config using brand identity."""
    return {
        "config": {
            "background": SOCIAL_THEME["background"],
            "font": SOCIAL_THEME["font"],
            "title": SOCIAL_THEME["title"],
            "axis": SOCIAL_THEME["axis"],
            "legend": SOCIAL_THEME["legend"],
            "view": SOCIAL_THEME["view"],
            "range": SOCIAL_THEME["range"],
            "mark": SOCIAL_THEME["mark"],
            "bar": {"cornerRadiusEnd": 3},
            "point": {"size": 60, "filled": True},
            "line": {"strokeWidth": 3},
        }
    }


alt.themes.register("unwelcomedata", _unwelcome_theme)
alt.themes.enable("unwelcomedata")


# ---------------------------------------------------------------------------
# Chart builders — fill in per project
# ---------------------------------------------------------------------------

# TODO: Copy and adapt chart functions from dui-by-state/src/viz_social.py
# as needed for this project. Common starting points:
#
# - social_scatter(df, x, y, color_by, title, subtitle, source, preset)
# - social_ranked_bars(df, x, y, title, top_n, bottom_n, preset)
# - social_diverging_bars(df, value_col, expected, title, top_n, preset)
# - social_comparison(df, group_col, value_col, title, preset)
# - social_trend(df, x, y, title, preset)
# - social_choropleth(df, column, title, mode, preset)


# ---------------------------------------------------------------------------
# Save to PNG
# ---------------------------------------------------------------------------

def save_social(
    chart: alt.Chart,
    cfg: dict[str, Any],
    filename: str,
    preset: str = "twitter_landscape",
    add_watermark: str = "@unwelcomedata",
    scale: float = 2.0,
) -> Path:
    """Render an Altair chart to PNG and save to outputs/.

    Args:
        chart:         Altair Chart object.
        cfg:           Project config dict (needs paths.outputs).
        filename:      Output filename without extension.
        preset:        Platform preset for final dimensions.
        add_watermark: Watermark text (bottom-right corner).
        scale:         Render scale factor for sharpness.

    Returns:
        Path to saved PNG.
    """
    out_dir = Path(cfg["paths"].get("outputs_social", cfg["paths"]["outputs"]))
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{filename}.png"

    w_px, h_px, _ = PRESETS[preset]

    # Render to PNG bytes via vl-convert
    png_bytes = vlc.vegalite_to_png(
        chart.to_dict(),
        scale=scale,
    )

    # Write initial render
    out_path.write_bytes(png_bytes)

    # Resize to exact platform dimensions + add watermark
    img = Image.open(out_path)
    img = img.resize((w_px, h_px), Image.LANCZOS)

    if add_watermark:
        img = _draw_watermark(img, add_watermark)

    img.save(out_path, format="PNG", optimize=True)
    print(f"Saved social chart -> {out_path}  ({w_px}x{h_px} px, preset={preset})")
    return out_path


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _preset_size(preset: str) -> tuple[int, int]:
    """Get (width, height) in pixels for a preset."""
    if preset not in PRESETS:
        raise ValueError(f"Unknown preset '{preset}'. Choose from: {list(PRESETS)}")
    w, h, _ = PRESETS[preset]
    return w, h


def _pretty(col: str) -> str:
    """Convert column_name to Pretty Title."""
    return col.replace("_", " ").title()


def _add_source(chart: alt.Chart, source: str, width: int) -> alt.Chart:
    """Add a source attribution line below the chart."""
    source_text = alt.Chart(
        pd.DataFrame([{"text": f"Source: {source}"}])
    ).mark_text(
        align="left", fontSize=9, color=PALETTE["mid"], dy=10,
    ).encode(
        text="text:N",
    ).properties(width=width - 120, height=20)

    return alt.vconcat(chart, source_text).configure_concat(spacing=5)


def _draw_watermark(img: Image.Image, text: str) -> Image.Image:
    """Draw watermark text on bottom-right of image."""
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 16)
    except (OSError, IOError):
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    x = img.width - text_w - 20
    y = img.height - text_h - 15

    draw.text((x, y), text, fill=(156, 163, 175, 180), font=font)
    return img
