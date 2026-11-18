# PlayWithJey — free Android-friendly video builder

This is a **manual-trigger prototype**, not a fully autonomous channel. It makes original text-slide videos, basic English synthetic narration, thumbnail images and metadata using GitHub Actions. It does NOT upload to YouTube, search for news, or create real GTA 6 gameplay. The `long` sample is a short explainer prototype, not a 6–10 minute video.

## Android setup
1. Create a free GitHub account and a **private** repository named `playwithjey`.
2. In Chrome enable **Desktop site** if GitHub controls are hard to find.
3. Upload `generate.py`, `topics.json`, and `.github/workflows/build.yml` with their directory paths intact. Add `assets/` only if desired. GitHub's web uploader may not preserve empty folders.
4. Open repository **Actions**, select **Build PlayWithJey Video**, choose **Run workflow**, select `short`, then run.
5. Open the completed workflow run and download the artifact ZIP. Inside are MP4, PNG thumbnail and metadata text.
6. Review factual accuracy, audio and visuals before publishing manually through YouTube Studio.

## Editing the content
Edit `topics.json` in GitHub. Each segment has a short `heading` and a spoken `narration`. Keep facts verified against official sources. This sample intentionally avoids uncertain release claims.

## Limitations
- GitHub Actions free quotas and account restrictions apply; no guaranteed unlimited usage.
- `espeak-ng` is a robotic free English voice, not a premium AI voice.
- Text slides are not real GTA gameplay and may be insufficient for audience retention or monetization.
- Automatic YouTube publishing needs separate Google OAuth consent and an upload integration; it is intentionally not enabled here.
- For copyright safety, use original commentary and footage you have rights to use. Do not impersonate Rockstar or present rumors as facts.
