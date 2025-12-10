# File Uploads and Dependencies

Demonstrates uploading files to jobs and managing Python dependencies.

## What You'll Learn

- Uploading files using helper functions
- Uploading entire directories
- Creating files on-the-fly (no disk writes)
- Installing Python packages at runtime
- Using requirements.txt
- Caching dependencies in volumes
- Using pre-built ML runtimes

## Run

```bash
python main.py
```

## Helper Functions

```python
from joblet import (
    upload_file,        # Upload local file
    upload_string,      # Create file from string
    upload_bytes,       # Create file from bytes
    upload_directory,   # Upload entire directory
    create_directory,   # Create empty directory
)
```

## Key Concepts

### Upload a Script

```python
script = '''#!/usr/bin/env python3
print("Hello from uploaded script!")
'''

job = client.jobs.run_job(
    command="python",
    args=["hello.py"],
    runtime="python-3.11",
    uploads=[
        upload_string(script, "hello.py", mode=0o755)
    ]
)
```

### Upload Multiple Files

```python
job = client.jobs.run_job(
    command="python",
    args=["main.py"],
    runtime="python-3.11",
    uploads=[
        upload_string(main_script, "main.py"),
        upload_string(config_json, "config.json"),
        create_directory("data"),
        upload_string(input_data, "data/input.txt"),
    ]
)
```

### Upload Local Files

```python
job = client.jobs.run_job(
    command="python",
    args=["train.py"],
    runtime="python-3.11-ml",
    uploads=[
        upload_file("./train.py"),
        upload_file("./model.pkl", "models/model.pkl"),
        upload_directory("./data", exclude=["*.pyc", "__pycache__"])
    ]
)
```

### Install Dependencies at Runtime

```python
wrapper = '''#!/bin/bash
pip install --user requests beautifulsoup4
python main.py
'''

job = client.jobs.run_job(
    command="bash",
    args=["run.sh"],
    runtime="python-3.11",
    uploads=[
        upload_string(wrapper, "run.sh", mode=0o755),
        upload_string(script, "main.py"),
    ]
)
```

### Use requirements.txt

```python
requirements = """
requests>=2.28.0
pandas>=2.0.0
"""

wrapper = '''#!/bin/bash
pip install --user -r requirements.txt
python main.py
'''

job = client.jobs.run_job(
    command="bash",
    args=["run.sh"],
    runtime="python-3.11",
    uploads=[
        upload_string(wrapper, "run.sh", mode=0o755),
        upload_string(requirements, "requirements.txt"),
        upload_string(script, "main.py"),
    ]
)
```

### Cache Dependencies in Volume

```python
# First run: Install packages to volume
client.volumes.create_volume("python-packages", size_mb=500)

client.jobs.run_job(
    command="pip",
    args=["install", "--target=/packages", "numpy", "pandas"],
    runtime="python-3.11",
    volumes=["python-packages:/packages"]
)

# Subsequent runs: Use cached packages (instant!)
script = '''
import sys
sys.path.insert(0, "/packages")
import numpy as np
print(np.random.rand(5))
'''

client.jobs.run_job(
    command="python",
    args=["run.py"],
    runtime="python-3.11",
    volumes=["python-packages:/packages"],
    uploads=[upload_string(script, "run.py")]
)
```

### Use Pre-built Runtime

For common packages, use pre-built runtimes (no installation needed):

```python
script = '''
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

# Packages are already installed!
model = LinearRegression()
'''

job = client.jobs.run_job(
    command="python",
    args=["train.py"],
    runtime="python-3.11-ml",  # numpy, pandas, sklearn pre-installed
    uploads=[upload_string(script, "train.py")]
)
```

## Available Runtimes

| Runtime | Pre-installed Packages |
|---------|----------------------|
| `python-3.11` | pip, setuptools, wheel |
| `python-3.11-ml` | numpy, scipy, pandas, scikit-learn, matplotlib |
| `python-3.11-pytorch-cuda` | PyTorch with CUDA support |

## Best Practices

1. **Small scripts**: Use `upload_string()` - no disk I/O
2. **Local files**: Use `upload_file()` with proper paths
3. **Common packages**: Use pre-built runtimes
4. **Custom packages**: Cache in volumes for fast reuse
5. **One-time installs**: `pip install --user` in wrapper script
