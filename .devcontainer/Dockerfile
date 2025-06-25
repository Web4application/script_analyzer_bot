# Base image with Node.js and Python 3
FROM mcr.microsoft.com/vscode/devcontainers/python:3.13-bullseye

# Install Node.js (latest LTS)
RUN curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - && \
    apt-get install -y nodejs

# Install additional Linux deps if needed (git, curl, build-essential)
RUN apt-get update && apt-get install -y git curl build-essential

# Set work directory inside container
WORKDIR /workspace

# Optional: Add a non-root user for better security (handled by VSCode container tools usually)
# RUN useradd -m devuser
# USER devuser

CMD [ "sleep", "infinity" ]
