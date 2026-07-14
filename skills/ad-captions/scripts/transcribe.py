"""
Transcribe video to word-level JSON using faster-whisper.
Outputs whisper-format JSON with segments[].words[] (word, start, end, probability).

Usage:
    python transcribe.py <video_path> [--model medium] [--language auto] [--output transcript.json]

Dependencies: pip install faster-whisper
"""

import argparse
import json
import os
import sys
import tempfile
import subprocess


def extract_audio(video_path: str) -> str:
    """Extract 16kHz mono WAV audio from video for whisper processing."""
    tmp = os.path.join(tempfile.gettempdir(), f"_vae_audio_{os.getpid()}.wav")
    cmd = [
        "ffmpeg", "-y", "-i", video_path,
        "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1",
        "-loglevel", "error", tmp
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Audio extraction failed: {result.stderr.strip()}")
    return tmp


def transcribe(
    video_path: str,
    model_size: str = "medium",
    language: str = "auto",
    device: str = "auto",
    compute_type: str = "auto",
) -> dict:
    from faster_whisper import WhisperModel

    audio_path = extract_audio(video_path)
    lang_code = language if language != "auto" else None

    device_str = device if device != "auto" else ("cuda" if _cuda_available() else "cpu")
    compute_str = compute_type if compute_type != "auto" else (
        "float16" if device_str == "cuda" else "int8"
    )

    model = WhisperModel(model_size, device=device_str, compute_type=compute_str)

    segments_raw, info = model.transcribe(
        audio_path,
        language=lang_code,
        word_timestamps=True,
        beam_size=5,
        vad_filter=True,
        vad_parameters=dict(min_silence_duration_ms=400, threshold=0.4),
    )

    segments = []
    for seg in segments_raw:
        words = []
        if seg.words:
            for w in seg.words:
                words.append({
                    "word": w.word.strip(),
                    "start": round(w.start, 3),
                    "end": round(w.end, 3),
                    "probability": round(w.probability, 3),
                })
        segments.append({
            "start": round(seg.start, 3),
            "end": round(seg.end, 3),
            "text": seg.text.strip(),
            "words": words,
        })

    try:
        os.unlink(audio_path)
    except OSError:
        pass

    return {
        "language": info.language,
        "duration": round(segments[-1]["end"] if segments else 0.0, 1),
        "language_probability": round(info.language_probability, 3),
        "segments": segments,
    }


def _cuda_available() -> bool:
    try:
        import torch
        return torch.cuda.is_available()
    except ImportError:
        return False


def main():
    parser = argparse.ArgumentParser(description="Transcribe video to word-level JSON")
    parser.add_argument("video", help="Path to input video file")
    parser.add_argument("--model", default="medium",
                        choices=["tiny", "base", "small", "medium", "large-v3"])
    parser.add_argument("--language", default="auto", help="Language code or 'auto'")
    parser.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    parser.add_argument("--compute-type", default="auto",
                        choices=["auto", "float16", "int8", "int8_float16"])
    parser.add_argument("--output", default="transcript.json")
    args = parser.parse_args()

    if not os.path.exists(args.video):
        print(f"ERROR: Video file not found: {args.video}", file=sys.stderr)
        sys.exit(1)

    print(f"Transcribing: {args.video}")
    print(f"Model: {args.model} | Language: {args.language}")

    result = transcribe(args.video, args.model, args.language, args.device, args.compute_type)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    word_count = sum(len(s["words"]) for s in result["segments"])
    print(f"Done. Language: {result['language']} | Duration: {result['duration']}s | "
          f"Segments: {len(result['segments'])} | Words: {word_count}")
    print(f"Output: {args.output}")


if __name__ == "__main__":
    main()
