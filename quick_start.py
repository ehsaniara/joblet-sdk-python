#!/usr/bin/env python3
"""
Quick Start Guide for Joblet SDK

This script provides an interactive guide to get you started with the Joblet SDK.
"""

import subprocess
import sys
from pathlib import Path


def print_header():
    """Print the header."""
    print("🚀 Joblet SDK - Quick Start Guide")
    print("=" * 50)
    print()


def check_requirements():
    """Check system requirements."""
    print("📋 Checking requirements...")

    # Check Python version
    version = sys.version_info
    if version < (3, 8):
        print(f"❌ Python {version.major}.{version.minor} is not supported")
        print("   Please install Python 3.8 or higher")
        return False

    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")

    # Check if we're in the right directory
    if not Path("pyproject.toml").exists():
        print("❌ Not in the Joblet SDK directory")
        print("   Please run this from the joblet-sdk-python directory")
        return False

    print("✅ In correct directory")
    return True


def setup_options():
    """Present setup options to the user."""
    print("\n🛠️  Setup Options:")
    print("1. Full development setup (recommended for contributors)")
    print("2. User installation (pip install)")
    print("3. Quick test with existing installation")
    print("4. Show configuration help")
    print("5. Exit")

    while True:
        try:
            choice = input("\nChoose an option (1-5): ").strip()
            if choice in ["1", "2", "3", "4", "5"]:
                return choice
            else:
                print("Please enter a number between 1 and 5")
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            sys.exit(0)


def run_dev_setup():
    """Run the development setup."""
    print("\n🔧 Running development setup...")
    try:
        result = subprocess.run([sys.executable, "setup_dev.py"], check=True)
        print("✅ Development setup completed!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Development setup failed")
        return False


def run_user_install():
    """Install as a user package."""
    print("\n📦 Installing Joblet SDK...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-e", "."], check=True)
        print("✅ Installation completed!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Installation failed")
        return False


def test_installation():
    """Test the current installation."""
    print("\n🧪 Testing installation...")
    try:
        import joblet

        print(f"✅ Joblet SDK {joblet.__version__} is working!")

        # Test basic import
        from joblet import JobletClient

        print("✅ JobletClient import successful")

        # Show proto info
        try:
            from joblet._proto_generation_info import PROTO_TAG

            print(f"✅ Proto files from version {PROTO_TAG}")
        except ImportError:
            print("⚠️  Proto generation info not available")

        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        print("   Try running option 1 or 2 first")
        return False


def show_config_help():
    """Show configuration help."""
    print("\n⚙️  Configuration Help")
    print("-" * 30)

    config_path = Path.home() / ".rnx" / "rnx-config.yml"
    print(f"Config file location: {config_path}")

    if config_path.exists():
        print("✅ Configuration file exists")
    else:
        print("❌ Configuration file not found")
        print("\nTo create a configuration file:")
        print("1. Run option 1 (development setup)")
        print("2. Or manually create with this content:")
        print()
        print("server:")
        print('  host: "your-server-host"')
        print("  port: 50051")
        print()

    print("You can also pass connection details directly:")
    print("  from joblet import JobletClient")
    print("  client = JobletClient(host='your-host', port=50051)")


def run_demo():
    """Ask user if they want to run a demo."""
    print("\n🎯 Ready to test?")
    response = input("Run demo example? (y/N): ").strip().lower()

    if response in ["y", "yes"]:
        print("\n🚀 Running enhanced demo...")
        try:
            subprocess.run([sys.executable, "examples/demo_with_guidance.py"])
        except KeyboardInterrupt:
            print("\n\n⏹️  Demo interrupted")
        except Exception as e:
            print(f"❌ Demo failed: {e}")


def show_next_steps():
    """Show next steps to the user."""
    print("\n📚 Next Steps:")
    print("=" * 20)
    print("1. Update your config: ~/.rnx/rnx-config.yml")
    print("2. Run examples:")
    print("   - python examples/demo_with_guidance.py")
    print("   - python examples/basic_job.py")
    print("3. Explore the API in your Python code:")
    print("   - from joblet import JobletClient")
    print("4. Development commands (if using dev setup):")
    print("   - make help  # Show all commands")
    print("   - make test  # Run tests")
    print("   - make example  # Run demo")
    print("\n📖 Documentation:")
    print("   - README.md for setup instructions")
    print("   - examples/ directory for code examples")
    print("   - pyproject.toml for project configuration")


def main():
    """Main interactive guide."""
    print_header()

    # Check requirements
    if not check_requirements():
        print("\n❌ Requirements check failed")
        sys.exit(1)

    # Main loop
    while True:
        choice = setup_options()

        if choice == "1":
            if run_dev_setup():
                run_demo()
                break
        elif choice == "2":
            if run_user_install():
                run_demo()
                break
        elif choice == "3":
            if test_installation():
                run_demo()
                break
        elif choice == "4":
            show_config_help()
            continue
        elif choice == "5":
            print("\n👋 Goodbye!")
            sys.exit(0)

    show_next_steps()
    print("\n🎉 Setup complete! Happy coding with Joblet SDK!")


if __name__ == "__main__":
    main()
