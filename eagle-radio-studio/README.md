# Eagle Radio Studio

> **Project Eagle** | Audio Management Tool | v2.0

## Overview

Eagle Radio Studio is a web-based tool for managing menu music, custom radio playlists, and audio deployment for Project Eagle (GTA San Andreas mod).

## Features

- 🎵 **Playlist Management** — Add, remove, reorder tracks across radio stations
- 🔀 **Random Playback** — Shuffle mode with auto-next when track ends
- 🚀 **Direct Deploy** — Push audio files straight to `gameplay-lab`
- 🎛️ **Station Config** — Custom stations with metadata (name, genre, artwork)
- 📋 **Audit Log** — Track all changes with timestamps

## Directory Structure

```
eagle-radio-studio/
├── app.py              ← Flask web UI (main entry point)
├── core/
│   ├── playlist.py     ← Playlist logic, shuffle, auto-next
│   ├── deploy.py       ← Deploy to gameplay-lab audio dirs
│   ├── catalog.py      ← Track metadata catalog
│   └── station.py      ← Radio station config management
├── data/
│   └── stations.json   ← Station definitions
└── README.md           ← This file
```

## Usage

```powershell
# Start the web UI
cd tools/eagle-radio-studio
python app.py

# Open in browser
# http://localhost:5000
```

## Deployment Target

Audio files deploy to:
```
C:\Users\LENOVO\Desktop\GTA\Project Eagle\gta sa gameplay-lab\audio\streams\
```

## Multi-Agent Lock

Always acquire `game-write` lock before deploying audio:

```python
from tools.eagle_coord_lock import EagleCoordLock

with EagleCoordLock("game-write", chat=CHAT_ID, task="deploy-radio"):
    studio.deploy_station("CUSTOM_RADIO")
```

## Jira

SCRUM-147 — [Eagle Radio Studio](https://nguyennguyenle997.atlassian.net/browse/SCRUM-147)
