# Manga TransJohn

Self-hosted manga/manhwa image translator (personal use) with a Torii-like UX.

## Stack
- Frontend: Next.js (TypeScript) + Konva.js
- Backend: FastAPI (Python)
- OCR/Detection: PaddleOCR
- Inpainting: LaMa (fallback OpenCV inpaint)
- Translation: Gemini 2.5 Flash ONLY (pt-BR target fixed)
- Storage: SQLite + local `/data` folder

## Repo Structure
```
frontend/   # Next.js app
backend/    # FastAPI service
samples/    # sample images
```

## Setup
### 1) Requirements
- Docker + Docker Compose (recommended)
- Or local: Node.js 20+, Python 3.10+

### 2) Font (required)
Place the provided **WildWorlds** font in:
```
backend/assets/fonts/WildWorlds.ttf
```
(You can also use `.otf` with the same filename.)

### 3) Environment
Create a `.env` file in `backend/`:
```
GEMINI_API_KEY=YOUR_KEY_HERE
```
> Do not commit keys. The key is loaded server-side only.

## Run with Docker
```
docker compose up --build
```
- Frontend: http://localhost:3000
- Backend: http://localhost:8000

## Run locally (dev)
### Backend
```
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend
```
cd frontend
npm install
npm run dev
```

## Usage
1. Open the app.
2. Upload or paste an image.
3. Select source language.
4. Click **Translate**.
5. Edit regions on the editor page (erase, ignore, manual add).
6. Export PNG or project JSON.

## Cover mode
Enable **Cover mode** to ignore large stylized text by default. You can also mark any region as **Ignore** and re-run translation without it.

## Sample images
Sample SVGs are provided in `samples/`:
- `samples/manga-page.svg`
- `samples/cover.svg`

Test steps:
1. Translate `samples/manga-page.svg`.
2. Enable **Cover mode** and ensure the cover title is ignored on `samples/cover.svg`.
3. Delete the cover title translation while keeping speech bubbles.

## License
Personal use only (project template).