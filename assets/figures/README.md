# Website figures

The updated PDFs are kept in the local, ignored `local/inputs/figures/` directory.
Only the converted website assets are committed and included in release exports.

| Local source | Website asset | Format |
| --- | --- | --- |
| `concept_v8.pdf` | `motivation.svg` | Vector SVG |
| `method_v6.pdf` | `method.svg` | Vector SVG |
| `method_v6.pdf` | `method.webp` | 1600px-wide social sharing preview |
| `real_subgoal_vs_exec_4tasks.pdf` | `real-subgoals.webp` | 3600px-wide WebP |
| `robot_setup_v2.pdf` | `robot-setup.webp` | 2160px-wide WebP |

SVG is exported with Poppler's `pdftocairo`. It preserves vector paths and
outlined text while embedding the original photographs. No external fonts or
image files are required.

WebP assets are rendered using `pdftoppm`, preserving the PDF page's aspect ratio,
then encoded in RGB with Pillow at quality 95 and compression method 6.

Run `python3 scripts/update_figures.py` to regenerate these assets. This optional
conversion step requires Poppler and Pillow. The website itself has no build
step or runtime dependency on these tools or the original PDFs.

The remaining simulation and efficiency figures come from the supplied LaTeX
materials and retain their existing WebP exports.
