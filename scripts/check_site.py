#!/usr/bin/env python3
"""Check website assets, text, and results against the current manuscript PDF."""

from hashlib import sha256
from html.parser import HTMLParser
from math import sqrt
from pathlib import Path
import re
import unicodedata
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree

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
        self.title_text = []
        self.h1_text = []
        self.bibtex_text = []
        self.abstract_text = []
        self.og_title = ""
        self.in_title = False
        self.in_h1 = False
        self.in_bibtex = False
        self.abstract_depth = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "h1":
            self.h1_count += 1
            self.in_h1 = True
        if tag == "title":
            self.in_title = True
        if tag == "meta" and attrs.get("property") == "og:title":
            self.og_title = attrs.get("content", "")
        if tag == "code" and attrs.get("id") == "bibtex":
            self.in_bibtex = True
        if tag == "div":
            if self.abstract_depth:
                self.abstract_depth += 1
            elif "abstract-content" in attrs.get("class", "").split():
                self.abstract_depth = 1
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
        if self.in_title:
            self.title_text.append(text)
        if self.in_h1:
            self.h1_text.append(text)
        if self.in_bibtex:
            self.bibtex_text.append(text)
        if self.abstract_depth:
            self.abstract_text.append(text)

    def handle_endtag(self, tag):
        if tag == "h1":
            self.in_h1 = False
        if tag == "title":
            self.in_title = False
        if tag == "code":
            self.in_bibtex = False
        if tag == "div" and self.abstract_depth:
            self.abstract_depth -= 1
        if tag in ("td", "th") and self.cell is not None:
            self.row.append(" ".join("".join(self.cell).split()))
            self.cell = None
        elif tag == "tr" and self.row is not None:
            self.tables[-1].append(self.row)
            self.row = None


def check_manuscript(parser, path, errors):
    try:
        import pymupdf as pdf
    except ImportError:
        print("INFO: PyMuPDF unavailable; skipping PDF text and result comparison.")
        return
    from update_figures import extract_form

    def normalize(text):
        return re.sub(r"[-\s]+", "", unicodedata.normalize("NFKC", text))

    with pdf.open(path) as paper:
        title = paper[0].get_text(clip=pdf.Rect(54, 70, 558, 120))
        citation = re.search(r"title\s*=\s*\{([^}]+)\}", "".join(parser.bibtex_text))
        titles = {
            "page title": "".join(parser.title_text),
            "hero title": "".join(parser.h1_text),
            "Open Graph title": parser.og_title,
            "BibTeX title": citation.group(1) if citation else "",
        }
        for label, text in titles.items():
            if normalize(text) != normalize(title):
                errors.append(f"The {label} differs from the current manuscript")
        abstract = next(
            block[4] for block in paper[0].get_text("blocks") if block[4].startswith("Abstract")
        )
        abstract = re.sub(r"^Abstract[—–-]?\s*", "", abstract).split("Videos are available")[0]
        if normalize("".join(parser.abstract_text)) != normalize(abstract):
            errors.append("Abstract differs from the current manuscript")

        # Read the printed bar labels from the PDF, independently of the HTML.
        specifications = [(5, "Im4", 4, 5), (6, "Im8", 9, 3), (7, "Im13", 6, 1)]
        if len(parser.tables) != len(specifications):
            errors.append(f"Expected three result tables, found {len(parser.tables)}")
            return
        for index, (page, resource, methods, conditions) in enumerate(specifications):
            with extract_form(paper, page, resource, pdf) as figure:
                labels = [
                    word
                    for word in figure[0].get_text("words")
                    if re.fullmatch(r"\d+\.\d", word[4])
                ]
            axis = 1 if conditions == 1 else 0
            labels.sort(key=lambda word: (word[axis] + word[axis + 2]) / 2)
            if len(labels) != methods * conditions:
                errors.append(f"Unexpected number of printed values in PDF figure {resource}")
                continue
            expected = [
                [labels[column * methods + row][4] for column in range(conditions)]
                for row in range(methods)
            ]
            actual = []
            for row in parser.tables[index][1:]:
                rates = []
                for cell in row[1 : conditions + 1]:
                    if "/" in cell:
                        successes, trials = map(int, cell.split("/"))
                        rates.append(f"{100 * successes / trials:.1f}")
                    else:
                        rates.append(cell.rstrip("%"))
                actual.append(rates)
            if actual != expected:
                errors.append(
                    f"Table {index + 1} differs from current PDF: HTML {actual}; PDF {expected}"
                )

        # Real-world intervals pool 80 trials and use the Wilson score formula.
        for row in parser.tables[0][1:]:
            counts = [tuple(map(int, cell.split("/"))) for cell in row[1:5]]
            successes = sum(count[0] for count in counts)
            trials = sum(count[1] for count in counts)
            rate, z = successes / trials, 1.96
            center = (rate + z * z / (2 * trials)) / (1 + z * z / trials)
            radius = (
                z
                * sqrt(rate * (1 - rate) / trials + z * z / (4 * trials * trials))
                / (1 + z * z / trials)
            )
            interval = f"[{100 * max(0, center - radius):.1f}, {100 * min(1, center + radius):.1f}]"
            if row[-1] != interval:
                errors.append(f"Incorrect Wilson interval for {row[0]}: {row[-1]} vs {interval}")
    print(
        "INFO: Compared titles, abstract, and three result tables with the current PDF; checked Wilson intervals."
    )


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
        Image = None
        print("INFO: Pillow unavailable; skipping pixel-dimension validation.")
    for attrs in parser.images:
        if not attrs.get("alt"):
            errors.append(f"Missing image description: {attrs['src']}")
        asset = ROOT / unquote(urlsplit(attrs["src"]).path)
        if not asset.is_file():
            continue
        declared = (int(attrs.get("width", 0)), int(attrs.get("height", 0)))
        if asset.suffix.lower() == ".svg":
            svg = ElementTree.parse(asset).getroot()
            if svg.tag != "{http://www.w3.org/2000/svg}svg":
                errors.append(f"Invalid SVG root: {asset.name}")
                continue
            view_box = [float(value) for value in svg.attrib["viewBox"].split()]
            if len(view_box) != 4 or declared != tuple(view_box[2:]):
                errors.append(
                    f"Incorrect SVG dimensions for {asset.name}: {declared} vs {view_box}"
                )
        elif Image is not None:
            with Image.open(asset) as image:
                image.verify()
                if declared != image.size:
                    errors.append(
                        f"Incorrect image dimensions for {asset.name}: {declared} vs {image.size}"
                    )

    pdf = ROOT / "assets/pilot-paper.pdf"
    if not pdf.is_file() or pdf.read_bytes()[:5] != b"%PDF-":
        errors.append("Missing or invalid paper PDF")
    original = ROOT / "local/inputs/paper/PILOT_arxiv (3).pdf"
    if original.is_file() and pdf.is_file():
        if sha256(original.read_bytes()).digest() != sha256(pdf.read_bytes()).digest():
            errors.append("Download PDF differs from the supplied manuscript")

    if pdf.is_file():
        check_manuscript(parser, pdf, errors)

    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        raise SystemExit(1)
    print(
        f"PASS: {len(parser.references)} references, {len(parser.images)} images, anchors, and PDF checked."
    )


if __name__ == "__main__":
    main()
