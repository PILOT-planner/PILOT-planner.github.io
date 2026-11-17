# Website videos

## Narrated project video

Source: `local/inputs/videos/PILOT_video_v52_arxiv_narrated_7min_nocaption.mp4`.
Public copy: `pilot-overview.mp4`.

The approximately 6-minute, 56-second presentation uses 1876x1080 H.264 video and stereo AAC
audio. The supplied MP4 already places its metadata before the media data for
progressive playback, so the public copy is byte-identical to the source.
Original timing, narration, and the source's embedded subtitle track are preserved.
This is the supplied v52 no-caption presentation, with no website-added captions.
The original filename is ignored by Git; the archived input remains local.

`pilot-overview-poster.webp` is the frame at one second, retained at 1876x1080
and encoded as WebP at quality 90. The video and poster URLs use
`?v=2` to refresh the previous version. The player uses `preload="none"`, displays
native controls, and plays inline without autoplay. Starting this video pauses
the task demonstrations, and starting a task demonstration pauses the narration.

## Four real-world task demonstrations

Source archive: `local/inputs/videos/wm_planning_demo-20261001T064544Z-1-001.zip`.
The original archive is preserved locally and excluded from Git and the public website bundle.

| Task | Original member inside archive | Website video |
| --- | --- | --- |
| Cup | `wm_planning_demo/cup/Ours.mp4` | `cup.mp4` |
| Pencil Case | `wm_planning_demo/pencilCase/Ours.mp4` | `pencil-case.mp4` |
| Bowl-Box | `wm_planning_demo/bowlBox/bowlBox_ours.mp4` | `bowl-box.mp4` |
| Bowl-Bowl | `wm_planning_demo/bowlBowl/Ours.mp4` | `bowl-bowl.mp4` |

These are the full PILOT demonstrations. The out-of-distribution Bowl-Box variant,
policy-only videos, and videos without the policy prior are not used for these cards.

All four clips retain the full sequence, play at **8× source speed**, have no audio,
and use 960px width with the original aspect ratio. Output: H.264, yuv420p, 30fps,
CRF 26, slow preset, faststart. The page explicitly states the playback speed, and both the inline player and
the enlarged in-page player show a `×8` badge in the upper-right corner.

The 8× files are encoded directly from the original archive. Their previous 4×
versions are retained locally in `local/unused-assets/task-videos-4x/`.
The playback rate remains 1 in the browser because the speedup is encoded in
the files. Both `index.html` and `assets/media.js` use `?v=2` to refresh cached
task videos.

To reproduce a video from its extracted original:

```bash
ffmpeg -i original.mp4 -map 0:v:0 -an \
  -vf 'setpts=(PTS-STARTPTS)/8,scale=960:-2,fps=30' \
  -c:v libx264 -preset slow -crf 26 -pix_fmt yuv420p \
  -threads 2 -movflags +faststart output.mp4
```

Each task's `*-poster.webp` shows the original recording at approximately
8 seconds, corresponding to about 1 second at 8× speed. These existing posters
were generated from the previous 4× clips at 2 seconds and encoded as WebP at
quality 85.
