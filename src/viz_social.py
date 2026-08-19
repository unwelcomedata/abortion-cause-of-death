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
# Chart builders — project-specific for abortion-cause-of-death
# ---------------------------------------------------------------------------

def social_comparison_bars(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    color_col: str | None = None,
    title: str = "",
    subtitle: str = "",
    source: str = "WONDER CDC",
    preset: str = "twitter_landscape",
) -> alt.Chart:
    """Grouped horizontal bars comparing categories.
    
    Args:
        df: DataFrame with data
        x_col: Column for bar lengths (deaths, counts, etc.)
        y_col: Column for bar grouping (causes, etc.)
        color_col: Optional column for color distinction
        title: Chart title
        subtitle: Subtitle/description
        source: Data source attribution
        preset: Platform preset (twitter_landscape, etc.)
    
    Returns:
        Altair Chart object (ready for save_social)
    """
    w_px, h_px, _ = PRESETS[preset]
    width = w_px - 120
    height = h_px - 180
    
    if color_col:
        color_scale = alt.Scale(domain=df[color_col].unique().tolist(),
                                range=[PALETTE["cat_2"], PALETTE["cat_5"]])
        color = alt.Color(f"{color_col}:N", scale=color_scale, title=color_col)
    else:
        color = alt.value(PALETTE["primary"])
    
    bars = alt.Chart(df).mark_barh().encode(
        x=alt.X(f"{x_col}:Q", title="Deaths"),
        y=alt.Y(f"{y_col}:N", title="", sort="-x"),
        color=color,
        tooltip=[y_col, x_col],
    ).properties(
        width=width,
        height=height,
        title=alt.TitleFrame(
            text=title,
            subtitle=subtitle,
            anchor="start",
            offset=10,
        ),
    )
    
    return bars.configure_axis(
        labelFontSize=10,
        titleFontSize=11,
    )


def social_sex_stacked_bars(
    df: pd.DataFrame,
    title: str = "",
    subtitle: str = "",
    source: str = "WONDER CDC",
    preset: str = "twitter_landscape",
) -> alt.Chart:
    """Horizontal stacked bars showing sex breakdown for top 10 causes.
    
    DataFrame should have columns: cause, male_deaths, female_deaths
    
    Args:
        df: Must include: cause, male_deaths, female_deaths
        title: Chart title
        subtitle: Subtitle
        source: Data source
        preset: Platform preset
    
    Returns:
        Altair Chart object
    """
    from shared.viz import SEX_COLORS
    
    w_px, h_px, _ = PRESETS[preset]
    width = w_px - 120
    height = h_px - 180
    
    # Melt for Altair stacking
    df_long = df.melt(
        id_vars=["cause"],
        value_vars=["male_deaths", "female_deaths"],
        var_name="sex",
        value_name="deaths"
    )
    df_long["sex"] = df_long["sex"].str.replace("_deaths", "").str.capitalize()
    
    color_scale = alt.Scale(
        domain=["Male", "Female"],
        range=[SEX_COLORS.get("Male", PALETTE["cat_2"]),
               SEX_COLORS.get("Female", PALETTE["cat_5"])]
    )
    
    bars = alt.Chart(df_long).mark_bar().encode(
        x=alt.X("deaths:Q", title="Deaths"),
        y=alt.Y("cause:N", title="", sort="-x"),
        color=alt.Color("sex:N", scale=color_scale, title="Sex"),
        tooltip=["cause", "sex", "deaths"],
    ).properties(
        width=width,
        height=height,
        title=alt.TitleFrame(
            text=title,
            subtitle=subtitle,
            anchor="start",
            offset=10,
        ),
    )
    
    return bars.configure_axis(
        labelFontSize=10,
        titleFontSize=11,
    )


def social_side_by_side(
    df_left: pd.DataFrame,
    df_right: pd.DataFrame,
    value_col: str = "deaths",
    label_col: str = "cause",
    title: str = "",
    subtitle: str = "",
    left_title: str = "Without",
    right_title: str = "With",
    preset: str = "twitter_landscape",
) -> alt.Chart:
    """Side-by-side grouped bars (e.g., "without abortion" vs "with abortion").
    
    Args:
        df_left: Data for left side
        df_right: Data for right side
        value_col: Column name for bar heights
        label_col: Column name for bar labels
        title: Main title
        subtitle: Subtitle
        left_title: Label for left group
        right_title: Label for right group
        preset: Platform preset
    
    Returns:
        Altair Chart object
    """
    w_px, h_px, _ = PRESETS[preset]
    width = w_px - 120
    height = h_px - 180
    
    # Add group identifier
    df_left["comparison"] = left_title
    df_right["comparison"] = right_title
    df_combined = pd.concat([df_left, df_right], ignore_index=True)
    
    # Sort by left side values for consistent ordering
    left_order = df_left.sort_values(value_col, ascending=True)[label_col].tolist()
    
    color_scale = alt.Scale(
        domain=[left_title, right_title],
        range=[PALETTE["cat_2"], PALETTE["accent"]]
    )
    
    chart = alt.Chart(df_combined).mark_bar().encode(
        x=alt.X(f"{value_col}:Q", title="Deaths"),
        y=alt.Y(f"{label_col}:N", title="", sort=left_order),
        color=alt.Color("comparison:N", scale=color_scale, title=""),
        xOffset="comparison",
        tooltip=[label_col, "comparison", value_col],
    ).properties(
        width=width,
        height=height,
        title=alt.TitleFrame(
            text=title,
            subtitle=subtitle,
            anchor="start",
            offset=10,
        ),
    )
    
    return chart.configure_axis(
        labelFontSize=10,
        titleFontSize=11,
    )


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

    # Position: right-aligned with chart content area, below footer rule
    x = img.width - text_w - 60
    y = img.height - text_h - 20

    draw.text((x, y), text, fill=(156, 163, 175, 180), font=font)
    return img
