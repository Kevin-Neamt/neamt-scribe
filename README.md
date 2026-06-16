# Neamt Scribe

A Neamt skill that converts YouTube videos into structured Markdown notes using
OpenAI Whisper (local transcription) and Claude (note generation).

## What it does

1. Downloads the audio track of any YouTube video via yt-dlp
2. Transcribes it locally with Whisper (no cloud transcription — runs on your machine)
3. Sends the transcript to Claude to generate structured Markdown notes with:
   - Executive summary
   - Key concepts
   - Main points
   - Important quotes
   - Data & statistics
   - Action items / takeaways
4. Saves the note to `~/.neamt/data/scribe/notes/` and shows it in the dashboard

## Installation

```bash
neamt install github:kevinneamt/neamt-scribe
```

Or from a local directory:

```bash
neamt install ./neamt-scribe
```

The install script will:
- Install `yt-dlp` and `openai-whisper` via pip
- Create `~/.neamt/data/scribe/notes/`

Then configure your Anthropic API key:

```bash
neamt config set anthropic_api_key sk-ant-...
```

## Requirements

- Python 3.11+
- ffmpeg (recommended for best audio quality — `brew install ffmpeg`)
- An Anthropic API key

## Permissions requested

| Permission | Why |
|---|---|
| `internet` | yt-dlp needs to download audio from YouTube |
| `filesystem:write` | Saves `.md` notes to `~/.neamt/data/scribe/notes/` |
| `anthropic_api` | Calls Claude to generate structured notes from the transcript |

## Usage

### Dashboard

Open the Neamt dashboard (`neamt start`) and click **Scribe** in the sidebar.

Paste a YouTube URL → click **Process** → wait (transcription takes ~1× real-time on CPU) → the note appears in the list and opens automatically.

### Programmatic (via bridge)

```python
from neamt.loader import discover_skills
from neamt.bridge import handle_call

skills = {s.manifest.id: s for s in discover_skills()}
scribe = skills["scribe"]

# Process a video
result = handle_call(scribe, "process_video", {"url": "https://youtube.com/watch?v=..."})
# → {"status": "ok", "result": {"status": "done", "title": "...", "filename": "...", "word_count": N}}

# List notes
result = handle_call(scribe, "list_notes", {})

# Read a note
result = handle_call(scribe, "get_note", {"filename": "2026-06-15_some-title.md"})

# Delete a note
result = handle_call(scribe, "delete_note", {"filename": "2026-06-15_some-title.md"})
```

## Notes storage

```
~/.neamt/data/scribe/
├── notes/
│   ├── 2026-06-15_video-title.md
│   └── ...
└── .tmp/        ← audio files during processing (auto-deleted)
```

## Uninstall

```bash
neamt uninstall scribe
```

You will be asked whether to delete your notes before the skill files are removed.

## Model

Notes are generated with `claude-haiku-4-5-20251001` by default (fast and cheap).
Whisper uses the `base` model by default (~150 MB, downloads on first use).
