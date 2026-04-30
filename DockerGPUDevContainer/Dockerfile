# NVIDIA opengl driver
FROM nvidia/opengl:1.0-glvnd-devel
# Prevent interactive prompts during package install
ENV DEBIAN_FRONTEND=noninteractive

# System deps
RUN apt-get update && apt-get install -y \
    curl \
    git \
    git-lfs \
    build-essential \
    ca-certificates \
    # X11 / display
    x11-apps \
    xauth \
    libx11-dev \
    libx11-xcb1 \
    # Qt xcb platform plugin deps (required from Qt 6.5+)
    libxcb-cursor0 \
    libxcb1 \
    libxcb-glx0 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-randr0 \
    libxcb-render-util0 \
    libxcb-render0 \
    libxcb-shape0 \
    libxcb-shm0 \
    libxcb-sync1 \
    libxcb-util1 \
    libxcb-xfixes0 \
    libxcb-xinerama0 \
    libxcb-xkb1 \
    libxkbcommon-x11-0 \
    libxkbcommon0 \
    # OpenGL (needed if Qt uses OpenGL backend)
    libgl1 \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libdbus-1-3 \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:/root/.local/bin:$PATH"

# Create working directory
WORKDIR /workspace

# Copy project files if they exist (uv will handle deps)
COPY pyproject.toml* uv.lock* ./

# Install dependencies using uv (syncs from lockfile if present)
RUN uv sync --frozen 2>/dev/null || echo "No lockfile found — run 'uv sync' after mounting your project"

# Default to bash so the devcontainer can attach
CMD ["/bin/bash"]
