"""
Render video with karaoke subtitles using pycaps.

Usage:
    python render_with_pycaps.py \
        --input video.mp4 \
        --transcript corrected_transcript.json \
        --style style.css \
        --output output.mp4 \
        --words-per-segment 5

Dependencies:
    pip install "pycaps[all] @ git+https://github.com/francozanardi/pycaps.git"
    playwright install chromium
"""

import argparse
import os
import sys


def render(input_video, transcript, style_css, output, words_per_segment):
    from pycaps.template import TemplateLoader
    from pycaps.transcriber.splitter.limit_by_words_splitter import LimitByWordsSplitter
    from pycaps.transcriber import TranscriptFormat

    builder = (
        TemplateLoader("minimalist")
        .with_input_video(input_video)
        .load(False)
    )
    builder.with_output_video(output)
    builder.add_css(style_css)
    builder.with_transcription_file(transcript, format=TranscriptFormat.WHISPER_JSON)
    builder.add_segment_splitter(LimitByWordsSplitter(limit=words_per_segment))

    pipeline = builder.build()
    pipeline.run()

    size_mb = os.path.getsize(output) / (1024 * 1024)
    print(f"Done: {output} ({size_mb:.1f} MB)")


def main():
    parser = argparse.ArgumentParser(description="Render video with karaoke captions")
    parser.add_argument("--input", required=True, help="Input video path")
    parser.add_argument("--transcript", required=True,
                        help="Corrected whisper transcript JSON")
    parser.add_argument("--style", required=True, help="CSS style file path")
    parser.add_argument("--output", default="output_subtitled.mp4",
                        help="Output video path")
    parser.add_argument("--words-per-segment", type=int, default=5,
                        help="Max words per subtitle line (default: 5)")
    args = parser.parse_args()

    for fp in [args.input, args.transcript, args.style]:
        if not os.path.exists(fp):
            print(f"ERROR: File not found: {fp}", file=sys.stderr)
            sys.exit(1)

    if os.path.exists(args.output):
        print(f"ERROR: Output already exists: {args.output}", file=sys.stderr)
        print("  Delete it or use --output with a different path.", file=sys.stderr)
        sys.exit(1)

    print(f"Input:    {args.input}")
    print(f"Style:    {args.style}")
    print(f"Words/seg: {args.words_per_segment}")
    print(f"Output:   {args.output}")
    print()

    render(args.input, args.transcript, args.style, args.output, args.words_per_segment)


if __name__ == "__main__":
    main()
