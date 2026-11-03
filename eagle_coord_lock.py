"""
Unified Multi-Conversation Coordination Lock Utility for Project Eagle (`gta sa gameplay-lab`).

Canonical lock tool across ALL workflows (Map Building / Mondstadt / WIBU-01 / INLAND-03A,
WaifuLink, Skin/Texture/Radio Studios, and Codex plugin transactions).

Supports two atomic directory-based locks under `data/project-eagle/coordination/`:
  1. `game-write`     -> `game-write.lock`
     Exclusive lock for modifying shared runtime files, `.img`/`.ipl`/`.ide`/`.col`/`.pegg` archives,
     `peds.ide`, `hud.lua`, `eagle_dating_sim.py`, `EagleCompanion.py`, or shared deployment metadata.
  2. `ingame-runtime` -> `ingame-runtime.lock`
     Exclusive lock for launching/killing `gta_pe.exe`, running `EagleCompanion.py` on `:8765`,
     running `eagle_ingame_tester.py` / DirectX 9 crawlers, reading/resetting
     `Project Eagle/gta sa gameplay-lab/data/eagle_companion.db`, or sending synthetic keyboard/mouse
     input (`SendInput` / `keybd_event`) to the Windows desktop.

NEVER run `taskkill /IM gta_pe.exe` or launch `gta_pe.exe` BEFORE acquiring `ingame-runtime`!

CLI Usage:
  python tools/eagle_coord_lock.py status
  python tools/eagle_coord_lock.py acquire game-write --chat <CHAT_ID> --task "<TASK>" --resources CUSTOM/CUSTOM_MODS.ipl
  python tools/eagle_coord_lock.py acquire ingame-runtime --chat <CHAT_ID> --task "<TASK>" --wait 900
  python tools/eagle_coord_lock.py release ingame-runtime --chat <CHAT_ID>

Python Context Manager Usage:
  from eagle_coord_lock import EagleCoordLock
  with EagleCoordLock("ingame-runtime", chat="<CHAT_ID>", task="Live D3D9 QA", wait_sec=900):
      ... # safe to launch EagleCompanion.py + gta_pe.exe here!
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Optional

WORKSPACE_ROOT = Path(r"C:\Users\LENOVO\Desktop\GTA")
COORD_DIR = WORKSPACE_ROOT / "data" / "project-eagle" / "coordination"
LOCK_MAP = {
    "game-write": COORD_DIR / "game-write.lock",
    "ingame-runtime": COORD_DIR / "ingame-runtime.lock",
}
FILE_ATTRIBUTE_REPARSE_POINT = 0x0400


def _now_iso_pair() -> tuple[str, str]:
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    return now_utc.astimezone().isoformat(), now_utc.isoformat()


def _assert_no_reparse(target: Path, stop_at: Path = WORKSPACE_ROOT) -> None:
    """Guard borrowed from Codex deploy_plugin.py: reject junctions/symlinks along coordination lock path."""
    cur = target
    stop_resolved = os.path.normcase(str(stop_at))
    while True:
        if cur.exists() or cur.is_symlink():
            if cur.is_symlink():
                raise RuntimeError(f"Refusing symlink/reparse point on lock path: {cur}")
            try:
                st = os.lstat(cur)
                attrs = getattr(st, "st_file_attributes", 0)
                if attrs & FILE_ATTRIBUTE_REPARSE_POINT:
                    raise RuntimeError(f"Refusing Windows reparse point/junction on lock path: {cur}")
            except OSError:
                pass
        if os.path.normcase(str(cur)) == stop_resolved or cur.parent == cur:
            break
        cur = cur.parent


def _pid_alive(pid: int) -> bool:
    if pid <= 0:
        return False
    if os.name == "nt":
        try:
            res = subprocess.run(
                [
                    "powershell.exe",
                    "-NoProfile",
                    "-NonInteractive",
                    "-Command",
                    f"@(Get-Process -Id {int(pid)} -ErrorAction SilentlyContinue).Count",
                ],
                capture_output=True,
                text=True,
                timeout=10,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
            )
            if res.returncode == 0 and res.stdout.strip().isdigit():
                return int(res.stdout.strip()) > 0
        except Exception:
            return True
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True


def read_lock_owner(lock_name: str) -> Optional[dict[str, Any]]:
    lock_dir = LOCK_MAP[lock_name]
    if not lock_dir.exists():
        return None
    # Safeguard against legacy Wave 4/5-style scripts that mistakenly wrote a plain JSON file instead of a directory
    if lock_dir.is_file():
        try:
            data = json.loads(lock_dir.read_text(encoding="utf-8-sig"))
            if isinstance(data, dict):
                data["legacy_plain_file_lock"] = True
                pid = int(data.get("pid", 0) or 0)
                data["pid_alive"] = _pid_alive(pid) if pid else None
                return data
        except Exception as exc:
            return {"status": "legacy_plain_file_lock_unreadable", "error": str(exc), "path": str(lock_dir)}
        return {"status": "legacy_plain_file_lock", "path": str(lock_dir)}

    owner_file = lock_dir / "owner.json"
    if not owner_file.exists():
        return {"status": "locked_without_owner_json", "path": str(lock_dir)}
    try:
        data = json.loads(owner_file.read_text(encoding="utf-8-sig"))
        pid = int(data.get("pid", 0) or 0)
        data["pid_alive"] = _pid_alive(pid) if pid else None
        return data
    except Exception as exc:
        return {"status": "corrupt_owner_json", "error": str(exc), "path": str(lock_dir)}


def acquire_lock(
    lock_name: str,
    chat: str,
    task: str,
    agent: str = "Antigravity",
    work_item: str = "",
    resources: Optional[list[str]] = None,
    pid: Optional[int] = None,
    wait_sec: float = 600.0,
    poll_sec: float = 3.0,
    stale_dead_pid_grace_sec: float = 45.0,
) -> dict[str, Any]:
    if lock_name not in LOCK_MAP:
        raise ValueError(f"Unknown lock_name {lock_name!r}; expected one of {list(LOCK_MAP)}")
    COORD_DIR.mkdir(parents=True, exist_ok=True)
    lock_dir = LOCK_MAP[lock_name]
    _assert_no_reparse(lock_dir)
    owner_pid = int(pid if pid is not None else os.getpid())
    deadline = time.time() + max(0.0, float(wait_sec))
    last_log = 0.0

    while True:
        try:
            os.mkdir(lock_dir)
            local_iso, utc_iso = _now_iso_pair()
            meta = {
                "lock": lock_name,
                "agent": agent,
                "chat": chat,
                "task": task,
                "work_item": work_item,
                "resources": list(resources or []),
                "pid": owner_pid,
                "acquired_at": local_iso,
                "acquired_utc": utc_iso,
                "acquired_epoch": round(time.time(), 3),
            }
            (lock_dir / "owner.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
            return meta
        except FileExistsError:
            owner = read_lock_owner(lock_name) or {}
            # Reclaim ONLY if an explicitly recorded owner PID has exited AND grace period elapsed
            rec_pid = int(owner.get("pid", 0) or 0)
            acq_ep = float(owner.get("acquired_epoch", 0.0) or 0.0)
            age = (time.time() - acq_ep) if acq_ep > 0 else 0.0
            if rec_pid > 0 and owner.get("pid_alive") is False and age > stale_dead_pid_grace_sec:
                try:
                    if lock_dir.is_file():
                        lock_dir.unlink()
                    else:
                        owner_file = lock_dir / "owner.json"
                        if owner_file.exists():
                            owner_file.unlink()
                        os.rmdir(lock_dir)
                    print(
                        f"[LOCK] Reclaimed stale {lock_name}.lock from exited PID {rec_pid} (chat={owner.get('chat')}).",
                        file=sys.stderr,
                    )
                    continue
                except OSError:
                    pass

            now = time.time()
            if now >= deadline:
                raise TimeoutError(
                    f"Timed out waiting {wait_sec:.0f}s for {lock_name}.lock; currently held by: {json.dumps(owner, ensure_ascii=False)}"
                )
            if now - last_log >= 10.0:
                rem = max(0.0, deadline - now)
                print(
                    f"[LOCK WAIT] {lock_name}.lock busy (chat={owner.get('chat')}, task={owner.get('task')}, pid={owner.get('pid')}, alive={owner.get('pid_alive')}); waiting ({rem:.0f}s left)...",
                    file=sys.stderr,
                    flush=True,
                )
                last_log = now
            time.sleep(min(poll_sec, max(0.2, deadline - now)))


def release_lock(lock_name: str, chat: str = "", force: bool = False) -> bool:
    if lock_name not in LOCK_MAP:
        raise ValueError(f"Unknown lock_name {lock_name!r}")
    lock_dir = LOCK_MAP[lock_name]
    if not lock_dir.exists():
        return False
    if lock_dir.is_file():
        if not force:
            raise PermissionError(
                f"{lock_name}.lock exists as a legacy plain file instead of a directory; inspect before --force removal."
            )
        lock_dir.unlink()
        return True

    owner_file = lock_dir / "owner.json"
    if owner_file.exists() and chat and not force:
        try:
            data = json.loads(owner_file.read_text(encoding="utf-8-sig"))
            held_chat = str(data.get("chat", ""))
            if held_chat and held_chat != chat:
                raise PermissionError(
                    f"Refusing to release {lock_name}.lock owned by chat={held_chat!r} (caller chat={chat!r})"
                )
        except PermissionError:
            raise
        except Exception:
            pass
    if owner_file.exists():
        owner_file.unlink()
    os.rmdir(lock_dir)
    return True


class EagleCoordLock:
    """Context manager for safe multi-agent file-write or in-game D3D9 testing."""

    def __init__(
        self,
        lock_name: str,
        chat: str,
        task: str,
        work_item: str = "",
        resources: Optional[list[str]] = None,
        agent: str = "Antigravity",
        wait_sec: float = 900.0,
    ) -> None:
        self.lock_name = lock_name
        self.chat = chat
        self.task = task
        self.work_item = work_item
        self.resources = resources
        self.agent = agent
        self.wait_sec = wait_sec
        self.meta: Optional[dict[str, Any]] = None

    def __enter__(self) -> dict[str, Any]:
        self.meta = acquire_lock(
            self.lock_name,
            chat=self.chat,
            task=self.task,
            agent=self.agent,
            work_item=self.work_item,
            resources=self.resources,
            pid=os.getpid(),
            wait_sec=self.wait_sec,
        )
        return self.meta

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        release_lock(self.lock_name, chat=self.chat)


def main() -> int:
    parser = argparse.ArgumentParser(description="Project Eagle Unified Multi-Conversation Lock Tool")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("status", help="Show status of game-write.lock and ingame-runtime.lock")

    p_acq = sub.add_parser("acquire", help="Acquire a coordination lock")
    p_acq.add_argument("lock_name", choices=list(LOCK_MAP.keys()))
    p_acq.add_argument("--chat", required=True, help="Conversation ID")
    p_acq.add_argument("--task", required=True, help="Short description of current operation")
    p_acq.add_argument("--agent", default="Antigravity", help="Agent name (Antigravity or Codex)")
    p_acq.add_argument("--work-item", default="", help="Relative path to work-item markdown")
    p_acq.add_argument("--resources", nargs="*", default=[], help="Optional list of target files/archives")
    p_acq.add_argument("--pid", type=int, default=0, help="Long-lived parent PID (0 = omit auto-reclaim by PID)")
    p_acq.add_argument("--wait", type=float, default=600.0, help="Max seconds to wait if busy")

    p_rel = sub.add_parser("release", help="Release a coordination lock")
    p_rel.add_argument("lock_name", choices=list(LOCK_MAP.keys()))
    p_rel.add_argument("--chat", default="", help="Conversation ID verification")
    p_rel.add_argument("--force", action="store_true", help="Force release even if chat differs")

    args = parser.parse_args()
    if args.cmd == "status":
        out = {name: read_lock_owner(name) for name in LOCK_MAP}
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return 0
    if args.cmd == "acquire":
        meta = acquire_lock(
            args.lock_name,
            chat=args.chat,
            task=args.task,
            agent=args.agent,
            work_item=args.work_item,
            resources=args.resources,
            pid=args.pid,
            wait_sec=args.wait,
        )
        print(json.dumps(meta, indent=2, ensure_ascii=False))
        return 0
    if args.cmd == "release":
        released = release_lock(args.lock_name, chat=args.chat, force=args.force)
        print(json.dumps({"lock": args.lock_name, "released": released}, ensure_ascii=False))
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
