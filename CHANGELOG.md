# Changelog

All notable changes to Manga TransJohn will be documented in this file.

## [1.0.3] - 2024-02-07

### Security
- **CRITICAL**: Updated Next.js to 15.2.3 to fix cache poisoning DoS and authorization bypass vulnerabilities
- Fixed cache poisoning DoS vulnerability (CVE pending)
- Fixed authorization bypass in Next.js middleware across multiple versions

### Changed
- Upgraded Next.js from 15.0.8 to 15.2.3
- Updated eslint-config-next to 15.2.3

### Notes
- All known Next.js vulnerabilities now patched
- Application fully compatible with Next.js 15.2.3
- PaddlePaddle vulnerabilities remain (no upstream patches available)

## [1.0.2] - 2024-02-07

### Security
- **CRITICAL**: Updated Next.js to 15.0.8 to fix remaining DoS vulnerabilities
- Updated React to 18.3.1 for Next.js 15 compatibility
- Updated React-DOM to 18.3.1 for Next.js 15 compatibility
- Updated TypeScript to 5.7.3
- Updated ESLint to 9.18.0
- Updated all @types packages to latest versions

### Changed
- Upgraded Next.js from 14.2.35 to 15.0.8 (major version upgrade)
- Upgraded ESLint from 8.x to 9.x (major version upgrade)
- Updated eslint-config-next to 15.0.8

### Notes
- Next.js 15 includes performance improvements and security fixes
- Application code compatible with Next.js 15 without modifications
- PaddlePaddle vulnerabilities remain (no upstream patches available)

## [1.0.1] - 2024-02-07

### Security
- **CRITICAL**: Updated all vulnerable dependencies
- Updated fastapi from 0.104.1 to 0.115.6 (ReDoS vulnerability)
- Updated python-multipart from 0.0.6 to 0.0.22 (file write, DoS, ReDoS)
- Updated pillow from 10.1.0 to 10.3.0 (buffer overflow)
- Updated paddlepaddle from 2.5.2 to 2.6.0 (code injection - partial fix)
- Updated next from 14.0.4 to 14.2.35 (multiple DoS, SSRF, auth bypass)
- Updated axios from 1.6.2 to 1.12.0 (DoS, SSRF vulnerabilities)
- Added SECURITY.md with vulnerability documentation
- Added Docker security hardening (cap_drop, no-new-privileges)
- Added resource limits to prevent DoS

### Changed
- Updated uvicorn to 0.34.0
- Updated pydantic to 2.10.6
- Updated requests to 2.32.3
- Updated google-generativeai to 0.8.3
- Updated tailwindcss to 3.4.17
- Updated autoprefixer to 10.4.20
- Updated postcss to 8.4.49
- Fonts volume now read-only in Docker
- Added CPU and memory limits to Docker services

### Documentation
- Added comprehensive SECURITY.md
- Updated README with security warning
- Documented PaddlePaddle unpatched vulnerabilities
- Added mitigation strategies
- Added alternative OCR suggestions

### Known Issues
- PaddlePaddle 2.6.0 still has unpatched vulnerabilities (RCE, command injection, path traversal)
- See SECURITY.md for details and mitigations
- Recommended for personal use in isolated environments only

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
