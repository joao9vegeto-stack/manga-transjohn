# Changelog

All notable changes to Manga TransJohn will be documented in this file.

## [1.0.0] - 2024-02-07

### Added
- Initial release
- Complete translation pipeline (detection → OCR → translation → inpainting → typesetting)
- FastAPI backend with PaddleOCR and Gemini 2.5 Flash
- Next.js frontend with interactive editor
- Docker Compose deployment
- Cover mode for filtering large text
- Undo/redo functionality
- Region editing and deletion
- Project export (PNG + JSON)
- Support for 7 source languages
- Brazilian Portuguese (pt-BR) as target language
- WildWorlds font integration
- Local-only storage
- Rate limiting and security features

### Backend Features
- Text detection using PaddleOCR
- OCR with multi-language support
- Gemini 2.5 Flash translation with manga-optimized prompts
- OpenCV inpainting for text removal
- Dynamic font sizing and typesetting
- Project persistence with JSON storage

### Frontend Features
- Drag-and-drop image upload
- Clipboard paste support
- Canvas-based image editor
- Region selection and editing
- Translation text editing
- Cover mode toggle
- Ignore list for regions
- Export to PNG and JSON
- Responsive UI with TailwindCSS

### Documentation
- Comprehensive README
- Setup instructions
- Usage guide
- API documentation
- Troubleshooting guide
- Contributing guidelines
