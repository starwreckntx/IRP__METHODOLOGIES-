---
name: tailscale-aperture-orchestrator
description: >
  Configure, manage, and troubleshoot Tailscale Aperture AI gateway deployments.
  Use when working with Aperture provider configs, access control grants, session
  telemetry, multi-model routing, Claude Code integration, or tailnet LLM orchestration.
---

# Tailscale Aperture Orchestrator Skill

This skill guides Claude through configuring and managing Aperture by Tailscale —
a centralized AI gateway that authenticates users via Tailscale identity instead of
distributing API keys. All LLM traffic routes through Aperture for visibility,
cost tracking, and access control.

---

## Core Architecture Understanding

Before generating any config or advice, internalize:

1. **Identity = Tailscale identity.** Users authenticate via tailnet membership —
   NOT via API keys. Aperture injects provider credentials server-side.
2. **Routing is model-name-based.** Aperture extracts the `model` field from
   the request body and routes to the matching configured provider.
3. **Always HTTP, not HTTPS** for client-to-Aperture connections. WireGuard
   handles transport encryption. HTTPS causes TLS errors.
4. **Tags ≠ Users.** Tag-based device identity loses per-user attribution.
   Always advise using personal Tailscale accounts for user-level tracking.
5. **Alpha product.** Features like rate limiting, prompt filtering are NOT yet
   supported. Never claim they exist.

---

## Supported Providers & Compatibility Matrix

| Provider     | Auth Header         | openai_chat | openai_responses | anthropic_messages | gemini | bedrock | vertex |
|-------------|---------------------|-------------|------------------|--------------------|--------|---------|--------|
| OpenAI       | Bearer              | ✅          | ✅               | ❌                 | ❌     | ❌      | ❌     |
| Anthropic    | x-api-key           | ❌          | ❌               | ✅                 | ❌     | ❌      | ❌     |
| Google Gemini| x-goog-api-key      | ❌          | ❌               | ❌                 | ✅     | ❌      | ❌     |
| Vertex AI    | Bearer              | ❌          | ❌               | ❌                 | ✅     | ❌      | ✅     |
| Bedrock      | Bearer              | ❌          | ❌               | ❌                 | ❌     | ✅      | ❌     |
| OpenRouter   | Bearer              | ✅          | ❌               | ❌                 | ❌     | ❌      | ❌     |
| Self-hosted  | varies              | ✅          | ❌               | ❌                 | ❌     | ❌      | ❌     |

---

## Workflow: Config Generation

### Step 1 — Identify providers needed

Ask or infer from context:
- Which AI providers (Anthropic, OpenAI, Gemini, Bedrock, self-hosted)?
- Which specific model IDs?
- Who needs access (all tailnet users, specific users, groups)?
- Any per-user model restrictions?

### Step 2 — Generate provider config

Anthropic example:
```json
{
  "providers": {
    "anthropic": {
      "baseurl": "https://api.anthropic.com",
      "authorization": {
        "type": "x-api-key",
        "value": "sk-ant-..."
      },
      "models": [
        "claude-haiku-4-5-20251001",
        "claude-sonnet-4-5",
        "claude-opus-4-5"
      ],
      "compatibility": {
        "anthropic_messages": true
      }
    }
  }
}
```

OpenAI example:
```json
{
  "providers": {
    "openai": {
      "baseurl": "https://api.openai.com",
      "authorization": {
        "type": "Bearer",
        "value": "sk-..."
      },
      "models": ["gpt-4o", "gpt-4o-mini", "o1"],
      "compatibility": {
        "openai_chat": true,
        "openai_responses": true
      }
    }
  }
}
```

Self-hosted on tailnet example:
```json
{
  "providers": {
    "private-llm": {
      "baseurl": "http://100.x.x.x:8080",
      "tailnet": true,
      "models": ["llama-3.1-70b", "qwen3-coder-30b"],
      "compatibility": {
        "openai_chat": true
      }
    }
  }
}
```

### Step 3 — Generate temp_grants

Open access for all tailnet members:
```json
"temp_grants": [
  {
    "src": ["*"],
    "grants": [
      {"role": "user"},
      {"providers": [{"provider": "*", "model": "*"}]}
    ]
  }
]
```

Admin + scoped model access:
```json
"temp_grants": [
  {
    "src": ["admin@example.com"],
    "grants": [
      {"role": "admin"},
      {"providers": [{"provider": "*", "model": "*"}]}
    ]
  },
  {
    "src": ["user@example.com"],
    "grants": [
      {"role": "user"},
      {"providers": [{"provider": "anthropic", "model": "*"}]}
    ]
  }
]
```

**Critical warning**: Removing the default `"*"` admin grant without explicitly
granting yourself admin access will lock you out of the Settings page.

### Step 4 — Validate mentally before output

Check:
- [ ] Every provider has `baseurl` and at least one model
- [ ] `authorization` type matches provider (Anthropic = `x-api-key`)
- [ ] No HTTPS in client connection URLs
- [ ] `temp_grants` includes at least one role grant
- [ ] Self-hosted providers have `"tailnet": true`

---

## Workflow: Claude Code Integration

When configuring Claude Code to use Aperture:

**Modern Claude Code (v2+)** — `~/.claude/settings.json`:
```json
{
  "apiKeyHelper": "echo '-'",
  "env": {
    "ANTHROPIC_BASE_URL": "http://ai"
  }
}
```

**Legacy Claude Code (v1.x)** — requires explicit model:
```json
{
  "model": "claude-sonnet-4-5",
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "bearer-managed",
    "ANTHROPIC_BASE_URL": "http://ai"
  }
}
```

**Via Bedrock**:
```json
{
  "env": {
    "ANTHROPIC_MODEL": "claude-sonnet-4-5",
    "ANTHROPIC_BEDROCK_BASE_URL": "http://ai/bedrock",
    "CLAUDE_CODE_USE_BEDROCK": "1",
    "CLAUDE_CODE_SKIP_BEDROCK_AUTH": "1"
  }
}
```

Replace `http://ai` with `http://<your-aperture-hostname>` or its FQDN
`http://<hostname>.<tailnet>.ts.net` if MagicDNS is not enabled.

---

## Workflow: Testing & Verification

Provide curl test commands appropriate to the provider being tested:

**Anthropic format:**
```bash
curl -s http://ai/v1/messages \
  -H "Content-Type: application/json" \
  -d '{
    "model": "claude-haiku-4-5-20251001",
    "max_tokens": 25,
    "messages": [{"role": "user", "content": "respond with: hello"}]
  }'
```

**OpenAI format:**
```bash
curl -s http://ai/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "gpt-4o", "messages": [{"role": "user", "content": "respond with: hello"}]}'
```

Tests must be run from a device on the tailnet. Remind user to check the
Aperture dashboard at `http://ai/ui/` after testing to confirm telemetry capture.

---

## Workflow: Access Control Configuration

For ACL changes in the Tailscale admin console to grant users access to Aperture:

```json
{
  "grants": [
    {
      "src": ["group:ai-users"],
      "dst": ["tag:aperture"],
      "ip": ["tcp:80", "tcp:443", "icmp:*"]
    }
  ]
}
```

Key principle: Aperture listens only on Tailscale interfaces. Non-tailnet
connections are blocked at the network level — this is a security feature,
not a bug.

---

## Workflow: Troubleshooting

### All sessions appear from same user
**Cause**: Devices authenticated with tag identity, not personal accounts.
**Fix**: Ensure users connect from devices associated with their personal
Tailscale accounts, not service-tagged devices.

### HTTPS connection failures
**Cause**: Client configured with `https://` instead of `http://`.
**Fix**: Change to `http://`. WireGuard provides encryption — no TLS needed.

### Provider routing failure (model not found)
**Cause**: Model ID in request doesn't match any configured model name.
**Fix**: Verify exact model string in providers config. Check `http://ai/ui/`
Models page for configured model IDs.

### Metrics showing partial token counts
**Cause**: Streaming response interrupted before completion.
**Expected behavior**: Partial capture is stored. This is by design in alpha.

### Lost admin access to Settings page
**Cause**: Removed `"*"` admin grant without adding explicit admin grant.
**Fix**: Requires direct config file intervention or Tailscale support.

---

## Multi-Model Orchestration Patterns

When the user wants to route different workloads to different models:

**Cost-tiered routing** (expensive flagship for complex tasks):
```json
"providers": {
  "anthropic-fast": {
    "baseurl": "https://api.anthropic.com",
    "models": ["claude-haiku-4-5-20251001"],
    "compatibility": {"anthropic_messages": true}
  },
  "anthropic-power": {
    "baseurl": "https://api.anthropic.com",
    "models": ["claude-opus-4-5"],
    "compatibility": {"anthropic_messages": true}
  }
}
```

**Scoped user access** (engineers get flagship, others get haiku):
```json
"temp_grants": [
  {
    "src": ["senior-eng@company.com"],
    "grants": [{"providers": [{"provider": "anthropic-power", "model": "*"}]}]
  },
  {
    "src": ["*"],
    "grants": [{"providers": [{"provider": "anthropic-fast", "model": "*"}]}]
  }
]
```

**Self-hosted LLM on tailnet** (private model, no public exposure):
```json
"providers": {
  "private-llm": {
    "baseurl": "http://100.x.x.x:8080",
    "tailnet": true,
    "models": ["llama-3.1-70b", "qwen3-coder-30b"],
    "compatibility": {"openai_chat": true}
  }
}
```

PurpBox-specific example (llama.cpp at 100.99.98.31:8080):
```json
"providers": {
  "purpbox-llm": {
    "baseurl": "http://100.99.98.31:8080",
    "tailnet": true,
    "models": ["llama-3.1-70b"],
    "compatibility": {"openai_chat": true}
  }
}
```

---

## Aperture Dashboard Reference

| Page      | URL              | What it shows                                      |
|-----------|------------------|----------------------------------------------------|
| Dashboard | /ui/             | Token usage, active sessions, quick stats          |
| Logs      | /ui/logs/        | Session-grouped request history, full captures     |
| Tool Use  | /ui/tool-use/    | Tool call patterns, histogram, per-session breakdown |
| Adoption  | /ui/adoption/    | Org-wide usage, top users, model popularity        |
| Models    | /ui/models/      | Configured models and provider info                |
| Settings  | /ui/settings/    | Config file editor (admin only)                    |

Admin can view any user's dashboard at `/ui/dashboard/<login-name>`.

---

## Session Tracking Behavior

- Sessions are grouped by conversation context, not individual requests
- Each session gets a unique ID visible in `/ui/logs/`
- Token counts are captured per-session, per-model, per-user
- Streaming sessions may show partial counts until stream completes
- Tool use (function calls) tracked separately at `/ui/tool-use/`

---

## Examples

- "Set up Aperture with Anthropic and OpenAI providers"
- "Configure Claude Code to use Aperture on my tailnet"
- "Add my llama.cpp server on PurpBox to Aperture"
- "Grant only senior engineers access to Claude Opus"
- "Why are all my Aperture sessions showing as the same user?"
- "Generate a curl command to test my Aperture Anthropic config"
- "Set up cost-tiered routing between Haiku and Opus"
