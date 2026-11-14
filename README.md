# eSAMTrade skills

A standalone collection of AI skills for Codex, GitHub Copilot and Claude Code, usable together in the same project. OpenCode is also supported. All skill instructions and supporting files are included here; no internal repository or shared checkout is required.

## Install in Claude Code

This repository is both a Claude Code plugin and a marketplace. Once these files are published to `eSAMTrade/skills`, run in your terminal:

```bash
claude plugin marketplace add eSAMTrade/skills
claude plugin install esamtrade-skills@esamtrade
```

The default is user scope, making the plugin available across your projects. Add `--scope project` to the install command to enable it for the current project. Inside Claude Code, the corresponding commands are `/plugin marketplace add eSAMTrade/skills` and `/plugin install esamtrade-skills@esamtrade`.

Start a new session and invoke, for example, `/esamtrade-skills:grill-me` or `/esamtrade-skills:spec-writer`. This installation uses Claude Code's plugin cache and needs neither Python nor `setup.py`. See the official [plugin installation guide](https://code.claude.com/docs/en/discover-plugins).

To try an unpublished local checkout from a project directory:

```bash
claude --plugin-dir /path/to/skills
```

## Install in Codex

After publishing the files to GitHub, ask Codex to install the complete collection with its built-in skill installer:

```text
$skill-installer Install every skill under skills/ from eSAMTrade/skills
(branch master), including code-standards and all supporting files.
Keep the skill directories as siblings so their relative references resolve.
```

The installer downloads the skills into your user skill directory. Install the whole collection to include cross-skill dependencies; this route does not require running this repository's `setup.py`. Once the skills are available, invoke one with `$grill-me` or `$spec-writer`. See the official [Codex skills documentation](https://developers.openai.com/codex/skills).

For a project-local installation from a checkout, use:

```bash
uv run /path/to/skills/setup.py install /path/to/project --assistant codex
```

This copies the collection into the project's `.agents/skills/`. Add `--skill grill-form`, for example, to install only that skill and its dependencies. Python requirements and update behavior are described below.

## Install project skills for several assistants

`setup.py` copies skills and their dependencies into the locations below. It creates ordinary files and directories, so no symlink permissions are needed and the source checkout can be moved or removed afterward.

| Assistant | Project directory |
| --- | --- |
| Codex and GitHub Copilot CLI | `.agents/skills/` |
| Claude Code | `.claude/skills/` |
| OpenCode, when selected | `.opencode/skills/` |

GitHub documents `.agents/skills` and `.claude/skills` as supported [Copilot skill locations](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-skills). VS Code discovery varies by harness; check the [VS Code skill locations](https://code.visualstudio.com/docs/agent-customization/agent-skills#skill-locations) for your session.

Requires Python 3.12+ and `aicodesign`, used for code provenance. With [uv](https://docs.astral.sh/uv/), the script's declared dependency is installed automatically:

```bash
uv run /path/to/skills/setup.py install /path/to/project
```

Or use a Python virtual environment:

```bash
python -m venv .venv
# Activate .venv for your shell, then:
python -m pip install 'aicodesign>=0.1.1'
python /path/to/skills/setup.py install /path/to/project
```

By default, all skills are copied to both `.agents/skills` and `.claude/skills`. To select assistants or skills, repeat `--assistant` or `--skill`:

```bash
python setup.py install /path/to/project --assistant claude --skill grill-form
python setup.py install /path/to/project --assistant codex --assistant copilot --skill py-dev
python setup.py install /path/to/project --assistant opencode
```

Dependencies are included automatically: `grill-form` brings `writing-style`; development skills bring the shared coding standards and their related workflows. Selecting Codex and Copilot uses the same destination once.

Rerunning the installer leaves identical files unchanged. Differing selected files stop the operation before copying; add `--force` to replace them. Unrelated files are preserved. Symlinked paths inside the destination are rejected, including mappings left by the older installer: inspect and remove those mappings yourself before installing again. Installation does not create `.github`, change `AGENTS.md`, or install a project formatter. Restart the assistant after copying. Choose either the plugin or copied skills for Claude in a project to avoid duplicate commands.

## Included skills

- `grill-me` and `grill-form`: explore decisions through questions, in chat or a browser questionnaire.
- `handoff`: prepare a concise handoff for another agent.
- `orchestrate-subagents`: delegate work using models and tools available in the current runtime.
- `web-ui-guidelines`: review interface behavior, layout, performance and content.
- `writing-style` and `spec-writer`: write clear prose and verifiable technical documents.
- `py-dev` and `java-dev`: implement and verify code using the project's toolchain and conventions.
- `code-standards`: bundled design, language, testing and document-creation rules.

Cross-skill links resolve relative to each installed `SKILL.md`, including inside the plugin cache. Install a skill through `setup.py --skill` to include its dependencies, or install the complete plugin. Copying a lone `SKILL.md` does not include its dependencies. `grill-form` carries its renderer beside the skill and copies it next to each generated HTML questionnaire.

## Synchronize a subset

The public `skills/` directory is the portable source. `SKILL_FILES` and `DEPENDENCIES` in `setup.py` define the exported files and required companion skills. Synchronize between collection roots in either direction:

```bash
python setup.py sync /path/to/source-collection /path/to/destination-collection --skill grill-form
python setup.py sync /path/to/source-collection /path/to/destination-collection --force
```

Both sides use the portable `skills/<name>/` layout. Only explicitly listed files are copied; local notes, caches and other unlisted files are excluded. Files absent from the source are not deleted. The command does not copy the installer or plugin manifests, commit, or push. When bringing changes from older internal instructions, port their paths and dependencies to this layout first; raw files with shared-checkout paths are not portable.

## Verify changes

From the repository root, with the Python dependency installed:

```bash
python -m unittest discover -s tests -v
claude plugin validate .claude-plugin/plugin.json --strict
claude plugin validate .claude-plugin/marketplace.json --strict
```

Tests exercise copied installation, subset dependency closure, relocation, conflict handling and selected-file synchronization. Manifest validation checks packaging; use a Claude Code session to verify actual skill execution.
