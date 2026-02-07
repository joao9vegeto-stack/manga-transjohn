# Quick Reference

## Essential Commands

```bash
# First time setup
cp .env.example .env
nano .env  # Add your GEMINI_API_KEY

# Verify setup
./verify-setup.sh

# Start application
./start.sh
# or
docker-compose up --build

# Stop application
docker-compose down

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Restart services
docker-compose restart
```

## Access Points

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## File Locations

### User Must Provide
- `GEMINI_API_KEY` in `.env`
- `backend/fonts/WildWorlds.ttf` (optional)
- `test-images/*.png` (for testing)

### Generated Data
- `data/uploads/` - Uploaded images
- `data/projects/` - Project JSON files
- `data/inpainted/` - Text-removed images
- `data/output/` - Final translated images

## Common Tasks

### Translate a Manga Page
1. Open http://localhost:3000
2. Upload image (drag-drop/click/paste)
3. Select source language
4. Click "Translate"
5. Edit translations in editor
6. Export final image

### Translate Cover (Avoid Title)
1. Upload cover image
2. Enable "Cover Mode" toggle
3. Translate
4. If title still translated, mark as "Ignore"
5. Click "Re-run Translation"
6. Export

### Edit Translations
1. In editor, click a region
2. Edit text in right panel
3. Click "Save Changes"
4. Use Undo/Redo as needed
5. Toggle visibility on/off
6. Export when done

## Supported Languages

### Source (Input)
- Japanese (ja)
- Korean (ko)
- Chinese Simplified (zh-CN)
- Chinese Traditional (zh-TW)
- English (en)
- Spanish (es)
- French (fr)

### Target (Output)
- Brazilian Portuguese (pt-BR) **ONLY**

## Troubleshooting

### Backend won't start
```bash
# Check logs
docker-compose logs backend

# Common issue: No API key
cat .env | grep GEMINI_API_KEY

# Fix
nano .env  # Add your API key
docker-compose restart backend
```

### Frontend won't connect
```bash
# Check backend is running
curl http://localhost:8000/health

# Restart both
docker-compose restart
```

### Slow translation
- Reduce image size (<2000x2000)
- Use Cover Mode to filter regions
- Check internet connection (Gemini API)

### Bad translations
- Verify source language is correct
- Try re-running translation
- Edit translations manually

## Performance

Typical timing for a manga page with 5-10 regions:
- Detection: 1-3 seconds
- OCR: 2-5 seconds  
- Translation: 5-10 seconds
- Inpainting: 2-5 seconds
- Typesetting: <1 second
- **Total: 10-25 seconds**

## Resources

- Full README: `README.md`
- Testing Guide: `TESTING.md`
- Troubleshooting: `TROUBLESHOOTING.md`
- Contributing: `CONTRIBUTING.md`

## Support

- GitHub Issues: https://github.com/joao9vegeto-stack/manga-transjohn/issues
- Documentation: Check the markdown files in repository root
