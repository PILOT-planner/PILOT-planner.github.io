# Website figures

All figures come from the updated `PILOT_arxiv (3).pdf`, hosted unchanged at
`assets/pilot-paper.pdf`. The original input is also retained in the ignored
`local/inputs/paper/` directory. Earlier standalone PDFs in `local/inputs/figures/`
are historical references rather than inputs to the current export.

| PDF source | Page | Website asset | Format |
| --- | --- | --- | --- |
| Figure 1, motivation | 1 | `motivation.svg` | Vector SVG |
| Figure 2, method | 2 | `method.svg` | Vector SVG |
| Figure 2, method | 2 | `method.webp` | 1600px-wide sharing preview |
| Figure 3, annotated robot setup | 5 | `robot-setup.webp` | 2160px-wide WebP |
| Figure 4, real-world task success | 5 | `real-success.svg` | Vector SVG |
| Figure 5(a), real-world success vs. time | 5 | `real-success-time.webp` | Native-resolution WebP |
| Figure 5(b), real-world CEM cost | 5 | `real-planning-cost.webp` | Native-resolution WebP |
| Figure 6, four robot tasks | 6 | `real-subgoals.webp` | 3600px-wide WebP |
| Figure 7, Push-T success by length | 6 | `pusht-success.svg` | Vector SVG |
| Figure 8, Push-T execution | 6 | `pusht-subgoals.webp` | 1374px-wide WebP |
| Figure 9(a), Push-T success vs. time | 6 | `pusht-success-time.webp` | Native-resolution WebP |
| Figure 9(b), Push-T CEM cost | 6 | `pusht-planning-cost.webp` | Native-resolution WebP |
| Figure 10, LIBERO-10 execution | 7 | `libero-subgoals.webp` | 2754px-wide WebP |
| Figure 11, LIBERO-10 success | 7 | `libero-success.svg` | Vector SVG |

Run `python3 scripts/update_figures.py` to regenerate these assets. The optional
conversion tool requires PyMuPDF, Pillow, and Poppler's `pdftocairo`. It extracts
the original PDF figure objects, retaining vector annotations and excluding
page text and captions. The two diagrams preserve vector geometry and outlined
text; their embedded photographs remain self-contained. WebP assets are encoded
in RGB at quality 95 and compression method 6.

Page numbers and resource names in the script correspond to this manuscript.
Review the mapping for future revisions. The website itself has no build step
or runtime dependency on these tools.

The result charts reproduce Figures 4, 7, and 11, and the expandable HTML tables
retain their exact numerical values for reading and copying.
`scripts/check_site.py` can independently read the printed bar labels from
those figures and compare them with the HTML tables when PyMuPDF is available.
