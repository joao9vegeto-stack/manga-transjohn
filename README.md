# Manga TransJohn

Self-hosted web application for translating manga/manhwa images to Brazilian Portuguese (pt-BR).

## Features

- **Complete Translation Pipeline**: Text detection → OCR → Translation → Inpainting → Typesetting
- **Gemini 2.5 Flash Translation**: Uses Google's Gemini 2.5 Flash for high-quality manga translation
- **Interactive Editor**: Edit, delete, and manage translations with a Torii-like interface
- **Cover Mode**: Automatically filters out large stylized text (titles/logos)
- **Batch Processing**: Process multiple images efficiently
- **Local-Only Storage**: All data stays on your machine
- **WildWorlds Font**: Professional manga font for typesetting
- **Export Options**: Export final images and project JSON files

## Architecture

### Backend (Python FastAPI)
- **Text Detection**: PaddleOCR detector
- **OCR**: PaddleOCR recognition engine
- **Translation**: Google Gemini 2.5 Flash (pt-BR only)
- **Inpainting**: OpenCV Telea inpainting
- **Typesetting**: PIL with WildWorlds font
- **Storage**: Local filesystem + SQLite

### Frontend (Next.js + TypeScript)
- **UI Framework**: Next.js 14 with React 18
- **Styling**: TailwindCSS
- **Canvas**: HTML5 Canvas for image editing
- **State Management**: React hooks

## Prerequisites

- Docker and Docker Compose
- Google Gemini API Key ([Get one here](https://makersuite.google.com/app/apikey))
- WildWorlds.ttf font file (see Font Setup section)

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/joao9vegeto-stack/manga-transjohn.git
cd manga-transjohn
```

### 2. Setup Gemini API Key

Create a `.env` file in the project root:

```bash
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

**IMPORTANT**: Never commit your API key to version control!

### 3. Setup WildWorlds Font

Place your `WildWorlds.ttf` font file in the `backend/fonts/` directory:

```bash
mkdir -p backend/fonts
# Copy your WildWorlds.ttf to backend/fonts/WildWorlds.ttf
```

If you don't have the WildWorlds font, the application will fall back to the system default font.

### 4. Run with Docker Compose

```bash
docker-compose up --build
```

The application will be available at:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Manual Setup (Without Docker)

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p data/uploads data/projects data/inpainted data/output fonts

# Set environment variable
export GEMINI_API_KEY=your_api_key_here

# Run the server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Set backend URL (optional, defaults to localhost:8000)
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Run development server
npm run dev

# Or build for production
npm run build
npm start
```

## Usage Guide

### Basic Translation Workflow

1. **Upload Image**
   - Visit http://localhost:3000
   - Drag and drop a manga page image, or click to select, or paste (Ctrl+V)
   - Select source language (Japanese, Korean, Chinese, English, Spanish, French)
   - Toggle "Cover Mode" if translating a cover page
   - Click "Translate"

2. **Wait for Processing**
   - The pipeline will automatically:
     - Detect text regions
     - Extract text with OCR
     - Translate to Brazilian Portuguese
     - Inpaint original text
     - Typeset translations

3. **Edit in Editor**
   - View all detected regions in the right panel
   - Click a region to select it
   - Edit the translated text
   - Toggle visibility with "Show Translation" checkbox
   - Mark regions to ignore and re-run translation
   - Delete unwanted regions
   - Use Undo/Redo for changes

4. **Export**
   - Click "Export Image" to download the final PNG
   - Click "Export Project JSON" to save project data for later

### Advanced Features

#### Cover Mode
When enabled, filters out very large text regions that are likely titles or logos. Useful for manga covers where you want to translate dialogue but not the title.

#### Ignore List
Mark specific regions as "ignored" and click "Re-run Translation" to reprocess the image without those regions. Useful for removing false detections.

#### Eraser Tool
(TODO: Full implementation) - Click the Eraser tool to manually remove translation overlays.

#### Add Region Tool
(TODO: Full implementation) - Draw a rectangle to manually add a text region.

## Testing

### Sample Test Scenarios

#### Scenario 1: Translate a Manga Page
1. Upload a manga page with dialogue bubbles
2. Set source language to Japanese
3. Leave Cover Mode OFF
4. Translate and verify all dialogue is detected and translated
5. Edit any translations that need adjustment
6. Export the final image

#### Scenario 2: Translate a Cover Page
1. Upload a manga cover image
2. Set source language to Japanese
3. Enable Cover Mode
4. Translate and verify that:
   - Large title text is ignored
   - Smaller text (subtitles, taglines) is translated
5. Manually mark the title region as "ignored" if it was detected
6. Delete the title translation while keeping other text
7. Export

## Configuration

### Supported Source Languages

- Japanese (ja)
- Korean (ko)
- Chinese Simplified (zh-CN)
- Chinese Traditional (zh-TW)
- English (en)
- Spanish (es)
- French (fr)

**Target language is fixed to Brazilian Portuguese (pt-BR)**

### Gemini Translation Prompt

The default prompt is optimized for manga translation:
- Translates naturally to Brazilian Portuguese
- Preserves honorifics when culturally relevant
- Handles onomatopoeia appropriately
- Keeps text concise for speech bubbles
- Maintains tone and emotional context

### Font Configuration

The application uses WildWorlds font exclusively for all typesetting. The font is:
- Fixed and cannot be changed through the UI
- Applied with dynamic sizing to fit regions
- Rendered with black outline for readability

## API Documentation

Once the backend is running, visit http://localhost:8000/docs for interactive API documentation.

Key endpoints:
- `POST /upload` - Upload an image
- `POST /pipeline` - Run the complete translation pipeline
- `POST /detect` - Detect text regions only
- `POST /ocr` - Extract text from regions
- `POST /translate` - Translate texts
- `POST /inpaint` - Inpaint text regions
- `POST /typeset` - Render translations
- `GET /project/{id}` - Retrieve project data
- `POST /project/update` - Update project with edits
- `GET /image/{id}` - Get image (original/inpainted/output)

## Troubleshooting

### Backend Issues

**PaddleOCR fails to initialize**
- Ensure you have enough RAM (at least 4GB recommended)
- Check that OpenCV dependencies are installed
- Try rebuilding the Docker container

**Gemini API errors**
- Verify your API key is set correctly
- Check API quotas at https://makersuite.google.com
- Ensure you have Gemini API access enabled

**Inpainting produces artifacts**
- This is expected with OpenCV inpainting
- For better quality, consider implementing LaMa inpainting (requires additional setup)

### Frontend Issues

**Images not loading**
- Check that backend is running on port 8000
- Verify CORS settings in backend
- Check browser console for errors

**Translation not working**
- Verify Gemini API key is set
- Check backend logs for errors
- Ensure source language is supported

**Canvas not rendering**
- Ensure browser supports HTML5 Canvas
- Check for JavaScript errors in console
- Try a different browser (Chrome/Firefox recommended)

## Development

### Project Structure

```
manga-transjohn/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── services/            # Backend services
│   │   ├── detector.py      # Text detection
│   │   ├── ocr.py          # OCR service
│   │   ├── translator.py   # Gemini translation
│   │   ├── inpainter.py    # Image inpainting
│   │   ├── typesetter.py   # Text rendering
│   │   └── storage.py      # Data storage
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── app/            # Next.js pages
│   │   ├── components/     # React components
│   │   ├── lib/           # API client & utilities
│   │   └── types/         # TypeScript types
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

### Adding New Features

1. **New Language Support**: Add language code to LANGUAGES array in frontend and translator service
2. **Custom Fonts**: Add TTF files to backend/fonts/ and update typesetter service
3. **Better Inpainting**: Replace OpenCV inpainting with LaMa or other advanced models
4. **Batch Processing UI**: Extend frontend to handle multiple images

## Security Notes

- **API Key**: Never commit GEMINI_API_KEY to git. Use environment variables.
- **Rate Limiting**: Backend has built-in rate limiting to prevent abuse
- **Local Only**: No external database or cloud storage is used
- **CORS**: Configured for localhost only in development

## Performance

- **Detection**: ~1-3 seconds per image
- **OCR**: ~0.5-1 second per region
- **Translation**: ~1-2 seconds per text (depends on Gemini API)
- **Inpainting**: ~2-5 seconds per image
- **Typesetting**: <1 second

Total pipeline: ~10-20 seconds for a typical manga page with 5-10 text regions.

## License

This project is provided as-is for personal use. Please ensure you have the rights to translate any manga you process.

## Credits

- **PaddleOCR**: Text detection and OCR
- **Google Gemini**: Translation engine
- **OpenCV**: Image processing and inpainting
- **Next.js & React**: Frontend framework
- **FastAPI**: Backend API framework
- **WildWorlds Font**: Manga typesetting font

## Contributing

This is a personal project, but suggestions and improvements are welcome via issues or pull requests.

## Support

For issues or questions, please open an issue on GitHub.