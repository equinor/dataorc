FROM mcr.microsoft.com/devcontainers/base:ubuntu-24.04 AS base

# Install uv
# Ref: https://docs.astral.sh/uv/getting-started/installation/
USER vscode
RUN curl --proto '=https' --tlsv1.2 -LsSf https://github.com/astral-sh/uv/releases/download/0.9.0/uv-installer.sh | sh
