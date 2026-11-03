# eagle_coord_lock.py — Unified Multi-Agent Coordination Lock

> **Project Eagle** | Multi-Agent Infrastructure | v1.0 (2026-11-04)

## Overview

`eagle_coord_lock.py` is the unified multi-agent coordination lock system for Project Eagle. It prevents race conditions when multiple AI agents (Antigravity, Codex, etc.) work in parallel on the same game files or runtime resources.

## Lock Types

| Lock Name | Lock File | Purpose |
|-----------|-----------|---------|
| `game-write` | `game-write.lock` | Acquiring before writing to gameplay-lab game files, archives, configs |
| `ingame-runtime` | `ingame-runtime.lock` | Acquiring before modifying in-memory or runtime GTA SA state |

## Installation

No dependencies beyond Python 3.8+ standard library. The script is self-contained.

```
tools/
└── eagle_coord_lock.py   ← this file
```

## CLI Usage

```powershell
# Check current lock status
python tools/eagle_coord_lock.py status

# Acquire the game-write lock
python tools/eagle_coord_lock.py acquire game-write --chat "bc8612dc" --task "deploy-skin" --resources "models/player.dff"

# Acquire the ingame-runtime lock
python tools/eagle_coord_lock.py acquire ingame-runtime --chat "bc8612dc" --task "test-cleo"

# Release the lock
python tools/eagle_coord_lock.py release game-write

# Force-release a stale lock (if original holder is dead)
python tools/eagle_coord_lock.py release game-write --force
```

## Python API — Context Manager

```python
from tools.eagle_coord_lock import EagleCoordLock

# Automatically acquires lock on enter, releases on exit
with EagleCoordLock(
    lock_name="game-write",
    chat="bc8612dc-2d29-44d1-b10a-17602bfec29c",
    task="deploy-loading-screens",
    resources=["txd/loading_screen_01.txd", "txd/loading_screen_02.txd"]
) as lock:
    # Safe to write game files here
    deploy_files(...)
    # Lock is automatically released when block exits
```

## Lock File Format (`owner.json`)

```json
{
  "agent": "antigravity",
  "chat": "bc8612dc-2d29-44d1-b10a-17602bfec29c",
  "task": "deploy-loading-screens",
  "pid": 12345,
  "resources": ["txd/loading_screen_01.txd"],
  "acquired_at": "2026-11-04T06:00:00+07:00"
}
```

## Stale Lock Recovery

If the owning process (by PID) has died, the lock is automatically reclaimed after **45 seconds**. This prevents permanent deadlock from crashed agents.

```
Lock file exists
  → PID alive? → Wait and retry
  → PID dead AND age > 45s? → Reclaim automatically
  → PID dead AND age < 45s? → Wait for safety window
```

## Security

- **Symlink/junction protection**: The lock directory is verified to be a real directory, not a symlink or junction, before writing. This prevents lock file injection attacks.
- **Atomic write**: Lock files are written atomically using temp-file + rename.

## Workflow Integration

```
Agent wants to write game files
        ↓
  EagleCoordLock("game-write").acquire()
        ↓
  [write files to gameplay-lab]
        ↓
  EagleCoordLock("game-write").release()
        ↓
  Other agent can now acquire
```

## Multi-Agent Coordination Protocol

Per [shared-agent-workflow.md](../docs/project-eagle/shared-agent-workflow.md):

1. Check `status` before starting any write operation
2. Register your scope in the lock's `task` field
3. Write only the resources listed in `resources`
4. Release immediately when done — do not hold lock longer than needed
5. Never bypass the lock system by writing directly

## Related Documentation

- [shared-agent-workflow.md](../docs/project-eagle/shared-agent-workflow.md) — Full coordination protocol
- [Confluence: Tools & Utilities Reference](https://nguyennguyenle997.atlassian.net/wiki/spaces/EAGLE/pages/98386)
- Jira ticket: SCRUM-146
