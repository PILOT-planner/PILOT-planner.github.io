# Real-world PILOT demonstrations

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

All four clips retain the full sequence, play at **4× source speed**, have no audio,
and use 960px width with the original aspect ratio. Output: H.264, yuv420p, 30fps,
CRF 26, slow preset, faststart. The page explicitly states the playback speed, and both the inline player and
the enlarged in-page player show a `×4` badge in the upper-right corner.

To reproduce a video from its extracted original:

```bash
ffmpeg -i original.mp4 -map 0:v:0 -an \
  -vf 'setpts=(PTS-STARTPTS)/4,scale=960:-2,fps=30' \
  -c:v libx264 -preset slow -crf 26 -pix_fmt yuv420p \
  -threads 2 -movflags +faststart output.mp4
```

Each `*-poster.webp` is the frame at 2 seconds in the compressed video
(8 seconds in the source), encoded as WebP at quality 85.
