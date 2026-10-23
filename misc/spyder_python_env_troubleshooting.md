# Python Environment Troubleshooting: Spyder on Windows and macOS

## 1. What happened on Windows

### Symptom

Running code in Spyder produced:

``` text
ModuleNotFoundError: No module named 'numpy'
```

### Root cause

Spyder was using a different Python environment from the one active in
PowerShell.

-   **Python used by Spyder:**
    `C:\Users\kevin\.conda\envs\spyder-env\python.exe`
-   **PowerShell's active environment (`base`):**
    `C:\Users\kevin\.anaconda-desktop\micromamba\envs\cuda`

Each Python environment has its own installed packages. Installing NumPy
in one environment does not automatically install it in another.

### Windows resolution

1.  In Spyder's IPython Console, identify the interpreter:

    ``` python
    import sys
    print(sys.executable)
    ```

2.  In PowerShell, install packages into that exact environment:

    ``` powershell
    conda install -p "C:\Users\kevin\.conda\envs\spyder-env" numpy pandas matplotlib scikit-learn
    ```

    Approve the installation if prompted.

3.  Restart Spyder's IPython Console, then verify:

    ``` python
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import sklearn

    print("NumPy:", np.__version__)
    print("Pandas:", pd.__version__)
    print("Imports successful!")
    ```

4.  If `conda` cannot manage that environment, use the environment's own
    Python executable to install packages instead. For example:

    ``` powershell
    & "C:\Users\kevin\.conda\envs\spyder-env\python.exe" -m pip install numpy pandas matplotlib scikit-learn
    ```

    Prefer conda for packages available through the environment's
    configured conda channels; use pip when appropriate. Avoid mixing
    package managers unnecessarily.

------------------------------------------------------------------------

## 2. How to troubleshoot the same issue on macOS (Spyder 6)

The key rule is the same on a Mac: **install packages into the Python
environment that runs your code---not automatically into whichever
environment happens to be active in Terminal.**

Because Spyder can be installed in different ways, first determine
whether your Spyder 6 app is a standalone installation or was installed
into a conda environment using conda-forge.

### Step A --- Identify the interpreter Spyder is actually using

In Spyder's IPython Console, run:

``` python
import sys
print(sys.executable)
```

Copy the full path. This is the most important diagnostic step.

You can also check the Python version:

``` python
import sys
print(sys.version)
```

### Step B --- If Spyder is using a conda environment

Open Terminal and list your environments:

``` bash
conda info --envs
```

If the interpreter path from Spyder belongs to one of those
environments, install packages into that environment. For example, if
the environment is named `spyder-env`:

``` bash
conda install -n spyder-env numpy pandas matplotlib scikit-learn
```

If you know the exact environment path, you can target it directly:

``` bash
conda install -p "/full/path/to/the/environment" numpy pandas matplotlib scikit-learn
```

Replace the example name or path with the one that matches Spyder's
`sys.executable`. Do not copy the example path literally.

If you installed Spyder itself into a conda-forge environment, use the
same conda installation that owns that environment.

**If `conda` is not in your PATH**, call it directly using its full path.
For miniforge (the most common setup on modern Macs), that is:

``` bash
~/miniforge3/bin/conda install -n spyder-env numpy pandas matplotlib scikit-learn
```

To avoid doing this every time, initialize conda for your shell once:

``` bash
~/miniforge3/bin/conda init zsh
```

Then restart Terminal. After that, `conda` will be available in every new session.

**Tip — use `mamba` for faster installs:** If you have miniforge, `mamba` is
included and is a drop-in replacement for `conda` that resolves dependencies
much faster. Just swap the command:

``` bash
mamba install -n spyder-env numpy pandas matplotlib scikit-learn
```

### Step C --- If Spyder 6 is the standalone app

A standalone Spyder app may use its own runtime to launch the
application, while running your code with a separate Python environment.
Installing packages into an unrelated conda environment will not fix
imports in the active console.

1.  First run `sys.executable` in Spyder to see which interpreter runs
    your code.
2.  If it points to a conda environment, install the packages into that
    exact environment using Step B.
3.  If you want Spyder to use a different conda environment, create or
    choose that environment and make sure it has a compatible
    `spyder-kernels` package.
4.  In Spyder, open **Preferences/Settings → Python interpreter**
    (wording may vary by version), choose the option to use a specific
    Python interpreter, and select that environment's Python executable.
5.  Apply the change and restart the IPython Console. If Spyder reports
    that `spyder-kernels` is missing or incompatible, follow the exact
    version guidance shown by Spyder and install the compatible version
    into the target environment.

For a typical conda environment, its Python executable is always at:

```
<conda-base>/envs/<environment-name>/bin/python
```

The format is the same on Apple Silicon and Intel Macs. What differs is
where the conda base directory lives, which depends on how conda was installed:

| Installation | Typical base path |
|---|---|
| miniforge | `~/miniforge3/` |
| Anaconda | `~/anaconda3/` or `/opt/anaconda3/` |
| Miniconda | `~/miniconda3/` |

Use the path reported by `sys.executable` or `conda info --envs` rather
than guessing.

### Step D --- Verify the packages

After installing packages and restarting the console, run:

``` python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sklearn

print("Python:", __import__("sys").executable)
print("NumPy:", np.__version__)
print("Pandas:", pd.__version__)
print("Imports successful!")
```

If the imports still fail, compare the printed Python path with the
environment where you installed the packages. If they differ, the
packages were installed into the wrong environment.

------------------------------------------------------------------------

## 3. Quick checklist for future `ModuleNotFoundError` issues

1.  **Read the missing module name** in the error message (for example,
    `numpy`).

2.  **Check the active interpreter** in the same app or console that
    raises the error:

    ``` python
    import sys
    print(sys.executable)
    ```

3.  **Identify the matching environment** with `conda info --envs` if it
    is managed by conda.

4.  **Install the package into that environment**, using conda or that
    environment's Python with `-m pip`.

5.  **Restart the IPython Console or kernel** and retry the import.

6.  **Avoid installing another Python distribution as a first fix.**
    Multiple installations can coexist, but they make it easier to
    target the wrong interpreter.

## Main takeaway

**The Python interpreter running your code determines which packages are
available.** Spyder's installation method, the active conda environment
in Terminal, and the interpreter used by Spyder are related but not
necessarily the same thing.
