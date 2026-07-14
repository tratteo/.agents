---
name: ad-captions
description: >
  Add styled karaoke subtitles to videos for social media (TikTok, Reels, Shorts).
  Use this skill when the user wants to add captions, subtitles, or karaoke-style
  word highlighting to any video. Triggers on requests like "add subtitles to this
  video", "generate captions for my ad", "put karaoke subtitles on...", "I need
  captions with highlighted words", "burn subtitles into this video", or any task
  involving video subtitling, caption generation, or subtitle styling. Also use
  when the user mentions pycaps, styled captions, word-by-word highlighting, or
  wants to add text overlays synchronized to speech in a video.
---

# ad-captions

Adds styled karaoke subtitles to videos using pycaps. Handles transcription, correction, CSS styling, and rendering into a single pipeline.

## Workflow

```
Input Video → [1. Gather style] → [2. Transcribe] → [3. Correct] → [4. Render] → Subtitled Video
```

---

## Phase 0: Gather Style Preferences

Before doing anything, ask the user these questions. Use defaults if they skip.

| Parameter | Default | Description |
|-----------|---------|-------------|
| Highlight color | `#4F39F6` | Hex color for the currently-spoken word background |
| Font | `Arial` | Font family (system fonts recommended for reliability) |
| Font weight | `800` (Bold) | CSS font-weight |
| Text color | `#FFFFFF` (White) | Color of subtitle text |
| Words per segment | `5` | Max words per subtitle line (3-6 recommended for short-form) |
| Position | `bottom` | Where captions appear in the video |
| Transcript | auto | Path to existing transcript, or "auto" to transcribe |
| Language | `auto` | ISO language code or "auto" for detection |

### Color Presets

| Name | Hex | Use case |
|------|-----|----------|
| Blue | `#4F39F6` | Default, professional |
| Gold | `#FFD700` | Warm, premium |
| Green | `#22C55E` | Growth, positive |
| Pink | `#EC4899` | Bold, attention |
| White highlight | `#FFFFFF` | Minimal, clean |

---

## Phase 1: Transcription

If the user provides a transcript (`transcript.json` or `.srt`), skip to Phase 3 (transcription correction).

Otherwise, transcribe the video with faster-whisper for word-level timestamps:

```bash
pip install faster-whisper  # one-time
python scripts/transcribe.py <video_path> --model medium --language <lang> --output transcript.json
```

The script outputs a whisper-format JSON with segments containing `words[]` with `word`, `start`, `end` timestamps.

---

## Phase 2: Analyze and Fix Transcription Errors

Read the transcript carefully. Whisper makes predictable errors with:
- **Brand/tech terms**: "ChatGPT" → "c'è GPT", "Firebase" → "fire base"
- **Acronyms**: "GEO" → "JEO", "AEO" → "AIO"
- **Proper nouns**: Names, product names, domain terms
- **Homophones**: Italian "c'è" vs English "chat", "Cloud" vs "Claude"

Use the `correct_transcript.py` script to apply corrections:

```bash
python scripts/correct_transcript.py transcript.json [corrections.json] --output corrected_transcript.json
```

The corrections JSON format:

```json
{
  "language": "it",
  "segments": [
    {
      "start": 0.0,
      "end": 5.14,
      "original_text": "Oggi passa dalle AI come c'e' GPT, Gemini, Cloud e...",
      "corrected_text": "Oggi passa dalle AI come ChatGPT, Gemini, Claude, e...",
      "words": [ ... original word timestamps ... ]
    }
  ]
}
```

When segment text is corrected and word count changes, the script redistributes word timestamps automatically. Include only segments that need correction.

---

## Phase 3: Render with pycaps

### Installation (one-time)

```bash
pip install "pycaps[all] @ git+https://github.com/francozanardi/pycaps.git"
playwright install chromium
```

### Generate CSS File

Create a CSS file from the style preferences gathered in Phase 0. The key CSS classes pycaps uses are:
- `.word` — base styles for every word
- `.word-being-narrated` — the currently highlighted word

Use the bundled `assets/default_style.css` as a template and customize the colors, font, and weight.

**CRITICAL**: The base `font-size` in CSS should always be `20px`. pycaps' layout engine scales this automatically based on video dimensions. Do NOT change the base font-size — adjust the visual outcome by changing `font-family`, `font-weight`, and `text-shadow` instead.

### Render

Use the bundled `scripts/render_with_pycaps.py` script:

```bash
python scripts/render_with_pycaps.py \
  --input <video.mp4> \
  --transcript <corrected_transcript.json> \
  --style <style.css> \
  --output <output.mp4> \
  --words-per-segment 5
```

The script:
1. Loads the `minimalist` pycaps template (best for karaoke word highlighting)
2. Applies the custom CSS from `--style`
3. Sets `LimitByWordsSplitter` with `--words-per-segment`
4. Burns subtitles directly into the video (no overlay step needed)

---

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `scripts/transcribe.py` | Transcribe video → whisper JSON with word timestamps |
| `scripts/correct_transcript.py` | Apply text corrections to whisper transcript |
| `scripts/render_with_pycaps.py` | Full pycaps rendering pipeline |

All scripts support `--help` for detailed usage.

## Reference Files

- `references/pycaps_reference.md` — pycaps API, templates, CSS classes, and troubleshooting
- `references/transcription_errors.md` — Common Whisper transcription mistakes by language
- `assets/default_style.css` — CSS template with all style properties and comments

---

## Quality Checklist

Before presenting the final video:
- [ ] All technical terms and acronyms are correctly transcribed
- [ ] Highlight color matches user's preference
- [ ] Segments are 3-6 words each (readable on mobile)
- [ ] Text is clearly visible against video background (check with shadow/outline)
- [ ] Subtitles are synchronized with audio
- [ ] No watermark segments (Amara.org, etc.) in the output

---

## Error Recovery

| Issue | Fix |
|-------|-----|
| Transcription fails | Check FFmpeg in PATH. Try `--model tiny`. |
| pycaps render fails | Reinstall: `pip install --force "pycaps[all] @ git+..."` then `playwright install chromium` |
| Subtitles too long | Decrease `--words-per-segment` to 3-4 |
| Font not rendering | Use a system font like Arial, Helvetica, or sans-serif |
| CSS animations not working | pycaps only supports CSS3 animations. Ensure `@keyframes` syntax is correct. |
