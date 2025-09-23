#!/usr/bin/env python3
"""Example of using GPU features with the Joblet Python SDK"""

from joblet import JobletClient


def main():
    """Demonstrate GPU job submission"""
    print("🚀 GPU Job Example with Joblet Python SDK")
    print("=" * 50)

    # Connect to Joblet server
    client = JobletClient(host="192.168.1.161", port=6060, insecure=True)

    try:
        # Example 1: Simple GPU job
        print("\n📋 Example 1: Basic GPU Job")
        response = client.jobs().run_job(
            command="nvidia-smi",
            name="gpu-info-check",
            gpu_count=1,  # Request 1 GPU
            gpu_memory_mb=4096,  # Require at least 4GB GPU memory
            runtime="python-3.11",
        )
        print(f"   Job submitted: {response['job_uuid']}")
        print(f"   Status: {response['status']}")

        # Example 2: Multi-GPU machine learning job
        print("\n📋 Example 2: Multi-GPU Training Job")
        response = client.jobs().run_job(
            command="python",
            args=["train_model.py", "--distributed"],
            name="multi-gpu-training",
            gpu_count=2,  # Request 2 GPUs
            gpu_memory_mb=8192,  # Require at least 8GB GPU memory per GPU
            max_memory=16384,  # 16GB system RAM
            max_cpu=80,  # 80% CPU limit
            runtime="python-3.11-ml",
            environment={"CUDA_VISIBLE_DEVICES": "0,1", "NCCL_DEBUG": "INFO"},
        )
        print(f"   Job submitted: {response['job_uuid']}")
        print(f"   Status: {response['status']}")

        # Example 3: Check job status to see GPU allocation
        print("\n📋 Example 3: Check GPU Job Status")
        job_uuid = response["job_uuid"]
        status = client.jobs().get_job_status(job_uuid)

        print(f"   Job: {status['name']}")
        print(f"   Status: {status['status']}")
        print(f"   GPU Count: {status['gpu_count']}")
        print(f"   GPU Memory: {status['gpu_memory_mb']} MB")
        print(f"   Allocated GPUs: {status['gpu_indices']}")

        # Example 4: GPU-enabled workflow
        print("\n📋 Example 4: GPU Workflow")
        workflow_yaml = """
name: gpu-ml-pipeline
jobs:
  preprocess:
    command: python
    args: ["preprocess.py"]
    runtime: python-3.11
    max_memory: 4096

  train:
    command: python
    args: ["train.py", "--epochs", "10"]
    runtime: python-3.11-ml
    gpu_count: 1
    gpu_memory_mb: 6144
    depends_on: [preprocess]
    max_memory: 8192

  evaluate:
    command: python
    args: ["evaluate.py"]
    runtime: python-3.11-ml
    gpu_count: 1
    gpu_memory_mb: 4096
    depends_on: [train]
"""

        workflow_response = client.jobs().run_workflow(
            workflow="gpu-ml-pipeline.yaml", yaml_content=workflow_yaml
        )
        print(f"   Workflow submitted: {workflow_response['workflow_uuid']}")
        print(f"   Status: {workflow_response['status']}")

    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nNote: This example requires a running Joblet server with GPU support.")
        print("Make sure the server has GPUs available and GPU manager is enabled.")

    finally:
        client.close()

    print("\n✅ GPU Examples Complete!")
    print("\n📚 Key Features Demonstrated:")
    print("   • GPU resource allocation (gpu_count)")
    print("   • GPU memory requirements (gpu_memory_mb)")
    print("   • Multi-GPU job scheduling")
    print("   • GPU status monitoring (gpu_indices)")
    print("   • GPU-enabled workflows")


if __name__ == "__main__":
    main()
