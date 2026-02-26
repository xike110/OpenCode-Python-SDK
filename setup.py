"""Setup script for OpenCode SDK (for backward compatibility)."""

from setuptools import find_packages, setup

# Read version from version.py
with open("opencode_sdk/version.py", "r", encoding="utf-8") as f:
    for line in f:
        if line.startswith("__version__"):
            version = line.split("=")[1].strip().strip('"').strip("'")
            break

# Read README
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="opencode-sdk",
    version=version,
    description="Python SDK for OpenCode AI CLI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="OpenCode Team",
    author_email="support@opencode.ai",
    url="https://opencode.ai",
    project_urls={
        "Documentation": "https://opencode.ai/docs",
        "Source": "https://github.com/opencode-ai/opencode",
        "Issues": "https://github.com/opencode-ai/opencode/issues",
    },
    packages=find_packages(exclude=["tests", "tests.*", "examples", "examples.*"]),
    python_requires=">=3.10",
    install_requires=[
        "httpx>=0.27.0",
        "pydantic>=2.0.0",
        "typing-extensions>=4.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "mypy>=1.0.0",
            "responses>=0.23.0",
        ],
        "docs": [
            "sphinx>=6.0.0",
            "sphinx-rtd-theme>=1.2.0",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="opencode ai cli sdk api",
    license="MIT",
)
