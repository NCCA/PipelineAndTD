#!/bin/bash

# Enable X11 forwarding for Docker containers
# This script sets up proper X11 permissions and environment

echo "Setting up X11 forwarding for Docker container..."

# Allow connections from local Docker containers
xhost +local:docker 2>/dev/null || xhost +local: 2>/dev/null

# Export display if not set
export DISPLAY=${DISPLAY:-:1}

echo "Using DISPLAY=$DISPLAY"

# Check if .Xauthority exists and is readable
if [ ! -r "$HOME/.Xauthority" ]; then
    echo "Warning: .Xauthority file not found or not readable at $HOME/.Xauthority"
    echo "Creating a new one..."
    touch "$HOME/.Xauthority"
fi

# Set XAUTHORITY if not already set
export XAUTHORITY=${XAUTHORITY:-$HOME/.Xauthority}

echo "Starting container with X11 forwarding enabled..."

# Run docker compose with proper environment
docker compose up -d

echo "Container started. To run the OpenGL application:"
echo "  docker compose exec dev ./OpenGLTriangle.py"
echo ""
echo "To test X11 connectivity first:"
echo "  docker compose exec dev xclock"