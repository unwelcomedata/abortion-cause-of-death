#!/usr/bin/env python3
"""Pre-publish validation — re-check the chart data before anything goes public.

Run this BEFORE curating the release branch / flipping the repo public. It
re-derives what the published charts should show, straight from the DuckDB
source tables, and confirms:

  1. The national comparison chart facts hold (abortion total, the top-5
     causes and their male/female splits, and the ordering the chart shows).
  2. The gestation-stage breakdown inside the abortion bar is correct — every
     stage that the chart labels has BOTH a stage name and a percentage in its
     `pct_label` (this is the bug that previously left segments unlabeled), the
     shares reconcile to the abortion total, and they sum to ~100%.
  3. The published export CSV exists, is non-empty, and reconciles with the
     DuckDB source on the abortion headline total.

Exit code 0 = all checks passed, safe to publish. Non-zero = do NOT publish.

Usage:
    .venv/bin/python scripts/validate_charts.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import duckdb
import pandas as pd

# Resolve project root (the dir containing config.yaml) and import src helpers.
PROJECT = Path(__file__).resolve().parent
while not (PROJECT / "config.yaml").exists() and PROJECT != PROJECT.parent:
    PROJECT = PROJECT.parent
sys.path.insert(0, str(PROJECT))
from src.ingest import load_config  # noqa: E402

ABORTION_TOTAL = 1_124_000  # Guttmacher 2024 national total (what the chart labels)

failures: list[str] = []
checks: list[str] = []


def check(name: str, condition: bool, detail: str = "") -> None:
    """Record a pass/fail line."""
    if condition:
        checks.append(f"  PASS  {name}")
    else:
        failures.append(f"  FAIL  {name}" + (f" — {detail}" if detail else ""))


def approx(a: float, b: float, tol: float = 0.005) -> bool:
    """True if a is within tol (fractional) of b."""
    if b == 0:
        return a == 0
    return abs(a - b) / abs(b) <= tol


def main() -> int:
    cfg = load_config("config.yaml")
    db = str(PROJECT / cfg["settings"]["duckdb_file"])
    export_dir = PROJECT / cfg["paths"]["export"]
    con = duckdb.connect(db, read_only=True)

    # ── Chart 3 — national comparison (abortion vs top-5 causes, by sex) ──
    nat = con.execute(
        "SELECT cause, male_deaths, female_deaths, abortion_deaths, total_deaths "
        "FROM chart_national_stacked ORDER BY total_deaths DESC"
    ).df()

    check(
        "national: abortion total == 1,124,000",
        int(nat.loc[nat.cause == "Abortion", "abortion_deaths"].iloc[0]) == ABORTION_TOTAL,
        f"got {int(nat.loc[nat.cause == 'Abortion', 'abortion_deaths'].iloc[0]):,}",
    )
    check(
        "national: abortion is the largest bar (ranks first by total)",
        nat.iloc[0].cause == "Abortion",
        f"top row is {nat.iloc[0].cause!r}",
    )
    # The disease bars must reconcile: male + female == total (abortion row is
    # single-segment so it's excluded from this split check).
    disease = nat[nat.cause != "Abortion"].copy()
    bad_split = disease[
        (disease.male_deaths + disease.female_deaths - disease.total_deaths).abs() > 1
    ]
    check(
        "national: male + female == total for every disease bar",
        len(bad_split) == 0,
        f"{len(bad_split)} disease rows violate the male/female split",
    )
    check(
        "national: top disease cause is Heart disease",
        disease.iloc[0].cause == "Heart disease",
        f"got {disease.iloc[0].cause!r}",
    )
    # Heart disease male share is what the chart labels as "55%".
    hd = disease.iloc[0]
    hd_male_share = hd.male_deaths / hd.total_deaths
    check(
        "national: Heart disease male share rounds to 55%",
        round(hd_male_share * 100) == 55,
        f"got {hd_male_share * 100:.1f}%",
    )

    # ── Gestation breakdown inside the abortion bar (the label-bug guard) ──
    gest = con.execute(
        "SELECT segment, x_start, x_end, pct_label FROM chart_abortion_gestation "
        "ORDER BY x_start"
    ).df()

    # Cumulative positions must reconcile to the abortion total (the bar length).
    check(
        "gestation: segments span exactly the abortion total",
        approx(float(gest.x_end.max()), ABORTION_TOTAL),
        f"x_end max = {float(gest.x_end.max()):,.0f}, expected {ABORTION_TOTAL:,}",
    )
    # Shares (derived from widths) must sum to ~100%.
    widths = (gest.x_end - gest.x_start) / ABORTION_TOTAL
    check(
        "gestation: stage shares sum to ~100%",
        approx(float(widths.sum()), 1.0),
        f"sum = {float(widths.sum()) * 100:.1f}%",
    )
    # THE BUG GUARD: every stage the chart actually labels (pct_label non-empty)
    # must carry BOTH a stage name AND a percentage, i.e. the "name (pct%)" form
    # the renderer splits into a two-line label. A bare "79%" (no name) or a
    # name with no percent is the regression we are preventing.
    labeled = gest[gest.pct_label.fillna("").str.strip() != ""]
    check(
        "gestation: at least the 3 major stages are labeled",
        len(labeled) >= 3,
        f"only {len(labeled)} stages have a label",
    )
    malformed = []
    for _, row in labeled.iterrows():
        lbl = str(row.pct_label)
        has_name = "(" in lbl and lbl.split("(")[0].strip() != ""
        has_pct = "%" in lbl
        if not (has_name and has_pct):
            malformed.append(f"{row.segment!r}->{lbl!r}")
    check(
        "gestation: every labeled stage has BOTH a name and a percentage",
        len(malformed) == 0,
        "malformed labels: " + ", ".join(malformed),
    )
    # Spot-check the headline share the chart shows for the earliest stage.
    first = labeled.iloc[0]
    first_share = (first.x_end - first.x_start) / ABORTION_TOTAL
    check(
        "gestation: earliest stage share rounds to 79% and its label says so",
        round(first_share * 100) == 79 and "79%" in str(first.pct_label),
        f"share {first_share * 100:.1f}%, label {first.pct_label!r}",
    )

    # ── Published export CSV — exists, non-empty, reconciles on the total ──
    csv_path = export_dir / "abortion_cause_of_death_v1.csv"
    if not csv_path.exists():
        check("export: abortion_cause_of_death_v1.csv exists", False, "missing export file")
    else:
        df_csv = pd.read_csv(csv_path)
        check("export: CSV is non-empty", len(df_csv) > 0, "0 rows")
        # The "With abortion" scenario should carry an Abortion row whose deaths
        # equal the headline total used by the chart.
        ab = df_csv[(df_csv.get("cause") == "Abortion")]
        if len(ab) > 0:
            csv_total = float(ab["deaths"].max())
            check(
                "export: CSV abortion deaths == chart total (no drift)",
                approx(csv_total, ABORTION_TOTAL),
                f"CSV has {csv_total:,.0f}, chart uses {ABORTION_TOTAL:,}",
            )
        else:
            check(
                "export: CSV contains an Abortion row",
                False,
                "no row with cause == 'Abortion' in the export",
            )

    con.close()

    # ── Report ────────────────────────────────────────────────────────────
    print("Pre-publish chart-data validation — abortion-cause-of-death")
    print("=" * 60)
    for line in checks:
        print(line)
    for line in failures:
        print(line)
    print("=" * 60)
    if failures:
        print(f"RESULT: {len(failures)} FAILURE(S) — DO NOT PUBLISH.")
        return 1
    print(f"RESULT: all {len(checks)} checks passed — safe to publish.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
