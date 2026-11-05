# Project Eagle Tools

> GTA San Andreas × Genshin Impact | Infrastructure & Tooling

## Repositories

| Repo | Description | Jira |
|------|-------------|------|
| [eagle-story-quest](https://github.com/nguyenlee97/eagle-story-quest) | VN Story Quest engine + Hu Tao / Citlali / Furina campaigns | SCRUM-170,174,178 |
| [eagle-waifulink](https://github.com/nguyenlee97/eagle-waifulink) | Dating sim, BGM v1.1, JP Voice, 6 heroines | SCRUM-141,160,173 |
| [eagle-market](https://github.com/nguyenlee97/eagle-market) | Wall Street, Trading, Eagle Times, EagleStake Casino | SCRUM-166-169 |
| [eagle-phone-os](https://github.com/nguyenlee97/eagle-phone-os) | EaglePhone OS v6.3, EagleRide v2.0, App UIs | SCRUM-161,162,176 |
| [eagle-debug-toolkit](https://github.com/nguyenlee97/eagle-debug-toolkit) | Savegame sync, Mondstadt bridge, diagnostics | SCRUM-177 |
| [project-eagle-tools](https://github.com/nguyenlee97/project-eagle-tools) | Coord lock, character chat (14 NPCs), CI scripts | SCRUM-146,163 |
| [eagle-map-glitch-lab](https://github.com/nguyenlee97/eagle-map-glitch-lab) | 3D map walker & boundary explorer | SCRUM-151 |

## Multi-Agent Lock

All tools writing to gameplay-lab must use `eagle_coord_lock.py`:

```python
from eagle_coord_lock import EagleCoordLock

with EagleCoordLock("game-write", chat=CHAT_ID, task="deploy", resources=["file.txd"]):
    # Safe to write to gameplay-lab
    ...
```

## Game Target
`C:\Users\LENOVO\Desktop\GTA\Project Eagle\gta sa gameplay-lab`

## Docs
- [Confluence Space EAGLE](https://nguyennguyenle997.atlassian.net/wiki/spaces/EAGLE)
- [Jira Board SCRUM](https://nguyennguyenle997.atlassian.net/jira/software/projects/SCRUM/boards)
