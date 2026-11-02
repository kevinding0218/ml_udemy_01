# Claude Code CLI — Model Management

## Current models (as of Nov 2026)

| Model | ID | Notes |
|---|---|---|
| Claude Fable 5 | `claude-fable-5` | Most capable, highest cost |
| Claude Opus 4.8 | `claude-opus-4-8` | Best balance for complex tasks |
| Claude Sonnet 5 | `claude-sonnet-5` | Fast, strong reasoning |
| Claude Sonnet 4.6 | `claude-sonnet-4-6` | Default in many sessions |
| Claude Haiku 4.5 | `claude-haiku-4-5` | Fastest, cheapest, 200K context |

---

## 1 — Check which model is active

**Option A:** Look at the status line at the bottom of the terminal — it shows the active model name.

**Option B:** Type `/model` with no argument in the Claude Code prompt — it opens an interactive picker showing the current selection.

**Option C:** Ask Claude directly:
```
Which model are you running on?
```

---

## 2 — Switch models mid-session

Type `/model` in the Claude Code prompt to open an interactive model picker.
Select a model with arrow keys, press Enter. The switch takes effect immediately for all
subsequent messages in the current session.

The change is session-only — it does not persist when you open a new CLI window.

---

## 3 — Set a default model for all future sessions

Claude Code reads its defaults from `~/.claude/settings.json`.

### Option A: Ask Claude to update it for you (easiest)

Just say:
```
Can you update my default model to claude-opus-4-8 in settings.json?
```
Claude will find the file, add or update the `model` key, and confirm.

### Option B: Edit it yourself

```bash
open ~/.claude/settings.json
```

Add or update the `model` key:

```json
{
  "model": "claude-opus-4-8"
}
```

If the file already has other keys, just add `"model"` anywhere in the top-level object:

```json
{
  "someOtherKey": "value",
  "model": "claude-sonnet-5"
}
```

Save the file. Every new Claude Code session will now open with that model by default.

### Option C: Create the file from scratch if it doesn't exist

```bash
mkdir -p ~/.claude
echo '{"model": "claude-opus-4-8"}' > ~/.claude/settings.json
```

---

## Quick reference

| Goal | How |
|---|---|
| See current model | Look at status line, or type `/model` |
| Switch model this session | `/model` → pick from list |
| Persist default across sessions | Edit `~/.claude/settings.json` → `"model": "claude-..."` |
| Ask Claude to update settings | Say: "update my default model to X in settings.json" |

---

## Notes

- Model IDs never take date suffixes — use `claude-opus-4-8`, not `claude-opus-4-8-20251101`.
- Switching with `/model` mid-session does not affect the `settings.json` default.
- If `settings.json` does not exist, Claude Code uses its own built-in default.
