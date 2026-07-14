# Common Whisper Transcription Errors

## Italian (it)

### Technical Terms & Acronyms

| Whisper output | Correct term | Reason |
|---------------|-------------|--------|
| "c'è GPT" | ChatGPT | Whisper splits "Chat" into Italian "c'è" |
| "JEO" | GEO | G/J confusion (Generative Engine Optimization) |
| "AIO" | AEO | I/E confusion (Answer Engine Optimization) |
| "Cloud" | Claude | Homophone in Italian context |
| "l'Alzheimer" | l'Answer / l'AEO | Unfamiliar acronym mapped to known word |
| "adorevole" | autorevole | Phonetic similarity in fast speech |
| "aprici al GPT" | apri ChatGPT | Verb splitting + acronym mangling |

### General Italian Issues

| Pattern | Description |
|---------|-------------|
| Apostrophe splitting | "l'" and "'AEO" become separate tokens "l" and "'AEO" |
| English terms in Italian | "brand", "webinar", "framework" may get Italian-ized |
| Numbers | "1 luglio" vs "primo luglio" — both are acceptable |
| Accented vowels | "è" vs "e'" — Whisper handles accents well but check |
| Compound prepositions | "dalle AI" vs "dalle IA" — both are used in Italian |

### Review Checklist

When reviewing an Italian transcript, check:

1. **AI/tech terms**: ChatGPT, Gemini, Claude, AEO, GEO, SEO, AI Overview
2. **English loanwords**: brand, webinar, framework, competitor, click, overview
3. **Low-confidence words** (probability < 0.7): these are the most likely errors
4. **Segment boundaries**: sometimes Whisper splits a word across two segments
5. **Watermarks**: "Sottotitoli creati dalla comunita Amara.org" — remove these

## English (en)

### Common Issues

| Whisper output | Correct term | Reason |
|---------------|-------------|--------|
| "gen kit" | Genkit | Compound technical terms |
| "fire base" | Firebase | Brand names |
| "A I" | AI | Acronym spacing |
| "U R L" | URL | Spelled-out acronyms |

---

## General Whisper Quirks (all languages)

- **Silence handling**: Whisper may insert hallucinated text during long silences
- **VAD filtering**: Enabling VAD (`vad_filter=True`) reduces hallucination but may clip very short utterances
- **Segment boundaries**: Words at segment boundaries may have incorrect timing
- **Punctuation**: Whisper adds commas and periods aggressively — they may not match the speaker's actual pauses
- **Filler words**: "um", "uh", "like", "you know" are usually transcribed and should be removed from subtitles
- **Repeated words**: Whisper sometimes duplicates short words ("the the", "e e" in Italian)
