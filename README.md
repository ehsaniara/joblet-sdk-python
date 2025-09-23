# Joblet Python SDK

The official Python SDK for [Joblet](https://github.com/ehsaniara/joblet) - a powerful distributed job orchestration system.

With this SDK, you can easily run jobs, manage complex workflows, and interact with Joblet servers directly from your Python applications. No need to worry about gRPC complexities or protocol details - we've got you covered!

## Quick Start

**Never used Joblet before?** No worries! Run our interactive guide:
```bash
python quick_start.py
```

**Already know what you're doing?** Jump straight into development:
```bash
python setup_dev.py
```

## Installation

### For most users (recommended)
The easiest way is to install from PyPI:
```bash
pip install joblet-sdk
```

Or add to your `requirements.txt`:
```txt
joblet-sdk>=0.1.0
```

### For latest development features
Install directly from GitHub:
```bash
pip install git+https://github.com/ehsaniara/joblet-sdk-python.git
```

### For contributors
Clone the repo and let our setup script do the heavy lifting:
```bash
git clone https://github.com/ehsaniara/joblet-sdk-python.git
cd joblet-sdk-python
python setup_dev.py  # This handles everything for you!
```

## Basic Usage

Here's how to run your first job - it's really that simple:

```python
from joblet import JobletClient

# Connect using TLS certificates from ~/.rnx/rnx-config.yml
with JobletClient(insecure=False) as client:
    job = client.jobs.run_job(
        command="echo",
        args=["Hello, Joblet!"],
        name="my-first-job"
    )
    print(f"🎉 Job started! ID: {job['job_uuid']}")
```

### Setting up Configuration

You'll need to tell the SDK where your Joblet server is and provide TLS certificates. Create a config file at `~/.rnx/rnx-config.yml`:

```yaml
version: "3.0"

nodes:
  default:
    address: "your-joblet-server:50051"  # Replace with your server address
    cert: |
      -----BEGIN CERTIFICATE-----
      # Your client certificate here (provided by your Joblet admin)
      -----END CERTIFICATE-----
    key: |
      -----BEGIN PRIVATE KEY-----
      # Your client private key here (provided by your Joblet admin)
      -----END PRIVATE KEY-----
    ca: |
      -----BEGIN CERTIFICATE-----
      # Your CA certificate here (provided by your Joblet admin)
      -----END CERTIFICATE-----
```

> **Note:** Your Joblet administrator will provide you with the necessary certificates. Joblet uses self-signed certificates created with OpenSSL for security.

### Or Configure Directly in Code

Don't like config files? No problem! You can set everything up directly:

```python
from joblet import JobletClient

client = JobletClient(
    host="your-joblet-server.com",
    port=50051,
    ca_cert_path="ca.pem",      # Optional: for SSL
    client_cert_path="client.pem",  # Optional: for client auth
    client_key_path="client.key"    # Optional: for client auth
)
```

## What Can You Do?

Once you've got a client connected, you can access all the cool Joblet features:

- **`client.jobs`** - The bread and butter! Run single jobs or complex workflows
- **`client.networks`** - Set up isolated networks for your jobs
- **`client.volumes`** - Create persistent storage that survives job restarts
- **`client.monitoring`** - Keep an eye on system health and performance
- **`client.runtimes`** - Manage different execution environments

## Try It Out!

Want to see it in action? We've got examples ready to go:

**Start with the interactive demo** (it'll guide you through everything):
```bash
python examples/demo_with_guidance.py
```

**Or jump straight to the basics**:
```bash
python examples/basic_job.py
```

Both examples will show you helpful error messages if something goes wrong - no cryptic failures here!

## Development

### Getting Started with Development

Want to hack on the SDK? We've made it super easy:

```bash
# The lazy way (our favorite!)
python setup_dev.py

# Or if you like doing things manually:
pip install -e .[dev]
python scripts/generate_proto.py  # Get the latest proto files
```

### Handy Development Commands

We've got a Makefile full of useful shortcuts:
```bash
make help          # See what's available
make setup         # Set everything up
make test          # Run the test suite
make format        # Make your code pretty
make lint          # Check for issues
make example       # Try out the demo
```

### Protocol Buffer Magic

Don't worry about gRPC version headaches - we handle that automatically:
```bash
# Refresh proto files for your gRPC version
python scripts/generate_proto.py

# See what versions are available
python scripts/generate_proto.py --list-tags

# Pin to a specific version
python scripts/generate_proto.py --version v1.0.1
```

## Testing

Make sure everything works before you ship:

```bash
make test          # The basics
make test-cov      # With coverage reports
make quick-test    # Fast feedback loop
```

## When Things Go Wrong

Don't panic! Here are the most common issues and how to fix them:

### "Can't connect to server"
- Is your Joblet server actually running?
- Double-check the host and port in your config
- Firewall blocking the connection?

### "SSL/TLS certificate errors"
- Joblet servers require TLS with self-signed certificates (created with OpenSSL)
- Make sure your certificates are properly formatted in the config file
- Ensure there are no extra spaces or line breaks in the certificate blocks
- The SDK uses `insecure=False` by default to work with self-signed certificates

### "gRPC version conflicts"
- Run `python scripts/generate_proto.py --force` to regenerate everything
- This fixes most weird import errors too

### "Import errors" or "Module not found"
- Run `python setup_dev.py` to reset your development environment
- Make sure you're using Python 3.8 or newer
- Still broken? Try a clean reinstall: `pip uninstall joblet-sdk && pip install -e .`

### Still Stuck?
- Try our interactive guide: `python quick_start.py`
- Check the examples in the `examples/` folder
- Run `python examples/demo_with_guidance.py` for detailed troubleshooting

## Contributing

Found a bug? Want to add a feature? Awesome! Here's how to get involved:

1. **Fork** this repository (there's a button for that on GitHub)
2. **Create a branch** for your changes: `git checkout -b my-cool-feature`
3. **Set up your environment**: `python setup_dev.py` (this will handle everything)
4. **Make your changes** and add tests (future you will thank you)
5. **Check everything works**: `make pre-commit` (catches issues before review)
6. **Submit a pull request** and tell us what you've built!

We're friendly and happy to help if you get stuck. This is a welcoming project! 🎉

## What is Joblet?

[Joblet](https://github.com/ehsaniara/joblet) is like having a super-powered task runner that works across multiple machines. Think of it as cron on steroids with a modern API.

Here's what makes it cool:

- **Run anything, anywhere**: Execute commands and scripts across your entire infrastructure
- **Smart workflows**: Chain jobs together with dependencies (job B runs only after job A succeeds)
- **Scales up and down**: Start small, grow big - Joblet handles the complexity
- **Real-time monitoring**: See what's running, what failed, and why
- **Security first**: Everything is encrypted and authenticated

This Python SDK is your friendly gateway to all that power. No need to learn gRPC or mess with protocol buffers - just import and go!

## The Joblet Family

- **[Joblet Server](https://github.com/ehsaniara/joblet)** - The main orchestration engine (start here!)
- **[Joblet Protocol](https://github.com/ehsaniara/joblet-proto)** - The underlying API definitions (for the curious)

## License

MIT License - see LICENSE file for details.