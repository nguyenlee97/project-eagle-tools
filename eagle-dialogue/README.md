# Eagle Dialogue — Paimon companion

**Current25/10: Paimon Agent installed.** See [handover](../../docs/project-eagle/dialogue/paimon-agent-2026-10-25.md). Current transaction: `paimon_agent_deploy.py status/rollback`; older web/VN recovery is superseded. Input8192, full output16384, native220-character pages/150s turn deadline; real Engine actions, durable wallet and receipt journal. Lower sections retain historical implementation notes.


**Current AI (25/10): GPT-6 Luna directly through OpenAI**, matching Character Chat's existing credential reference, with a separate Paimon profile, low reasoning and1200 completion cap. Web/native turns hot-load it. [AI ownership, verification and rollback](../../docs/project-eagle/dialogue/paimon-luna-2026-10-25.md).

**Web test ready:** http://127.0.0.1:8765/paimon, or EaglePhone app11 -> Try Paimon on web. Same AI/persona/2010 guard/36 prompts, separate test memory. Demo/chat modes require no GTA. [Startup, verification and recovery](../../docs/project-eagle/dialogue/paimon-web-test-2026-10-24.md). Web flow has been browser/API tested; native gameplay QA below remains separate.

Target: Project Eagle gameplay-lab. Existing `Start_Eagle_Lab_With_Sidecar.bat`, then F7 -> 11.Paimon -> I/K select -> F9. VN panel with three random choices from36 English prompts; UP/DOWN selects, Enter sends, typing returns to free text, Backspace edits, TAB leaves. User reports the base feature works; new UI gameplay testing remains theirs.

Read [current state](../../docs/project-eagle/dialogue/current-state.md), [diary](../../docs/project-eagle/dialogue/development-diary.md) and [work item](../../docs/project-eagle/work-items/2026-10-23-codex-paimon-companion.md) before changes. Skin is the existing model48295 Paimon; no archive rebuild or global slot ownership.

## Source

- `bridge/paimon.py`, `build_paimon.py`: Phone-command CLEO builder; original pilot builder retained as historical source/tests.
- `bridge/choices.py`, `hud/paimon_hud.lua`, `build_vn_hud.py`: trusted pool, plain snapshot reader/VN renderer and latest-HUD integration builder.
- `vn_hud_deploy.py`: current five-target guarded transaction; preserve current debugger HUD and refresh its source mirror. [VN handover](../../docs/project-eagle/dialogue/vn-hud-2026-10-23.md).
- `runtime/eagle_dialogue/paimon_web.py`, `paimon_web.html`, `paimon_choices.json`: web session/AI/context/memory backend, VN page and canonical prompt pool. `build_paimon_web.py` and `paimon_web_deploy.py` build/deploy the independent seven-target web transaction from current Phone sources.
- `runtime/eagle_dialogue/paimon_context.py`: game-date grounding and spoiler gates; only exact/current-day news, no PC date or future market anchors.
- `paimon_store.py`: bounded SQLite observations/accepted turns, stable character and branch isolation after load/rewind.
- `paimon_service.py`: asynchronous text-only OpenAI-compatible API caller; no mock or executable-tool fallback.
- `paimon_phone.py`: narrow Engine hooks/context publication, Phone command, status and deterministic portfolio reminders.
- `integrate_paimon.py`: hooks latest localized/map-fixed Engine/Web/HUD into staging; mirrored sources remain current.
- `paimon_deploy.py`: older15-target Paimon transaction, retained before-images. It and earlier repair/pilot layers refuse superseding ownership.

## Build/check/recover

```powershell
C:\Python310\python.exe -B -m unittest discover -s tools\eagle-dialogue\tests -p 'test_*.py'
C:\Python310\python.exe -B tools\eagle-dialogue\vn_hud_deploy.py status
```

Current transaction is applied at `staging/project-eagle/paimon-vn-hud-20261023/manifest.json`. Build order: `build_paimon.py --output-dir <staging>/native`, `build_vn_hud.py`, guarded `vn_hud_deploy.py prepare/apply`. A prepared unused plan may be revised only with all before hashes matching; old plan metadata is retained. Future installed changes require inspecting current ownership. With GTA closed, `vn_hud_deploy.py rollback` restores this slice and refuses drift; SQLite/backend/API/launcher remain intact. Do not restore whole old Phone/game directories.

Lua checks use optional development dependencies `lupa` (`lupa.lua51`) and `Pillow`; `preview_vn_hud.py` captures the real Lua draw commands using approximate fonts. The game does not depend on these Python packages. Actual font/input/appearance remains user QA.

## API ownership

Paimon now owns `data/project-eagle/paimon/connection.json`, with direct OpenAI/gpt-6-luna and the same named external credential as Character Chat. Runtime/source paimon_config.json hot-load this independent secret-free profile. No keys in source/config/logs; no automatic fallback. The old API chat's relay/profile is historical for Paimon and remains untouched.

The existing launcher starts/reuses Paimon and autostarts only this project's configured 127.0.0.1:18082 provider relay if absent. Remote endpoints are not launched. Normal game/Phone startup remains the original BAT flow. Native waits at most45s; transport capped35s. Replies are bounded160 ASCII characters for the verified game buffer path.

Prompt/date/source/output gates reduce future disclosure but cannot erase modern model priors; assess actual persona/spoiler behavior during user testing. Memory forks across native reload/rewind until save identity is reliable. News/portfolio/context are game data, not live web information or automatic trade authority.

API schema reference: [Chat Completions](https://developers.openai.com/api/reference/resources/chat). Native literal-string copy semantics: [CLEO5 v5.0.3 MemoryOperations](https://raw.githubusercontent.com/cleolibrary/CLEO5/v5.0.3/cleo_plugins/MemoryOperations/MemoryOperations.cpp).
