# Isolated Paimon API gateway

See [the handover](../../docs/project-eagle/dialogue/opencode2api-handover.md) for current readiness, sources, verification, credentials and recovery. **Groq is now verified and selected**, using a separate text-only relay at `127.0.0.1:18082/v1`. The old anonymous OpenCode gateway on 18080 remains a historical quota-blocked option.

From the workspace root:

```powershell
.\tools\opencode2api\provider_service.ps1 -Action status
.\tools\opencode2api\provider_service.ps1 -Action start
```

The key-entry page is `http://127.0.0.1:18082`. It selects Groq first; it calls OpenAI only when Groq cannot pass and the user has supplied an OpenAI key. No OpenAI key was needed or used in the completed verification. `provider-status.json` in task staging records secret-free evidence.

No game startup BAT, game files or shared companion sources are owned by this tool. Do not publish the private `state` directory. `install.json` and the staging connection file contain no secret; local relay authentication is supplied through `EAGLE_OPENCODE_API_KEY`, while the dedicated upstream key is in `EAGLE_GROQ_API_KEY` and private state.
