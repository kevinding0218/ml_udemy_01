# Installing Python Packages

## Which tool to use: pip vs conda

| Situation | Use |
|---|---|
| Pure Python package (Flask, requests, FastAPI) | **pip** |
| Package with native/C dependencies (numpy, scikit-learn, opencv) | **conda** |
| Not sure | Try pip first — it works for most packages |

General rule: conda is better at resolving complex native dependencies. For everything else, pip is simpler and more up to date.

---

## How to install

### With pip (miniforge)

```bash
~/miniforge3/bin/pip install <package-name>
```

### With conda (miniforge)

```bash
~/miniforge3/bin/conda install <package-name>
```

### Inside a specific conda environment

```bash
conda activate your-env-name
pip install <package-name>
```

---

## How to find the right package name

The package name you `import` in code is not always the same as the name you install.

Examples:
| `import` statement | Install name |
|---|---|
| `import sklearn` | `pip install scikit-learn` |
| `import cv2` | `pip install opencv-python` |
| `import PIL` | `pip install Pillow` |
| `import flask` | `pip install flask` |

If you're not sure of the install name, search: `pip install <what you tried to import>` on Google, or check [pypi.org](https://pypi.org).

---

## Verify the install worked

```bash
~/miniforge3/bin/python -c "import <package>; print(<package>.__version__)"
```

Example:
```bash
~/miniforge3/bin/python -c "import flask; print(flask.__version__)"
```

If it prints a version number, the package is installed in the right environment.

---

## If the import still fails after installing

The package was likely installed into a different Python environment than the one your IDE or script is using.

1. Check which Python your script uses:
   ```python
   import sys
   print(sys.executable)
   ```

2. Install into that exact Python:
   ```bash
   /path/from/above -m pip install <package-name>
   ```

See `spyder_python_env_troubleshooting.md` for a full walkthrough of this problem.
