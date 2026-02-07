#!/bin/bash

# Setup verification script for Manga TransJohn

echo "=== Manga TransJohn Setup Verification ==="
echo ""

ERRORS=0
WARNINGS=0

# Check 1: .env file
echo "✓ Checking .env file..."
if [ -f .env ]; then
    if grep -q "GEMINI_API_KEY=your_gemini_api_key_here" .env; then
        echo "  ⚠️  WARNING: .env file exists but contains placeholder API key"
        echo "     Edit .env and add your real GEMINI_API_KEY"
        WARNINGS=$((WARNINGS+1))
    else
        echo "  ✓ .env file found with API key"
    fi
else
    echo "  ❌ ERROR: .env file not found"
    echo "     Run: cp .env.example .env"
    echo "     Then edit .env and add your GEMINI_API_KEY"
    ERRORS=$((ERRORS+1))
fi
echo ""

# Check 2: Docker
echo "✓ Checking Docker..."
if command -v docker &> /dev/null; then
    echo "  ✓ Docker installed: $(docker --version)"
else
    echo "  ❌ ERROR: Docker not found"
    echo "     Install Docker from: https://docs.docker.com/get-docker/"
    ERRORS=$((ERRORS+1))
fi
echo ""

# Check 3: Docker Compose
echo "✓ Checking Docker Compose..."
if command -v docker-compose &> /dev/null; then
    echo "  ✓ Docker Compose installed: $(docker-compose --version)"
else
    echo "  ❌ ERROR: Docker Compose not found"
    echo "     Install Docker Compose from: https://docs.docker.com/compose/install/"
    ERRORS=$((ERRORS+1))
fi
echo ""

# Check 4: WildWorlds Font
echo "✓ Checking WildWorlds font..."
if [ -f backend/fonts/WildWorlds.ttf ]; then
    echo "  ✓ WildWorlds.ttf found"
else
    echo "  ⚠️  WARNING: WildWorlds.ttf not found in backend/fonts/"
    echo "     The app will work but use default font"
    echo "     For best results, add WildWorlds.ttf to backend/fonts/"
    WARNINGS=$((WARNINGS+1))
fi
echo ""

# Check 5: Test Images
echo "✓ Checking test images..."
IMAGE_COUNT=$(find test-images -type f \( -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" \) 2>/dev/null | wc -l)
if [ $IMAGE_COUNT -gt 0 ]; then
    echo "  ✓ Found $IMAGE_COUNT test image(s)"
else
    echo "  ⚠️  WARNING: No test images found in test-images/"
    echo "     Add some manga images to test the application"
    WARNINGS=$((WARNINGS+1))
fi
echo ""

# Check 6: Port Availability
echo "✓ Checking port availability..."
if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "  ⚠️  WARNING: Port 3000 is in use"
    echo "     The frontend may fail to start"
    WARNINGS=$((WARNINGS+1))
else
    echo "  ✓ Port 3000 available"
fi

if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "  ⚠️  WARNING: Port 8000 is in use"
    echo "     The backend may fail to start"
    WARNINGS=$((WARNINGS+1))
else
    echo "  ✓ Port 8000 available"
fi
echo ""

# Summary
echo "=== Verification Summary ==="
echo ""
if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo "✓ All checks passed! You're ready to run:"
    echo "  ./start.sh"
    echo "  or"
    echo "  docker-compose up --build"
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo "⚠️  $WARNINGS warning(s) found, but you can proceed"
    echo "  Run: ./start.sh"
    exit 0
else
    echo "❌ $ERRORS error(s) found. Please fix them before running."
    echo ""
    echo "Quick fix commands:"
    echo "  cp .env.example .env"
    echo "  nano .env  # Add your GEMINI_API_KEY"
    exit 1
fi
