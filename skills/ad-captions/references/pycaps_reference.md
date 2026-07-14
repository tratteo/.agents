# pycaps Reference

## Installation

```bash
pip install "pycaps[all] @ git+https://github.com/francozanardi/pycaps.git"
playwright install chromium
```

## Templates

pycaps ships with these built-in templates:

| Template | Best for |
|----------|----------|
| `minimalist` | Karaoke word highlighting with clean layout |
| `default` | Bold text with custom font (requires `black.ttf` in resources) |
| `vibrant` | Colorful, energetic subtitles |
| `classic` | Traditional subtitle look |
| `word-focus` | Heavy emphasis on highlighted word |

For karaoke subtitles, `minimalist` or `default` work best.

## Key API Classes

### CapsPipelineBuilder

```python
from pycaps import CapsPipelineBuilder

builder = CapsPipelineBuilder()
builder.with_input_video(path)
builder.with_output_video(path)
builder.with_transcription_file(path, format=TranscriptFormat.WHISPER_JSON)
builder.add_css(path)           # Add CSS file
builder.add_css_content(str)    # Add raw CSS string
builder.add_segment_splitter(splitter)
pipeline = builder.build()
pipeline.run()
```

### TranscriptFormat

```python
from pycaps.transcriber import TranscriptFormat

TranscriptFormat.AUTO          # Auto-detect
TranscriptFormat.WHISPER_JSON  # Standard whisper JSON
TranscriptFormat.PYCAPS_JSON   # pycaps internal format
TranscriptFormat.SRT           # SubRip subtitle
TranscriptFormat.VTT           # WebVTT
```

### Segment Splitters

```python
from pycaps.transcriber.splitter.limit_by_words_splitter import LimitByWordsSplitter
from pycaps.transcriber.splitter.limit_by_chars_splitter import LimitByCharsSplitter

# Split by word count (simplest)
LimitByWordsSplitter(limit=5)

# Split by character count (more control)
LimitByCharsSplitter(max_limit=42, min_limit=15, avoid_finishing_segment_with_word_shorter_than=3)
```

### TemplateLoader

```python
from pycaps.template import TemplateLoader

builder = TemplateLoader("minimalist").with_input_video("input.mp4").load(False)
# load(False) = don't show transcription preview GUI
# load(True)  = show editable transcription preview
```

## CSS Classes Used by pycaps

| Class | Applies to |
|-------|-----------|
| `#video` | The whole video container |
| `.captions` | The captions container (use for alignment) |
| `.caption` | One subtitle segment/phrase |
| `.word` | Every individual word |
| `.word-being-narrated` | The word currently being spoken |
| `.word.before-highlighted` | Words already spoken |
| `.word.after-highlighted` | Words yet to be spoken |

## Font Sizing

pycaps renders captions at a fixed resolution (video width x height), then overlays them.
The base `font-size: 20px` in CSS is scaled by the layout engine based on video dimensions
and word lengths. For 1080x1920 vertical videos, the rendered text is approximately 52-60px.

**Do not increase the base font-size** — if text appears too small, check:
- The video dimensions are correct (pycaps auto-detects them)
- The font-family is a valid system font (Arial, Helvetica are safe choices)

## Troubleshooting

### Playwright fails to launch browser
```bash
playwright install chromium --force
```

### Font doesn't render
Use system fonts (Arial, Helvetica) instead of web fonts. pycaps renders in headless Chromium which may not have web fonts available.

### CSS animations don't work
pycaps only supports animations with `--animate` flag (slower, real-time rendering):
```bash
pycaps render --input video.mp4 --template minimalist --animate
```

### "Output video path already exists" error
pycaps refuses to overwrite existing files. Delete the output file or use a different name.

### Segment splitter not working
Make sure it's added BEFORE `builder.build()` and that the transcript format is `whisper_json` (which includes word-level timestamps).

### Subtitles seem clipped
The `LimitByWordsSplitter` may leave trailing words. Try a slightly larger limit, or use `LimitByCharsSplitter` for more control.
