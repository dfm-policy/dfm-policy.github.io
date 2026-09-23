# Updating dfm-policy.github.io

1. Copy `index.html` and the `static/dfmp/` folder into the repo root (replaces the old index.html;
   your existing `stacking/`, `placing/`, `favicon.ico` and `static/css|js` stay as they are).
2. Recommended: add H.264 copies of the four continuous runs next to the .mov files. The page tries
   `.mp4` first and falls back to `.mov`; HEVC .mov files do not play in Firefox and some Chrome setups.

       for f in stacking/cup_stacking1 stacking/cup_stacking2 placing/cup_placing1 placing/cup_placing2; do
         ffmpeg -i $f.mov -an -c:v libx264 -crf 23 -preset slow -pix_fmt yuv420p -movflags +faststart $f.mp4
       done

3. Commit and push. Edit `build_page.py` and run it to regenerate index.html.

Page order: title + supplementary video, abstract, real-robot continuous runs, FM vs DP vs DFMP
(synced, 3x), recovery, Push-T multimodality animations, simulation rollouts (2x).

static/dfmp/ (about 27 MB):
- videos/overview.mp4        the submitted supplementary video
- videos/compare/*.mp4       best FM / DP / DFMP policy per real task (3x, audio removed)
- videos/recovery/*.mp4      failed grasp followed by a successful retry (already 5x)
- videos/multimodal/*.mp4    Push-T rollout animations, two initial states
- videos/sim/*.mp4           8 simulation rollouts (2x)
- posters/                   first-frame images shown before each video loads
