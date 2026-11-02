# Python Environment Management with Conda

## Current state (as of setup)

| | Mac | Status |
|---|---|---|
| Conda distribution | Miniforge3 at `/Users/rading/miniforge3` | ✅ |
| `base` environment | Python 3.14.7 | ✅ |
| `ml` environment | Python 3.14 | ✅ created |
| `dev` environment | Python 3.10 | ⬜ to do |
| python.org Pythons (3.11, 3.12, 3.13) | Removed from `/Library/Frameworks/` | ✅ |
| `~/.bash_profile` | Cleaned up, `conda activate ml` on startup | ✅ |

**Platform:** Apple Silicon (osx-arm64) — important for choosing correct packages
**Channel:** conda-forge (better than the default Anaconda channel for ML on Apple Silicon)

---

## The golden rule: never install packages into base

`base` is conda's system environment. If you break it by installing conflicting
packages, conda itself can stop working. Treat it as read-only.

```
base        ← conda lives here. Do not touch.
ml          ← Python 3.14, PyTorch, transformers, numpy, etc.
dev         ← Python 3.10, general scripting, web tools, etc.
```

This rule applies identically on Mac and Windows.

---

## Step 1 — Create both environments

**Mac / Linux**
```bash
conda create -n ml python=3.14       # ✅ done
conda create -n dev python=3.10      # ⬜ run this next
```

**Windows (Command Prompt or Anaconda Prompt)**
```cmd
conda create -n ml python=3.14
conda create -n dev python=3.10
```

> The conda commands themselves are identical on Mac and Windows.
> The difference is which terminal you type them in (see Step 8).

---

## Step 2 — Install packages into ml

**Mac / Windows — same command**
```bash
conda activate ml
pip install torch torchvision transformers numpy pandas scikit-learn matplotlib jupyter pillow requests flask
```

Verify:
```bash
python --version                                    # → Python 3.14.x
python -c "import torch; print(torch.__version__)"
```

> **Why pip inside conda?** Some packages (torch, transformers) have better/faster wheels
> on PyPI than on conda-forge. It is fine to mix — just always install conda packages
> first, then pip packages on top.

---

## Step 3 — Install packages into dev

For `officialDpSpark` (`/Users/rading/Development/ebay/collectibles/officialDpSpark`):

**Mac / Windows — same command**
```bash
conda activate dev
pip install pyspark requests urllib3 pytz pylint mypy
```

> **Note:** the repo README says `pytlint` — that is a typo, the real package is `pylint`.
> `pyspark` is the local Spark client; the actual Spark cluster runs in Data Lake Studio, not locally.

---

## Step 4 — Daily usage

**Mac / Linux**
```bash
conda activate ml          # switch to ML work
conda activate dev         # switch to dev work
conda deactivate           # back to base
conda env list             # see all environments
pip list                   # packages in active env
which python               # show which Python is active
```

**Windows**
```cmd
conda activate ml
conda activate dev
conda deactivate
conda env list
pip list
where python               # ← "where" instead of "which" on Windows
```

---

## Step 5 — Set ml as default on new terminal

### Mac

Add one line to `~/.bash_profile` (already done):
```bash
conda activate ml
```
Every new terminal opens in `ml` automatically.

To check or edit:
```bash
open ~/.bash_profile        # opens in TextEdit
# or
code ~/.bash_profile        # opens in VS Code
```

### Windows

Conda on Windows auto-activates `base` by default. To auto-activate `ml` instead:

**Option A — set via conda config (recommended):**
```cmd
conda config --set auto_activate_base false
```
Then add `conda activate ml` to your PowerShell profile:
```powershell
# Open your PowerShell profile in Notepad
notepad $PROFILE

# Add this line at the bottom:
conda activate ml
```
If the profile file doesn't exist yet:
```powershell
New-Item -Path $PROFILE -Type File -Force
```

**Option B — Anaconda Prompt shortcut:**
Right-click the Anaconda Prompt shortcut → Properties → change the Target to:
```
%windir%\system32\cmd.exe /K "conda activate ml"
```

---

## Step 6 — Configure Spyder

**Current setup (Mac):** Spyder is installed as a standalone app with its own bundled
**Python 3.11** at `/Users/rading/Library/spyder-6/`. It is completely independent —
deleting the python.org frameworks had no effect on it.

To make Spyder use your `ml` conda environment instead of its bundled Python:

### Option A: Install Spyder inside ml (recommended)

**Mac / Windows — same**
```bash
conda activate ml
conda install spyder
spyder          # launches using ml's Python — sees all ML packages automatically
```

### Option B: Connect standalone Spyder to ml via spyder-kernels

```bash
# Inside the ml environment
conda activate ml
conda install spyder-kernels

# Then in Spyder:
# Preferences → Python interpreter → Use the following interpreter
```

| | Path to paste into Spyder |
|---|---|
| Mac | `/Users/rading/miniforge3/envs/ml/bin/python` |
| Windows | `C:\Users\<you>\miniconda3\envs\ml\python.exe` |

To find the exact path in your active environment:

**Mac**
```bash
conda activate ml && which python
```
**Windows**
```cmd
conda activate ml && where python
```

---

## Step 7 — Configure IntelliJ / PyCharm

IntelliJ sets a Python interpreter **per project** — set `ml` for ML projects, `dev` for Spark/scripting projects.

1. Open project → **File → Project Structure** (or **PyCharm → Preferences → Project → Python Interpreter**)
2. Click **+** → **Add Python SDK** → **Conda Environment** → **Existing environment**
3. Browse to the Python binary:

| Environment | Mac path | Windows path |
|-------------|----------|--------------|
| `ml` (Python 3.14) | `/Users/rading/miniforge3/envs/ml/bin/python` | `C:\Users\<you>\miniconda3\envs\ml\python.exe` |
| `dev` (Python 3.10) | `/Users/rading/miniforge3/envs/dev/bin/python` | `C:\Users\<you>\miniconda3\envs\dev\python.exe` |
| `base` (Python 3.14) | `/Users/rading/miniforge3/bin/python` | `C:\Users\<you>\miniconda3\python.exe` |

**Project assignments:**
- `card-similarity-search` → `ml`
- `officialDpSpark` → `dev`

---

## Step 8 — Migrate card-similarity-search to the ml environment

The project currently has its own `.venv` folder. Once `ml` has the right packages,
point the project at `ml` and remove `.venv` to stop duplicating torch (~2GB).

**Mac**
```bash
conda activate ml
pip install -r card-similarity-search/requirements.txt
# Switch interpreter in IntelliJ to ml, then:
rm -rf card-similarity-search/.venv
```

**Windows**
```cmd
conda activate ml
pip install -r card-similarity-search\requirements.txt
rem Switch interpreter in IntelliJ to ml, then:
rmdir /s /q card-similarity-search\.venv
```

---

## Quick reference

| Task | Mac / Linux | Windows |
|------|-------------|---------|
| Create environment | `conda create -n <name> python=<ver>` | same |
| Activate | `conda activate <name>` | same |
| Deactivate | `conda deactivate` | same |
| List environments | `conda env list` | same |
| List packages | `conda list` or `pip list` | same |
| Find Python location | `which python` | `where python` |
| Delete environment | `conda remove -n <name> --all` | same |
| Export to file | `conda env export > environment.yml` | same |
| Recreate from file | `conda env create -f environment.yml` | same |
| Update conda | `conda update conda` | same |
| Open shell profile | `open ~/.bash_profile` | `notepad $PROFILE` (PowerShell) |

---

## Environment path reference

| Environment | Python version | Mac path | Windows path |
|-------------|---------------|----------|--------------|
| `base` | 3.14 | `/Users/rading/miniforge3/bin/python` | `C:\Users\<you>\miniforge3\python.exe` |
| `ml` | 3.14 | `/Users/rading/miniforge3/envs/ml/bin/python` | `C:\Users\<you>\miniforge3\envs\ml\python.exe` |
| `dev` | 3.10 | `/Users/rading/miniforge3/envs/dev/bin/python` | `C:\Users\<you>\miniforge3\envs\dev\python.exe` |
| Spyder (standalone) | 3.11 | `/Users/rading/Library/spyder-6/bin/python3.11` | `C:\Users\<you>\AppData\Local\spyder-6\python.exe` |

---

## Why Miniforge over Anaconda

| | Anaconda | Miniforge |
|---|---|---|
| Default channel | `defaults` (Anaconda Inc.) | `conda-forge` (community) |
| Apple Silicon support | Slower, some packages use Rosetta | Full native ARM64 |
| Size | ~3GB installed | ~200MB installed |
| License | Restricted for commercial use | Fully open source |
| Windows support | Full | Full |

**Installing Miniforge on Windows:**
Download the `.exe` installer from https://github.com/conda-forge/miniforge/releases
and run it. Default install path: `C:\Users\<you>\miniforge3\`
During install, check **"Add Miniforge3 to my PATH"** or use the Anaconda Prompt shortcut it creates.
