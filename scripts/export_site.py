#!/usr/bin/env python3
"""Export the public website without the original manuscript source/archive."""

from pathlib import Path
import shutil
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]


def main():
    output = ROOT / "build/site"
    files = [ROOT / "index.html", ROOT / ".nojekyll"] + sorted(
        file for file in (ROOT / "assets").rglob("*")
        if file.is_file() and file.suffix != ".md"
    )
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)
    archive = ROOT / "build/pilot-website.zip"
    with ZipFile(archive, "w", ZIP_DEFLATED) as bundle:
        for file in files:
            relative = file.relative_to(ROOT)
            target = output / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(file, target)
            bundle.write(file, str(relative))
    print(f"Exported {len(files)} files to {output}")
    print(f"Created {archive} ({archive.stat().st_size / 1024 / 1024:.1f} MB)")


if __name__ == "__main__":
    main()
