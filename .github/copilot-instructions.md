# Aider Copilot Instructions

## Repository Overview

**Aider** is an AI pair programming CLI tool that edits code in local git repositories using LLMs. Written in Python 3.9-3.12, works best with GPT-4o and Claude 3.5 Sonnet.

**Stats:** ~83MB, 97 Python files, CLI app with optional GUI, PyPI package: `aider-chat`

## Development Setup

**Required:** Python 3.9-3.12 (3.12 recommended), Git, pip, pip-tools

**Setup Steps (IN ORDER):**
```bash
# Create venv OUTSIDE repo to avoid conflicts
python -m venv ../aider_venv && source ../aider_venv/bin/activate

# Install (Windows: use ..\aider_venv\Scripts\activate)
pip install -e .
pip install -r requirements.txt
pip install -r requirements/requirements-dev.txt

# Optional: Enable pre-commit hooks
pre-commit install
```

## Testing

**ALWAYS run `pytest` before committing.**

```bash
pytest                                              # All tests
pytest tests/basic/test_coder.py                   # Specific file
pytest tests/basic/test_coder.py::TestCoder::test_specific_case  # Specific case
pytest -k "pattern"                                # Keyword match
```

**Config:** `pytest.ini` - Tests in `tests/basic`, `tests/help`, `tests/browser`, `tests/scrape`

## Linting & Code Style

**Pre-commit hooks auto-run on commit. Manual:** `pre-commit run --all-files`

**Style:** PEP 8, 100 char line length, **NO type hints**, isort + Black + flake8 + codespell

```bash
isort --profile black .                  # Sort imports
black --line-length 100 --preview .      # Format code
flake8 --show-source                     # Lint (ignores E203, W503)
codespell                                # Spell check
```

**Run locally:** `aider`, `aider --model gpt-4o`, `aider file1.py file2.py`, `aider --help`

## CI/CD Workflows

**Three workflows on push/PR to `main`:**

1. **Ubuntu Tests** - Python 3.9-3.12 on Ubuntu, runs pytest
2. **Windows Tests** - Python 3.9-3.12 on Windows, runs pytest  
3. **Docker Build** - Builds `aider` and `aider-full` for linux/amd64 and linux/arm64

**All ignore:** `aider/website/**`, `README.md`, `HISTORY.md` (docs don't trigger CI)

## Project Structure

**Root:** `pyproject.toml` (config), `requirements.txt` (deps), `requirements/` (.in files), `.pre-commit-config.yaml`, `.flake8`, `pytest.ini`, `CONTRIBUTING.md`, `README.md`

**Source (`aider/`):** Entry: `main.py`
- `coders/` - 30+ coder strategies (`base_coder.py`, `editblock_coder.py`, `udiff_coder.py`, `wholefile_coder.py`)
- `commands.py` - CLI handlers
- `io.py` - I/O handling
- `repo.py` - Git ops
- `repomap.py` - Repo mapping
- `models.py` - LLM configs
- `llm.py` - LLM interface
- `queries/` - Tree-sitter files
- `website/` - Jekyll docs

**Tests (`tests/`):** `basic/` (24 files), `browser/`, `help/`, `scrape/`, `fixtures/`

**Other:** `scripts/` (pip-compile.sh, update-docs.sh), `benchmark/` (Exercism), `docker/`

## Dependencies

**Managed with pip-tools.** Edit `.in` files, never `.txt` files directly.

**Add dependency:**
1. Edit appropriate `.in` file (main, dev, help, browser, playwright)
2. `pip install pip-tools && ./scripts/pip-compile.sh`
3. Upgrade all: `./scripts/pip-compile.sh --upgrade`
4. Commit both `.in` and `.txt`

## Docker

**Build:** `docker build -t aider -f docker/Dockerfile .`

**Targets:** `aider` (standard+playwright), `aider-full` (all deps)

**Config:** Python 3.10-slim base, system packages (build-essential, git, libportaudio2, pandoc), venv at `/venv`, chromium installed

## Known Issues

1. **pip timeouts:** Use `pip install --timeout=300` or `--no-cache-dir`, retry if needed
2. **Pinned versions** (don't upgrade without testing):
   - `tree-sitter==0.21.3` - v0.22.2 breaks tree-sitter-languages
   - `numpy<2` - sentence-transformers incompatible
   - `tokenizers==0.19.1` - dependency conflicts
   - `importlib-metadata<8.0.0` - GitHub Release action
   - `networkx<3.3`, `scipy<1.14` - Python 3.9 compatibility

## Pre-Commit Checklist

**ALWAYS do before committing:**
```bash
pre-commit run --all-files              # If hooks installed
pytest                                  # Run all tests
black --check --line-length 100 --preview . && flake8 --show-source && isort --profile black --check .
python -c "from aider.main import main; print('OK')"  # Test imports
aider --help                            # If CLI modified
```

## Quick Reference

**Setup:** `python -m venv ../aider_venv && source ../aider_venv/bin/activate && pip install -e . && pip install -r requirements.txt && pip install -r requirements/requirements-dev.txt`

**Test:** `pytest` | **Lint:** `pre-commit run --all-files` | **Run:** `aider --help`

**File Locations:**
- Coder strategy: `aider/coders/` | Commands: `aider/commands.py` | Tests: `tests/basic/`
- CLI args: `aider/args.py` | Deps: `requirements/requirements.in` + `./scripts/pip-compile.sh` | Docs: `aider/website/`

## Critical Notes

1. **Trust these instructions** - only search if info missing/wrong
2. **Always use venv** - wrong environment causes mysterious errors
3. **Test incrementally** - run pytest often
4. **Never edit .txt requirements** - edit .in files, run pip-compile.sh
5. **Docs don't trigger CI** - website/README/HISTORY changes are safe
6. **Python 3.9-3.12 compatibility required**
7. **NO type hints** - project policy
