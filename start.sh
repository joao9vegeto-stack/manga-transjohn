#!/bin/bash

# Quick start script for Manga TransJohn

echo "=== Manga TransJohn Quick Start ==="
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  No .env file found!"
    echo "Creating .env from template..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Edit .env and add your GEMINI_API_KEY"
    echo "Get your API key at: https://makersuite.google.com/app/apikey"
    echo ""
    read -p "Press Enter after you've added your API key to .env..."
fi

# Check if WildWorlds font exists
if [ ! -f backend/fonts/WildWorlds.ttf ]; then
    echo ""
    echo "⚠️  WildWorlds.ttf font not found!"
    echo "Place your WildWorlds.ttf file in backend/fonts/"
    echo ""
    echo "The application will still work with the default font,"
    echo "but results may not look as professional."
    echo ""
    read -p "Press Enter to continue anyway or Ctrl+C to exit and add the font..."
fi

echo ""
echo "Starting Manga TransJohn with Docker Compose..."
echo ""

docker-compose up --build

echo ""
echo "=== Manga TransJohn Stopped ==="
