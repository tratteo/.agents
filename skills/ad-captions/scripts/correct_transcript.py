"""
Apply text corrections to a whisper-format transcript.

Usage:
    python correct_transcript.py transcript.json --corrections corrections.json --output corrected.json

If --corrections is not provided, just reads the transcript and prints segment info
for manual review.

The corrections JSON format:
{
  "segments": [
    {
      "start": 0.0,
      "end": 5.14,
      "original_text": "raw whisper text",
      "corrected_text": "fixed text",
      "words": [{"word": "...", "start": 0.0, "end": 0.26, "probability": 0.9}]
    }
  ]
}

When corrected_text has a different word count than the original, word timestamps
are redistributed to match the corrected words (stretch/shrink mapping).
Words with None as the word text are removed (for merged tokens).
"""

import argparse
import copy
import json
import os
import sys


def redistribute_words(original_words, corrected_text):
    """Map corrected words onto original word timestamps.

    If counts match: replace word text 1:1.
    If counts differ: distribute corrected words proportionally across original timestamps.
    """
    corrected_words = corrected_text.split()
    n_orig = len(original_words)
    n_corr = len(corrected_words)

    if n_corr == 0:
        return original_words

    new_words = []
    for i, cw in enumerate(corrected_words):
        idx = int(i * n_orig / n_corr)
        idx = min(idx, n_orig - 1)
        new_words.append({
            "word": cw,
            "start": original_words[idx]["start"],
            "end": original_words[idx]["end"],
            "probability": original_words[idx].get("probability", 0.0),
        })
    return new_words


def apply_corrections(transcript, corrections):
    """Apply segment-level text corrections to a whisper transcript."""
    segments = transcript["segments"]

    # Build lookup by (start, end)
    corr_lookup = {}
    for cseg in corrections.get("segments", []):
        key = (round(cseg["start"], 2), round(cseg["end"], 2))
        corr_lookup[key] = cseg

    new_segments = []
    for seg in segments:
        seg = copy.deepcopy(seg)
        key = (round(seg["start"], 2), round(seg["end"], 2))

        if key in corr_lookup:
            cseg = corr_lookup[key]
            if "corrected_text" in cseg and cseg["corrected_text"]:
                seg["text"] = cseg["corrected_text"]
                # Redistribute words if word count changed
                if seg.get("words"):
                    seg["words"] = redistribute_words(seg["words"], cseg["corrected_text"])

        new_segments.append(seg)

    transcript["segments"] = new_segments
    return transcript


def validate_corrections(transcript, corrections):
    """Check that correction segments match source segments."""
    src_keys = {(round(s["start"], 2), round(s["end"], 2)) for s in transcript["segments"]}
    for cseg in corrections.get("segments", []):
        key = (round(cseg["start"], 2), round(cseg["end"], 2))
        if key not in src_keys:
            print(f"WARNING: Correction at {cseg['start']}-{cseg['end']} "
                  f"doesn't match any source segment")


def print_segments(transcript):
    """Print segment info for manual review."""
    for i, seg in enumerate(transcript["segments"]):
        text = seg["text"]
        words = seg.get("words", [])
        low_conf = [w["word"] for w in words if w.get("probability", 1.0) < 0.7]
        dur = seg["end"] - seg["start"]
        print(f"[{i}] {seg['start']:.2f}-{seg['end']:.2f} ({dur:.1f}s) | {len(words)}w")
        print(f"    \"{text}\"")
        if low_conf:
            print(f"    LOW CONFIDENCE: {', '.join(low_conf)}")
        print()


def main():
    parser = argparse.ArgumentParser(description="Correct whisper transcript text")
    parser.add_argument("transcript", help="Path to whisper transcript.json")
    parser.add_argument("--corrections", default=None,
                        help="Path to corrections JSON file")
    parser.add_argument("--output", default="corrected_transcript.json",
                        help="Output path for corrected transcript")
    parser.add_argument("--review", action="store_true",
                        help="Print segments for manual review")
    args = parser.parse_args()

    if not os.path.exists(args.transcript):
        print(f"ERROR: Transcript not found: {args.transcript}", file=sys.stderr)
        sys.exit(1)

    with open(args.transcript, "r", encoding="utf-8") as f:
        transcript = json.load(f)

    if args.review:
        print_segments(transcript)
        return

    if args.corrections:
        if not os.path.exists(args.corrections):
            print(f"ERROR: Corrections file not found: {args.corrections}", file=sys.stderr)
            sys.exit(1)
        with open(args.corrections, "r", encoding="utf-8") as f:
            corrections = json.load(f)
        validate_corrections(transcript, corrections)
        transcript = apply_corrections(transcript, corrections)
    else:
        print("No corrections provided. Use --corrections to apply fixes.")
        print("  Or use --review to inspect the transcript first.")
        sys.exit(0)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(transcript, f, indent=2, ensure_ascii=False)

    n_words = sum(len(s.get("words", [])) for s in transcript["segments"])
    print(f"Corrected: {len(transcript['segments'])} segments, {n_words} words")
    print(f"Output: {args.output}")


if __name__ == "__main__":
    main()
