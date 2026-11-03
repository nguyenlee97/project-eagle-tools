# Eagle Character Chat

English-only, standalone conversation engine and local Conversation Studio for Venti, Jean, Diluc, Mona, Kaeya, Lisa, Klee, Barbara, Noelle and Fischl with Oz. No GTA runtime imports, game writes, skin installation or map integration.

**v0.3.3 roster update:** Noelle adds her own sourced dossier and optional Hangout boundaries. Fischl is accompanied by Oz in the encounter, with clearly attributed dialogue and one shared Fischl conversation-memory scope. Their model/skin inventory is documented separately from game installation.

**v0.3.2 roster update:** Klee and Barbara add separate sourced dossiers, adapted choices and private memory. Klee uses a child's voice with proportionate reported knowledge; Barbara distinguishes her own Prologue encounters from the dragon-rescue party. Optional story scenes remain progression-gated.

**v0.3.1 roster update:** Kaeya and Lisa add separate sourced biographies, relationships, disclosure limits, adapted dialogue and private memory. Character order is declared in `content/world.json`; installing another character requires its matching dialogue and cognition files.

**v0.3.0 grounding update:** sourced personal histories, typed relationships, character-specific knowledge/disclosure, separate Natlan and Snezhnaya events, focused question anchors and quoted conversation provenance. This addresses the independent audit's context gaps; real-model fidelity still requires answer review.

## Start

Double-click **Start_Character_Chat.bat**, or run:

```powershell
.\studio.ps1 -Action start
```

Open **http://127.0.0.1:8952**. Python 3.10+ with SQLite FTS5 is the only runtime dependency; no package installation or frontend build is required. The launcher reuses the existing selected AI relay when configured on local port 18082. It does not change the provider, credentials, or start GTA. Adapted dialogue remains available if the AI relay cannot start.

```powershell
.\studio.ps1 -Action status
.\studio.ps1 -Action stop
```

Stop affects only this studio's recorded process; the shared provider stays available to Paimon. `-NoBrowser` starts without opening a browser. For a separate QA instance, use `python -B -m eagle_character_chat.server --port 8953 --data-dir <dedicated-folder>`.

## Use

Select a character. Choose a dialogue option or type a free message. Replies from the supplied graphs are labeled **Adapted dialogue**: original English writing grounded in the linked sources, not verbatim in-game transcripts. Graph state advances only after a reply is shown. Follow-up questions receive the full preceding exchange.

**Memory** shows notes for the selected character and branch. Clear first-person messages such as `My nickname is Finch.`, `I like mint tea.`, or `I plan to visit Liyue.` can become attributed notes after the reply is displayed. This is conservative sentence matching, not unrestricted extraction from every message. `Actually, ...` and `Correction: ...` work with the same supported sentence forms. Other acknowledged conversation remains searchable. You can add/edit notes directly or use `Remember: <a detail>`; edited notes have priority over automatic extraction. Notes never turn NPC improvisation or player claims into world canon.

**Journey** creates a separate profile/playthrough or forks the current branch at a checkpoint. Checkpoints include accepted exchanges and note changes, not just message counts. A fork inherits only eligible history and the note versions in effect at that checkpoint. These are explicit standalone journeys, not detected GTA saves. No NPC reads another character's personal memories.

**Forget this exchange** removes the selected exchange, its derived note, search entry and related trace copies from the current branch. Independent later replies or branches may still mention that information and must be handled separately. Removing a note alone does not delete the conversation that originally mentioned it. This is a local recall editor, not secure erasure of SQLite backups/WAL pages.

**Reset character memory…** is below the notes in **Memory & sources**. It opens a confirmation naming the selected character and journey. Confirming clears all that character's local conversations, note versions, search/summary/trace data in the current branch and returns adapted choices to their starting point. Canonical background/shared story, other characters and other branches stay intact. Existing forks and backups can retain earlier copies. Canceling the dialog changes nothing. The action cannot be undone in the studio; a changed checkpoint or unfinished reply rejects a stale reset request.

At compact widths, Journey and Memory open as drawers. Enter sends; Shift+Enter starts a new line. Cancel discards an in-flight/undisplayed reply. API errors are explicit; the application never substitutes a fake AI answer.

## World, character and story continuity

The default story profile is **after Version 7.1**, with Aether already acquainted with the cast. A compact world foundation and current-event state are always supplied, even if supporting lore search returns no match. Venti's own history and the enabled canonical history with Aether exist independently of the local transcript. The character profiles distinguish public role, private identity, values, voice, disclosure and limits. Global-event awareness does not imply eyewitness participation.

`content/cognition/world.json` defines the setting, reviewed concepts/events, entity aliases and extra detail records. Events identify participants; other characters receive reported knowledge without becoming eyewitnesses. The adjacent character files contain private character foundations and canonical histories. `relationships` records identify subject/predicate/object; `awareness` records identify when a character learned something and whether disclosure is public, guarded or private with the Traveler. Jean and Diluc can know Venti's identity while respecting its privacy; this grants Mona, Kaeya or Lisa no such knowledge.

Optional shared encounters use explicit `requires_story` / `completed_optional` gates. Release versions describe when material became available, not an invented in-world calendar date. Editing a player memory never changes the world snapshot. A character's stable biography is distinct from whether Aether participated in an optional scene.

The most relevant reviewed records also appear as `question_anchors`. Character-specific relational phrases such as “your father” do not reinterpret the Traveler's own family. Recent and recalled dialogue are quoted with speaker attribution inside the context; previous generated replies are not sent as fresh assistant demonstrations or treated as factual evidence. This preserves old chats while allowing mistakes from an older content version to be corrected. It is a grounding strategy, not a proof that generation cannot repeat an error.

Reviewed briefs keep major world awareness and personal anchors present on every turn; relevant records retain their full text and, where authored, a chronological sequence. Factual “why/what happened” questions prioritize those causes over a character's general values. The assembled context has a 20,000-character budget; optional detail/history is trimmed before stable briefs. Full source records remain intact in the content pack.

Free-chat generation uses one compact JSON envelope containing selected evidence record IDs and the natural reply. The engine checks that those IDs were eligible in that request and attaches the original curated text locally; the model cannot fabricate an evidence quotation. Only the reply reaches chat. Invalid/truncated envelopes fail explicitly without committing a false fallback. Evidence selection is saved in the trace and costs no second verification call. These checks establish provenance, not semantic entailment: a model can still misuse a real record, so factual fidelity continues to need answer review.

Search adds details rather than deciding whether a character has heard of a major power. Relevant titles/aliases and recent follow-up subjects help retrieval. Old AI replies remain visible transcripts but are not canon; a reviewed correction takes precedence. Sources distinguish game-text transcripts hosted by the community, official material, editorial summaries and authored setting assumptions.

## Content and model limits

- Snapshot ceiling is 7.1. The starter records are supplemented by compact world/character foundations, selected personal relationships and historical/current events; this remains a bounded lore slice, not the full 7.1 storyline. There are **120 adapted choices**, 12 per character.
- Sources, retrieval scope, release version and content hashes are inspectable. Private identity records are filtered before lore retrieval. The model still has pretrained knowledge: prompt grounding is not a proof that it can never hallucinate or disclose an unsupported fact.
- Character fidelity and factual consistency need behavioral review. Automated context checks prove which information was supplied, not that every generated sentence is correct. The cognition evaluation fixture tests connected understanding, uncertainty, tone, canonical continuity and memory isolation.
- No voice, multiplayer, actor spawning, proximity trigger, GTA save reconciliation, quest progression or skin conversion is implemented.
- Free chat sends the selected prompt, character lore and relevant conversation context to the configured provider. Conversation storage is local. No keys are stored in this tool's configuration, database, logs or evidence.

## Layout and interfaces

- `eagle_character_chat/`: content validation/retrieval, SQLite store, conversation controller, API adapter and loopback HTTP server.
- `content/`: English character graphs, curated lore, source manifest and versioned cognition packs.
- `static/`: dependency-free local UI.
- Local state: workspace `data/project-eagle/character-chat/conversations.sqlite3` plus the studio process record/logs.
- Connection: dedicated `data/project-eagle/character-chat/connection.json` when present, otherwise the existing shared relay profile. Character Chat now selects `gpt-6-luna` directly through OpenAI, with low reasoning and structured dialogue output. Its credential is read from the explicitly named per-user environment value, not from a repository file. Shared Paimon/relay selection is independent.

Core entry points: `Engine.open_session`, `submit`, `state`, `cancel`, `remember`, `forget_exchange`; `Store.ack` commits a displayed turn. HTTP API exposes `/api/bootstrap`, sessions, turns/status/ack/cancel, notes, playthroughs and branches. Mutations require the bootstrap CSRF token and a local Host/Origin. No arbitrary file or command execution endpoint is exposed.

Only committed exchanges enter recall. Request IDs deduplicate retries even after the dialogue graph advances. Ready replies persist for acknowledgement across a restart; interrupted pending requests are cancelled. Four bounded worker slots, provider timeout <=35 seconds and no automatic paid failover.

## Verification

```powershell
python -B -m unittest discover -s tests -v
node --check static/app.js
```

Tests use temporary databases and a test-only HTTP provider. Live smoke checks are opt-in and send synthetic prompts through the real configured provider:

```powershell
python -B verify_live.py --output <dedicated-QA-folder>
python -B verify_cognition.py --staging ../../staging/project-eagle/character-cognition-v2-20261024
```

The cognition runner uses a fresh synthetic database, at most 20 provider calls, and saves responses for explicit review; lexical warning flags are not behavior scores. Use `--list-groups` or `--groups <IDs>` for focused runs. It never uses the user conversation database.

Content updates are validated at startup; restart the studio after editing JSON/core. Memory schema v2 is an additive migration preserving v1 IDs, text, source links and checkpoint intervals; it does not backfill old conversations. Unknown schemas fail instead of rebuilding. Code-only rollback to v0.1 cannot read a v2 database: preserve the upgraded DB separately and restore its matching pre-upgrade SQLite backup only if intentionally reverting the entire standalone app. Never overwrite newer conversations with an old backup during normal content changes.
