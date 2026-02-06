# Tooling & MCP Strategy

Purpose: document the MCP (Model Control Plane) servers and local tooling configuration that support day-to-day development on Project Chimera.

Project Context: This is Project Chimera, an autonomous influencer system.

Selected MCP Servers

- `githubMCP` (git-mcp): Remote Git-backed MCP used for versioned interactions and repo-aware operations. Useful for creating PRs, fetching history, and syncing changes between local edits and remote.
- `filesystem-mcp` (local filesystem container): Provides the ability to run controlled filesystem operations inside a containerized environment (mounts), useful for running formatters, linters, and ephemeral editors without granting broad host access.
- `tenxfeedbackanalytics` (observability/telemetry): Collects development telemetry, performance logs, and audit events. Useful for feedback on agent behaviors and automated scans.

Recommended `mcp.json` snippets

Use workspace-relative server entries (example `.vscode/mcp.json`):

```json
{
  "servers": {
    "githubMCP": {
      "type": "http",
      "url": "https://gitmcp.io/your-org/your-repo"
    },
    "filesystem": {
      "type": "http",
      "url": "http://localhost:12345/filesystem"
    },
    "tenxfeedbackanalytics": {
      "type": "http",
      "url": "https://mcppulse.10academy.org/proxy"
    }
  }
}
```

How each server helps development

- `githubMCP` (git-mcp):
  - Create branch-scoped changes, open PRs, and fetch remote diffs.
  - Best practice: use for any change that should be tracked or reviewed.

- `filesystem-mcp`:
  - Bind only specific host paths into the container for targeted edits and formatting.
  - Example docker run (Windows paths must be quoted):

    docker run -i --rm --mount type=bind,src="C:\Users\eyobe\OneDrive\Desktop",dst=/projects/Desktop mcp/filesystem /projects

  - Use readonly mounts for directories that must not be modified.

- `tenxfeedbackanalytics`:
  - Send development telemetry and trigger feedback logs for agent interactions.
  - Useful to comply with Snyk/security scanning workflow and to capture performance outliers.

Security and Permissions

- Principle of Least Privilege: only mount or give the MCP server access to minimal required directories.
- For `filesystem-mcp`, prefer read-only mounts for host directories when mutation is not needed.
- Ensure `githubMCP` tokens and credentials are stored in the workspace secrets manager or external Vault; do not check them into the repo.

Operational Advice

- Use `githubMCP` for edits that require code review; use `filesystem-mcp` for quick, isolated tooling runs (formatters, linters).
- Before running any agent-driven code generation, consult `specs/` per the Prime Directive. Include spec reference in commit/PR.
- Periodically export the MCP config (`.vscode/mcp.json`) for CI and onboarding documentation.

Next steps

- Add example local `docker run` wrapper script for `filesystem-mcp` in `tools/` to standardize mounts across the team.
- Optionally, add a `CLAUDE.md` or top-level `README` note referencing `.cursor/rules` for onboarded copilots.
