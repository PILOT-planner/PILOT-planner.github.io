#!/usr/bin/env python3
"""Convert locally supplied figure PDFs into website assets using Poppler."""

from pathlib import Path
import subprocess
import tempfile
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "local/inputs/figures"
OUTPUT = ROOT / "assets/figures"


def main():
    sources = [
        "concept_v8.pdf", "method_v6.pdf",
        "real_subgoal_vs_exec_4tasks.pdf", "robot_setup_v2.pdf",
    ]
    for name in sources:
        if not (SOURCE / name).is_file():
            raise SystemExit(f"Missing figure input: {SOURCE / name}")
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for original, name in [
        ("concept_v8.pdf", "motivation.svg"),
        ("method_v6.pdf", "method.svg"),
    ]:
        subprocess.run([
            "pdftocairo", "-svg", str(SOURCE / original), str(OUTPUT / name)
        ], check=True)
        print(f"Converted {original} to {name}")
    with tempfile.TemporaryDirectory(prefix="pilot-figures-") as folder:
        for original, name, width in [
            ("method_v6.pdf", "method.webp", 1600),
            ("real_subgoal_vs_exec_4tasks.pdf", "real-subgoals.webp", 3600),
            ("robot_setup_v2.pdf", "robot-setup.webp", 2160),
        ]:
            prefix = Path(folder) / Path(name).stem
            subprocess.run([
                "pdftoppm", "-png", "-singlefile", "-scale-to-x", str(width),
                "-scale-to-y", "-1", str(SOURCE / original), str(prefix),
            ], check=True)
            with Image.open(prefix.with_suffix(".png")) as image:
                image.convert("RGB").save(
                    OUTPUT / name, "WEBP", quality=95, method=6
                )
                print(f"Converted {original} to {name}: {image.width}x{image.height}")


if __name__ == "__main__":
    main()
