#!/usr/bin/env python3
"""Check site assets and independently compare HTML results with LaTeX tables."""

from hashlib import sha256
from html.parser import HTMLParser
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


class SiteParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.references = []
        self.images = []
        self.tables = []
        self.row = None
        self.cell = None
        self.h1_count = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "h1":
            self.h1_count += 1
        for attribute in ("href", "src", "poster"):
            if attrs.get(attribute):
                self.references.append(attrs[attribute])
        if tag == "img" and attrs.get("src"):
            self.images.append(attrs)
        if tag == "table":
            self.tables.append([])
        elif tag == "tr":
            self.row = []
        elif tag in ("td", "th"):
            self.cell = []

    def handle_data(self, text):
        if self.cell is not None:
            self.cell.append(text)

    def handle_endtag(self, tag):
        if tag in ("td", "th") and self.cell is not None:
            self.row.append(" ".join("".join(self.cell).split()))
            self.cell = None
        elif tag == "tr" and self.row is not None:
            self.tables[-1].append(self.row)
            self.row = None


def main():
    parser = SiteParser()
    parser.feed((ROOT / "index.html").read_text())
    errors = []
    if parser.h1_count != 1:
        errors.append(f"Expected one h1, found {parser.h1_count}")
    duplicate_ids = {item for item in parser.ids if parser.ids.count(item) > 1}
    if duplicate_ids:
        errors.append(f"Duplicate IDs: {sorted(duplicate_ids)}")

    for reference in parser.references:
        url = urlsplit(reference)
        if url.scheme or url.netloc:
            continue
        if url.path:
            asset = ROOT / unquote(url.path)
            if not asset.is_file():
                errors.append(f"Missing asset: {reference}")
        elif url.fragment and url.fragment not in parser.ids:
            errors.append(f"Missing anchor: {reference}")

    # Pillow is optional; the core validator uses only the Python standard library.
    try:
        from PIL import Image
    except ImportError:
        print("INFO: Pillow unavailable; skipping pixel-dimension validation.")
    else:
        for attrs in parser.images:
            if not attrs.get("alt"):
                errors.append(f"Missing image description: {attrs['src']}")
            asset = ROOT / attrs["src"]
            if not asset.is_file():
                continue
            with Image.open(asset) as image:
                image.verify()
                declared = (int(attrs.get("width", 0)), int(attrs.get("height", 0)))
                if declared != image.size:
                    errors.append(f"Incorrect image dimensions for {asset.name}: {declared} vs {image.size}")

    pdf = ROOT / "assets/pilot-paper.pdf"
    if not pdf.is_file() or pdf.read_bytes()[:5] != b"%PDF-":
        errors.append("Missing or invalid paper PDF")
    original = ROOT / "local/inputs/paper/RA_L_PILOT_submission (3).pdf"
    if original.is_file() and pdf.is_file():
        if sha256(original.read_bytes()).digest() != sha256(pdf.read_bytes()).digest():
            errors.append("Download PDF differs from the supplied manuscript")

    source = ROOT / "local/paper-source/text/04-experiments.tex"
    number = r"\d+/\d+|\d+\.\d+"
    if source.is_file():
        latex = re.sub(r"(?m)(?<!\\)%.*$", "", source.read_text())
        expected_tables = []
        for block in re.findall(r"\\begin\{tabular\}(.+?)\\end\{tabular\}", latex, flags=re.S):
            rows = []
            for row in re.split(r"\\\\", block):
                if "&" not in row:
                    continue
                values = re.findall(number, " ".join(row.split("&")[1:]))
                if values:
                    rows.append(values)
            expected_tables.append(rows)
        actual_tables = []
        for table in parser.tables:
            actual_tables.append([
                values for row in table
                if (values := re.findall(number, " ".join(row[1:])))
            ])
        if actual_tables != expected_tables:
            for index, (actual, expected) in enumerate(zip(actual_tables, expected_tables), 1):
                if actual != expected:
                    errors.append(f"Table {index} differs from LaTeX: HTML {actual}; LaTeX {expected}")
            if len(actual_tables) != len(expected_tables):
                errors.append(f"Table count mismatch: HTML {len(actual_tables)}; LaTeX {len(expected_tables)}")
        else:
            print("PASS: All three result tables match the original LaTeX numerical entries.")
    else:
        print("INFO: LaTeX source unavailable; skipping independent result-table comparison.")

    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        raise SystemExit(1)
    print(f"PASS: {len(parser.references)} references, {len(parser.images)} images, anchors, and PDF checked.")


if __name__ == "__main__":
    main()
