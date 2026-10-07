# PILOT Project Website

An academic project website for PILOT, built from the supplied PDF and LaTeX materials, with a layout inspired by [DreamSteer](https://dream-steer.github.io/). The site uses plain HTML, CSS, and JavaScript. It requires no Node.js dependencies or build step and can be hosted on GitHub Pages or any static hosting service.

## Directory Structure

```text
PILOT_website/
├── index.html          # Website entry point
├── assets/             # Images, fonts, PDF, videos, styles, and scripts
├── scripts/            # Validation and export tools
├── README.md
├── .nojekyll           # Serve static files directly on GitHub Pages
├── .gitignore
├── local/              # Original materials and archived assets; not tracked
│   ├── inputs/         # Original paper, video, and logo inputs
│   ├── paper-source/   # Extracted LaTeX source
│   └── unused-assets/  # Retired images
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

- Paper title, anonymous authorship, PDF download, and key results.
- Motivation, abstract, method diagram, and control settings.
- Four real-world UR5e task demonstrations, video posters, and subgoal/execution comparisons.
- Real-world results, per-task success counts, 95% Wilson confidence intervals, and robot setup.
- Planning efficiency plots and tabbed Push-T and LIBERO-10 results.
- Copyable BibTeX and enlarged paper figures.
- Responsive layouts, keyboard navigation, and image/video dialogs. Basic reading and native video playback also work without JavaScript.

The desktop content is centered at 84% of the viewport width, capped at 1200px. The title is capped at 1120px; the abstract, citation, and key metrics are capped at 1000px. Tablet margins are 24px on each side, and mobile margins are 20px. Desktop body text ranges from 22px to 28px, captions from 21px to 26px, and tables use 21px text. Mobile body text and captions use 20px, with 19px table text.

The layout includes a continuous paper title, a soft gradient hero, dark resource buttons, three contribution cards below the first figure, and a single-column abstract. Task videos use four columns on desktop, two on tablets, and one on small screens. The real-world results pair a success chart with the robot setup and switch to a single column on smaller screens. Push-T and LIBERO-10 use tabs with keyboard support; both remain visible without JavaScript. Wide figures support horizontal scrolling on mobile, and figure dialogs link to full-resolution images. The header icon and favicon use the supplied PNG logo.

## Videos and Resource Links

Edit [assets/media.js](assets/media.js):

```javascript
window.PILOT_CONFIG = {
  codeUrl: "",  // Code repository URL; empty shows Coming soon
  arxivUrl: "", // arXiv URL; empty hides the button
  videos: {
    "cup": "assets/videos/cup.mp4",
    "pencil-case": "assets/videos/pencil-case.mp4",
    "bowl-box": "assets/videos/bowl-box.mp4",
    "bowl-bowl": "assets/videos/bowl-bowl.mp4"
  }
};
```

The four demonstrations in `assets/videos/` come from the task-specific `Ours.mp4` / `bowlBox_ours.mp4` files in the supplied archive. They preserve the full action sequence, encoded at 4x speed, 960px width, and 30fps using H.264 without audio. Faststart enables playback before the entire file downloads. Individual files are approximately 0.4-1.0MB, totaling about 2.6MB. Posters are actual video frames. See [assets/videos/README.md](assets/videos/README.md) for source mappings and encoding parameters.

Each video displays a `×4` badge in the upper-right corner. Select `Enlarge` to open an in-page player, capped at 960px, that retains the playback position and speed badge. Close it with the close button, Escape, or a click on the backdrop. Playback position returns to the inline player. With JavaScript enabled, playing one demonstration pauses the others, and a failed video falls back to its poster. Native video playback remains available without JavaScript.

When replacing a video, update the paths in both `assets/media.js` and `index.html`, along with the speed labels and description. Direct HTTPS video URLs are supported. Video hosting pages, such as YouTube watch pages, require a separate embedded player.

The manuscript currently uses anonymous authorship. Update `.authors` and `#bibtex` in `index.html` when public authorship and publication details are available.

## File Reference

- `index.html`: Website content and experimental results.
- `assets/style.css`: Typography, layout, and responsive styles.
- `assets/fonts/`: Local Noto Sans fonts and the OFL license.
- `assets/main.js`: Video integration, dialogs, tabs, and citation copying.
- `assets/media.js`: Video, code, and arXiv configuration.
- `assets/videos/`: Compressed MP4 demonstrations, posters, and provenance notes.
- `assets/figures/`: WebP figures converted from the paper materials.
- `assets/pilot-paper.pdf`: An exact copy of the supplied paper PDF.
- `local/paper-source/`: Extracted LaTeX source, retained locally.
- `scripts/check_site.py`: Asset, link, image, PDF, and result-table validation.
- `scripts/export_site.py`: Website-only release export.

## Validation and Release Export

```bash
python3 scripts/check_site.py
python3 scripts/export_site.py
```

When original materials are available locally, validation also compares the PDF and numerical tables against the manuscript. In a fresh clone, it checks website assets and internal links without requiring the original materials. Pillow is optional and enables image-dimension validation.

The export command regenerates `build/site/` and `build/pilot-website.zip`, containing only the website and its required assets. It clears the previous `build/site/` to remove obsolete resources. Upload the contents of `build/site/` to a static hosting service. All resource paths are relative and support deployment under a repository subpath.

## GitHub and GitHub Pages

The repository is [PILOT-planner/PILOT-planner](https://github.com/PILOT-planner/PILOT-planner), and the current website is on `main`. To clone it:

```bash
git clone https://github.com/PILOT-planner/PILOT-planner.git
cd PILOT-planner
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
