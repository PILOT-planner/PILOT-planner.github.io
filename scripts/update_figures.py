#!/usr/bin/env python3
"""Extract website figures from the updated manuscript without page captions."""

import argparse
from io import BytesIO
from math import ceil
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]

# Page numbers and PDF resource names refer to PILOT_arxiv (3).pdf.
FORM_FIGURES = [
    (1, "Im1", "motivation.svg", None),
    (2, "Im2", "method.svg", None),
    (2, "Im2", "method.webp", 1600),
    (5, "Im3", "robot-setup.webp", 2160),
    (5, "Im4", "real-success.svg", None),
    (6, "Im7", "real-subgoals.webp", 3600),
    (6, "Im8", "pusht-success.svg", None),
    (6, "Im9", "pusht-subgoals.webp", 1374),
    (7, "Im12", "libero-subgoals.webp", 2754),
    (7, "Im13", "libero-success.svg", None),
]
IMAGE_FIGURES = [
    (5, "Im5", "real-success-time.webp"),
    (5, "Im6", "real-planning-cost.webp"),
    (6, "Im10", "pusht-success-time.webp"),
    (6, "Im11", "pusht-planning-cost.webp"),
]


def extract_form(paper, page_number, resource, pdf):
    """Place one original figure object on its own page at its native size."""
    with pdf.open() as copied:
        copied.insert_pdf(paper, from_page=page_number - 1, to_page=page_number - 1)
        forms = [item for item in copied[0].get_xobjects() if item[1] == resource and item[2] == 0]
        if len(forms) != 1:
            raise SystemExit(f"Expected figure {resource} on page {page_number}")
        xref, _, _, bounds = forms[0]
        x0, y0, x1, y1 = bounds
        page = copied.new_page(width=x1 - x0, height=y1 - y0)
        copied.xref_set_key(page.xref, "Resources", f"<</XObject<</Figure {xref} 0 R>>>>")
        stream = copied.get_new_xref()
        copied.update_object(stream, "<<>>")
        copied.update_stream(stream, f"q 1 0 0 1 {-x0:g} {-y0:g} cm /Figure Do Q".encode())
        copied.xref_set_key(page.xref, "Contents", f"{stream} 0 R")
        figure = pdf.open()
        figure.insert_pdf(copied, from_page=1, to_page=1)
    return figure


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--paper", type=Path, default=ROOT / "assets/pilot-paper.pdf")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "assets/figures")
    args = parser.parse_args()
    try:
        import pymupdf as pdf
        from PIL import Image
    except ImportError as error:
        raise SystemExit("Figure extraction requires PyMuPDF and Pillow.") from error
    if not args.paper.is_file():
        raise SystemExit(f"Missing manuscript: {args.paper}")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    with pdf.open(args.paper) as paper, tempfile.TemporaryDirectory(
        prefix="pilot-figures-"
    ) as folder:
        for page_number, resource, name, width in FORM_FIGURES:
            with extract_form(paper, page_number, resource, pdf) as figure:
                page = figure[0]
                if name.endswith(".svg"):
                    # Integer page dimensions keep HTML image sizing exact.
                    size = ceil(page.rect.width), ceil(page.rect.height)
                    with pdf.open() as canvas:
                        target = canvas.new_page(width=size[0], height=size[1])
                        target.show_pdf_page(target.rect, figure, 0)
                        source = Path(folder) / f"{Path(name).stem}.pdf"
                        canvas.save(source, garbage=4, deflate=True)
                    subprocess.run(
                        ["pdftocairo", "-svg", str(source), str(args.output_dir / name)], check=True
                    )
                    print(f"Extracted {name}: {size[0]}x{size[1]}")
                else:
                    scale = width / page.rect.width
                    pixels = page.get_pixmap(matrix=pdf.Matrix(scale, scale), alpha=False)
                    image = Image.frombytes("RGB", (pixels.width, pixels.height), pixels.samples)
                    if image.width != width:
                        image = image.resize(
                            (width, round(image.height * width / image.width)),
                            Image.Resampling.LANCZOS,
                        )
                    image.save(args.output_dir / name, "WEBP", quality=95, method=6)
                    print(f"Extracted {name}: {image.width}x{image.height}")
        for page_number, resource, name in IMAGE_FIGURES:
            matches = [
                item for item in paper[page_number - 1].get_images(full=True) if item[7] == resource
            ]
            if len(matches) != 1:
                raise SystemExit(f"Expected image {resource} on page {page_number}")
            original = paper.extract_image(matches[0][0])
            with Image.open(BytesIO(original["image"])) as image:
                image.convert("RGB").save(args.output_dir / name, "WEBP", quality=95, method=6)
                print(f"Extracted {name}: {image.width}x{image.height}")


if __name__ == "__main__":
    main()
