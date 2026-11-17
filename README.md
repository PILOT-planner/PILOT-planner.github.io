# PILOT Project Website

An academic project website for PILOT, built from the supplied PDF and LaTeX materials, with a layout inspired by [DreamSteer](https://dream-steer.github.io/). The site uses plain HTML, CSS, and JavaScript. It requires no Node.js dependencies or build step and can be hosted on GitHub Pages or any static hosting service.

The current content follows `PILOT_arxiv (3).pdf`: **PILOT: Guiding Long-Horizon World-Model Planning for Robot Manipulation with Imagined Subgoals and Policy Priors**. The arXiv identifier and links remain `2610.14335`.

## Directory Structure

```text
PILOT_website/
├── index.html          # Website entry point
├── assets/             # Images, fonts, PDF, videos, styles, and scripts
├── scripts/            # Asset conversion, validation, and export tools
├── README.md
├── .nojekyll           # Serve static files directly on GitHub Pages
├── .gitignore
├── local/              # Original materials and archived assets; not tracked
│   ├── inputs/         # Original source materials
│   │   ├── figures/    # Earlier standalone figure PDFs, kept for reference
│   │   ├── logo/       # Original logo image
│   │   ├── paper/      # Manuscript PDF and LaTeX archive
│   │   └── videos/     # Original demonstration archive and narrated project video
│   ├── paper-source/   # Original LaTeX source, kept for reference
│   └── unused-assets/  # Retired images and earlier task video versions
└── build/              # Generated files; not tracked
    ├── site/           # Website-only release directory
    ├── pilot-website.zip
    └── previews/       # Browser screenshots
```

`local/` and `build/` are excluded from Git. Original archives, extracted LaTeX, duplicate inputs, and screenshots remain local. Compressed demonstration videos and the paper PDF are included in `assets/` and committed to Git. A fresh clone can display the website without the original materials.

## Local Preview

Run from the repository root:

```bash
python3 -m http.server 8000 --bind 127.0.0.1
```

Open <http://localhost:8000>. You can also open `index.html` directly; a local HTTP server provides more complete clipboard support.

## Website Content

- Paper title, authors and affiliation, arXiv links, and key results.
- Full narrated project video with original audio and native playback controls.
- Motivation, abstract, method diagram, and control settings.
- Four real-world UR5e task demonstrations, video posters, and subgoal/execution comparisons.
- Paper-style SVG result charts, expandable numerical tables, 95% Wilson confidence intervals, and robot setup.
- Planning efficiency plots and tabbed Push-T and LIBERO-10 results.
- Copyable BibTeX and enlarged paper figures.
- Responsive layouts, keyboard navigation, and image/video dialogs. Basic reading and native video playback also work without JavaScript.

The desktop content is centered at 84% of the viewport width, capped at 1200px. The title uses a wider desktop container capped at 1640px, with two lines at typical desktop widths; the abstract and key metrics are capped at 1000px. The citation uses the main content width, and long BibTeX lines wrap without changing the copied text. Tablet margins are 24px on each side, and mobile margins are 20px. Desktop body text ranges from 22px to 28px, captions from 21px to 26px, and tables use 21px text. Mobile body text and captions use 20px, with 19px table text.

The layout includes a continuous paper title, a soft gradient hero, dark resource buttons, three contribution cards below the first figure, and a single-column abstract. The abstract initially shows its first paragraph, through the statement that no goal image is needed at test time, with a `Show more` / `Show less` button to expand or collapse the remaining text; the full abstract remains visible without JavaScript. Task videos use four columns on desktop, two on tablets, and one on small screens. The real-world results pair a success chart with the robot setup and switch to a single column on smaller screens. Push-T and LIBERO-10 use tabs with keyboard support; both remain visible without JavaScript. Wide figures support horizontal scrolling on mobile, and figure dialogs link to full-resolution images. The header icon and favicon use the supplied PNG logo.

The full presentation follows the hero, introduced by "An overview of PILOT, its method, and robot experiments." without a separate visible heading. Its responsive player is capped at 1000px, and the `Video` navigation link jumps to it. The presentation retains its original audio, uses native playback controls, and remains available without JavaScript. A poster and `preload="none"` avoid loading the full video before playback.

The efficiency highlight reports approximately 4× planning speedup at comparable success on the real-robot Bowl-Bowl task, following the second contribution in the current manuscript. This is distinct from the Push-T CEM iteration comparison, which remains in the detailed planning-efficiency discussion. Real-world, Push-T, and LIBERO-10 results use the PDF's vector bar charts as the primary display; their unchanged numerical tables are available under native `View detailed results` disclosures that also work without JavaScript.

## Videos and Resource Links

The presentation in `assets/videos/pilot-overview.mp4` is an exact copy of the supplied `PILOT_video_v52_arxiv_narrated_7min_nocaption.mp4`: approximately 7 minutes, 1876x1080 H.264 with AAC narration, about 47MB, already optimized for progressive playback. Its original input is retained under `local/inputs/videos/`. The player uses the source aspect ratio, and video/poster URLs use `?v=2` to refresh the previous version. Edit these paths and the dimensions in `index.html` when replacing it.

Edit [assets/media.js](assets/media.js):

```javascript
window.PILOT_CONFIG = {
  codeUrl: "",  // Code repository URL; empty shows Coming soon
  arxivUrl: "https://arxiv.org/abs/2610.14335", // Empty hides the arXiv button
  videos: {
    "cup": "assets/videos/cup.mp4?v=2",
    "pencil-case": "assets/videos/pencil-case.mp4?v=2",
    "bowl-box": "assets/videos/bowl-box.mp4?v=2",
    "bowl-bowl": "assets/videos/bowl-bowl.mp4?v=2"
  }
};
```

The four demonstrations in `assets/videos/` come from the task-specific `Ours.mp4` / `bowlBox_ours.mp4` files in the supplied archive. They preserve the full action sequence, encoded directly from those originals at 8x speed, 960px width, and 30fps using H.264 without audio. Faststart enables playback before the entire file downloads. Posters are actual video frames. See [assets/videos/README.md](assets/videos/README.md) for source mappings and encoding parameters.

Each task video displays a `×8` badge in the upper-right corner. Select `Enlarge` to open an in-page player, capped at 960px, that retains the playback position and speed badge. Close it with the close button, Escape, or a click on the backdrop. Playback position returns to the inline player. With JavaScript enabled, playing any video pauses the others, including the narrated presentation, and a failed task video falls back to its poster. Native video playback remains available without JavaScript.

When replacing a video, update the paths in both `assets/media.js` and `index.html`, along with the speed labels and description. Direct HTTPS video URLs are supported. Video hosting pages, such as YouTube watch pages, require a separate embedded player.

The authors are Yang Liu and Hanchen Cui (equal contribution), followed by Karthik Desingh, affiliated with the University of Minnesota Twin Cities. All three authors link to their personal homepages. The author list is also included in the page metadata and BibTeX. The citation identifies the 2026 arXiv preprint [arXiv:2610.14335](https://arxiv.org/abs/2610.14335), categorized as `cs.RO`.

## File Reference

- `index.html`: Website content and experimental results.
- `assets/style.css`: Typography, layout, and responsive styles.
- `assets/fonts/`: Local Noto Sans fonts and the OFL license.
- `assets/icons/NOTICE.txt`: Sources and licenses for the inline Academicons ArXiv and Font Awesome GitHub symbols. Resource buttons follow the DreamSteer style, with uniform `Code (Coming soon)` text.
- `assets/main.js`: Abstract expansion, video integration, dialogs, tabs, and citation copying.
- `assets/media.js`: Video, code, and arXiv configuration.
- `assets/videos/`: Full narrated presentation, compressed MP4 demonstrations, posters, and provenance notes.
- `assets/figures/`: SVG diagrams and result charts, WebP photographic figures, and a social sharing preview.
- `assets/pilot-paper.pdf`: An exact copy of the updated `PILOT_arxiv (3).pdf`.
- `local/inputs/paper/`: Original and updated manuscripts, retained locally.
- `local/paper-source/`: The earlier LaTeX source, retained for reference.
- `scripts/check_site.py`: Asset checks and independent title, abstract, result, and confidence-interval validation against the current PDF.
- `scripts/export_site.py`: Website-only release export.
- `scripts/update_figures.py`: Extract the current PDF's figure objects and plots into SVG and WebP assets.

## Updating Figures

The active figures are extracted directly from `assets/pilot-paper.pdf`, including annotations and labels. Earlier standalone figure PDFs remain in the ignored `local/inputs/figures/` directory for reference. The motivation and method diagrams and the three primary result charts use SVG to preserve vector text and lines. Robot and simulator sequences, the annotated setup, and planning-efficiency plots use high-quality WebP. A raster copy of the method diagram is used for social sharing previews. See [assets/figures/README.md](assets/figures/README.md) for the source mapping.

To regenerate the assets, install PyMuPDF, Pillow, and Poppler (`pdftocairo`), then run:

```bash
python3 scripts/update_figures.py
```

The script also accepts `--paper PATH` and `--output-dir PATH`. Its page/resource mapping refers to the current manuscript and should be reviewed when replacing the PDF. If source dimensions change, update the corresponding image dimensions in `index.html`. Bump the image cache version when replacing an asset at the same path.

## Validation and Release Export

```bash
python3 scripts/check_site.py
python3 scripts/export_site.py
```

The core validator checks website assets, anchors, and the hosted PDF without requiring original materials. Pillow optionally enables raster-image validation. With PyMuPDF installed, the validator also compares all title variants and the abstract with the current PDF, reads the numerical labels directly from its three result charts, and independently checks the real-world Wilson confidence intervals. The abstract's closing pointer to the project website is omitted on the website itself. When the updated input is present in `local/inputs/paper/`, its checksum must match the hosted PDF. Earlier LaTeX tables are no longer used as the numerical reference.

The export command regenerates `build/site/` and `build/pilot-website.zip`, containing only the website and its required assets. It clears the previous `build/site/` to remove obsolete resources. Upload the contents of `build/site/` to a static hosting service. All resource paths are relative and support deployment under a repository subpath.

## GitHub and GitHub Pages

The repository is [PILOT-planner/PILOT-planner.github.io](https://github.com/PILOT-planner/PILOT-planner.github.io), and the current website is on `main`. To clone it:

```bash
git clone https://github.com/PILOT-planner/PILOT-planner.github.io.git
cd PILOT-planner.github.io
```

After committing changes, push the current branch:

```bash
git push origin main
```

To upload the three saved version tags as well:

```bash
git push origin pilot-ds pilot-ori pilot-ds-plus
```

In **Settings → Pages**, select **Deploy from a branch**, choose **main** and **/(root)**, then save. The root `index.html`, `assets/`, and `.nojekyll` support direct publishing; generated files in `build/` are not needed. See the [GitHub Pages documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site).

All real-world, Push-T, and LIBERO results are taken from the supplied manuscript.
