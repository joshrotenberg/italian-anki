#!/usr/bin/env python3
"""
install_setuptools.py.

A simple script to install setuptools which provides pkg_resources module
required by isort.
"""
import subprocess  # nosec B404 - Used for installing setuptools
import sys


def main():
    """Install setuptools package."""
    print("Installing setuptools...")
    try:
        # nosec B603 - Command uses only fixed strings and sys.executable
        subprocess.check_call([sys.executable, "-m", "pip", "install", "setuptools>=65.5.0"])
        print("setuptools installed successfully!")
        return 0
    except subprocess.CalledProcessError as e:
        print(f"Error installing setuptools: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
