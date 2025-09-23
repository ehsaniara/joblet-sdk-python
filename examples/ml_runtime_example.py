#!/usr/bin/env python3
"""Example of running a job with python-3.11-ml runtime."""

import time

from joblet import JobletClient


def main():
    # Uses config from ~/.rnx/rnx-config.yml by default
    # The server requires TLS certificates (self-signed with OpenSSL)
    with JobletClient(insecure=False) as client:
        print(f"Connecting to {client.host}:{client.port}")
        if not client.health_check():
            print("Server not available")
            return

        print("Server is available!")

        # Python script that demonstrates ML libraries
        python_script = """
import sys
print(f"Python version: {sys.version}")
print("\\nInstalled ML packages:")

try:
    import numpy as np
    print(f"- NumPy {np.__version__}")

    # Create a simple array and do some operations
    arr = np.array([1, 2, 3, 4, 5])
    print(f"  Array: {arr}")
    print(f"  Mean: {np.mean(arr)}")
    print(f"  Sum: {np.sum(arr)}")
except ImportError as e:
    print(f"- NumPy: Not available ({e})")

try:
    import pandas as pd
    print(f"- Pandas {pd.__version__}")

    # Create a simple DataFrame
    df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
    print("  Sample DataFrame:")
    print(df.to_string(index=False))
except ImportError as e:
    print(f"- Pandas: Not available ({e})")

try:
    import sklearn
    print(f"- Scikit-learn {sklearn.__version__}")

    # Simple linear regression example
    from sklearn.linear_model import LinearRegression
    X = [[1], [2], [3], [4]]
    y = [2, 4, 6, 8]
    model = LinearRegression().fit(X, y)
    print(f"  Linear regression prediction for [5]: {model.predict([[5]])[0]:.1f}")
except ImportError as e:
    print(f"- Scikit-learn: Not available ({e})")

try:
    import matplotlib
    print(f"- Matplotlib {matplotlib.__version__}")
except ImportError as e:
    print(f"- Matplotlib: Not available ({e})")

try:
    import torch
    print(f"- PyTorch {torch.__version__}")

    # Simple tensor operations
    tensor = torch.tensor([1.0, 2.0, 3.0])
    print(f"  Tensor: {tensor}")
    print(f"  Tensor sum: {torch.sum(tensor).item()}")
except ImportError as e:
    print(f"- PyTorch: Not available ({e})")

print("\\nML runtime demonstration completed!")
"""

        # Run the job with python-3.11-ml runtime
        job = client.jobs.run_job(
            command="python3",
            args=["-c", python_script],
            name="ml-runtime-demo",
            runtime="python-3.11-ml",  # Specify the ML runtime
        )

        print(f"Job started: {job['job_uuid']}")
        print("Waiting for completion...\n")

        # Wait for completion
        while True:
            status = client.jobs.get_job_status(job["job_uuid"])
            print(f"Status: {status['status']}")

            if status["status"].lower() in ["completed", "failed"]:
                break
            time.sleep(1)

        # Show logs
        logs = b"".join(client.jobs.get_job_logs(job["job_uuid"]))
        print(f"\nOutput:\n")
        print(f"{logs.decode()}")

        # Get final job status
        final_status = client.jobs.get_job_status(job["job_uuid"])
        print(f"\nFinal job status: {final_status['status']}")

        if final_status["exit_code"] is not None:
            print(f"Exit code: {final_status['exit_code']}")


if __name__ == "__main__":
    main()
