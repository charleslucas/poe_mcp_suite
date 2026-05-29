---
name: verify-install
description: Verify the poe_mcp_suite install end-to-end — exercises all MCP servers and reports a green/red health table. Manual procedure; run after a fresh clone, a git pull + submodule update, or .mcp.json/env changes.
disable-model-invocation: true
---

This is the suite's install-verification procedure, invoked manually with `/verify-install`. The playbook in `playbooks/` is the single source of truth.

Read `playbooks/verify-install.md` and follow its tiered checklist exactly. Report the green/red table at the end and stop before any destructive cleanup.
