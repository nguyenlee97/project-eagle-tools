# Project Eagle Tools

> **GTA San Andreas Modding Infrastructure** | Project Eagle

Collection of tools and utilities developed for Project Eagle — a GTA San Andreas total conversion featuring Genshin Impact characters, custom radio, and enhanced world-building.

## Tools Overview

| Tool | Path | Purpose | Jira |
|------|------|---------|------|
| [eagle_coord_lock.py](README-eagle-coord-lock.md) | `eagle_coord_lock.py` | Multi-agent coordination lock (game-write + ingame-runtime) | SCRUM-146 |
| [Eagle Radio Studio](eagle-radio-studio/README.md) | `eagle-radio-studio/` | Menu music & playlist management, deploy to gameplay-lab | SCRUM-147 |
| [Conversation Tracker](conversation-tracker/README.md) | `conversation-tracker/` | Confluence auto-push & conversation analysis | SCRUM-148 |
| [Skin Viewer](skin-viewer/README.md) | `skin-viewer/` | DFF/TXD deploy & skin catalog management | SCRUM-149 |
| [World Texture Studio](world-texture-studio/README.md) | `world-texture-studio/` | 3D texture catalog & deploy to gameplay-lab | SCRUM-150 |
| [Map Glitch Lab](map-glitch-lab/README.md) | `map-glitch-lab/` | 3D map walker & glitch/boundary exploration | SCRUM-151 |
| [Eagle Character Chat](eagle-character-chat/README.md) | `eagle-character-chat/` | Genshin character dialogue engine for WaifuLink | SCRUM-152 |
| [Eagle Dialogue](eagle-dialogue/README.md) | `eagle-dialogue/` | CLEO bridge & Visual Novel HUD deploy | SCRUM-153 |
| [OpenCode2API](opencode2api/README.md) | `opencode2api/` | LLM provider bridge (gpt-6-luna & others) | SCRUM-154 |

## Quick Start

```powershell
# Clone the repository
git clone https://github.com/nguyenlee97/project-eagle-tools.git
cd project-eagle-tools

# Check multi-agent lock status before any writes
python eagle_coord_lock.py status

# Start Eagle Radio Studio
python eagle-radio-studio/app.py

# Start World Texture Studio
python world-texture-studio/app.py
```

## Multi-Agent Coordination

All tools that write to gameplay-lab **must** use the coordination lock:

```python
from eagle_coord_lock import EagleCoordLock

with EagleCoordLock("game-write", chat=CHAT_ID, task="my-task", resources=["file.txd"]):
    # Safe to write here
    ...
```

See [README-eagle-coord-lock.md](README-eagle-coord-lock.md) for full documentation.

## Game Target

All tools deploy to:
```
C:\Users\LENOVO\Desktop\GTA\Project Eagle\gta sa gameplay-lab\
```

Do **not** use the archive at `D:\GTA Archive\Project Eagle\gta sa clean\` as a mod target.

## Documentation

- [Project Eagle Docs](https://nguyennguyenle997.atlassian.net/wiki/spaces/EAGLE)
- [Shared Agent Workflow](../docs/project-eagle/shared-agent-workflow.md)
- [Jira Board](https://nguyennguyenle997.atlassian.net/jira/software/projects/SCRUM/boards)

## Project

**Project Eagle** — GTA San Andreas × Genshin Impact  
Maintained by: nguyenlee97 | Agents: Antigravity (Gemini), Codex
