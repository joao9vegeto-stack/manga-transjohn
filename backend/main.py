from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
import json
import uuid
import asyncio
from datetime import datetime

from services.detector import TextDetector
from services.ocr import OCRService
from services.translator import TranslatorService
from services.inpainter import InpainterService
from services.typesetter import TypesetterService
from services.storage import StorageService

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(title="Manga TransJohn API", version="1.0.0")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://frontend:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
detector = TextDetector()
ocr_service = OCRService()
translator = TranslatorService()
inpainter = InpainterService()
typesetter = TypesetterService()
storage = StorageService()

# Pydantic models
class DetectRequest(BaseModel):
    image_id: str
    cover_mode: bool = False

class OCRRequest(BaseModel):
    image_id: str
    regions: List[Dict[str, Any]]

class TranslateRequest(BaseModel):
    texts: List[str]
    source_lang: str
    target_lang: str = "pt-BR"

class InpaintRequest(BaseModel):
    image_id: str
    regions: List[Dict[str, Any]]

class TypesetRequest(BaseModel):
    image_id: str
    regions: List[Dict[str, Any]]
    translations: List[str]

class PipelineRequest(BaseModel):
    image_id: str
    source_lang: str
    cover_mode: bool = False
    ignored_regions: List[int] = []

class UpdateProjectRequest(BaseModel):
    project_id: str
    regions: List[Dict[str, Any]]
    deleted_regions: List[int] = []
    ignored_regions: List[int] = []

@app.get("/")
async def root():
    return {"message": "Manga TransJohn API", "version": "1.0.0"}

@app.post("/upload")
@limiter.limit("10/minute")
async def upload_image(request: Any, file: UploadFile = File(...)):
    """Upload an image and return an image_id"""
    try:
        # Generate unique ID
        image_id = str(uuid.uuid4())
        
        # Save uploaded file
        file_path = await storage.save_upload(image_id, file)
        
        return {
            "image_id": image_id,
            "filename": file.filename,
            "path": file_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/detect")
@limiter.limit("20/minute")
async def detect_text(request: Any, data: DetectRequest):
    """Detect text regions in an image"""
    try:
        image_path = storage.get_image_path(data.image_id)
        regions = await detector.detect(image_path, data.cover_mode)
        
        # Save detection results
        await storage.save_detection(data.image_id, regions)
        
        return {
            "image_id": data.image_id,
            "regions": regions,
            "count": len(regions)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ocr")
@limiter.limit("20/minute")
async def extract_text(request: Any, data: OCRRequest):
    """Extract text from detected regions"""
    try:
        image_path = storage.get_image_path(data.image_id)
        texts = await ocr_service.extract_text(image_path, data.regions)
        
        # Save OCR results
        await storage.save_ocr(data.image_id, texts)
        
        return {
            "image_id": data.image_id,
            "texts": texts
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/translate")
@limiter.limit("30/minute")
async def translate_text(request: Any, data: TranslateRequest):
    """Translate texts using Gemini 2.5 Flash"""
    try:
        translations = await translator.translate_batch(
            data.texts,
            data.source_lang,
            data.target_lang
        )
        
        return {
            "translations": translations,
            "count": len(translations)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/inpaint")
@limiter.limit("10/minute")
async def inpaint_image(request: Any, data: InpaintRequest):
    """Remove text from image using inpainting"""
    try:
        image_path = storage.get_image_path(data.image_id)
        inpainted_path = await inpainter.inpaint(
            image_path,
            data.regions,
            data.image_id
        )
        
        return {
            "image_id": data.image_id,
            "inpainted_path": inpainted_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/typeset")
@limiter.limit("20/minute")
async def typeset_text(request: Any, data: TypesetRequest):
    """Render translations onto the image"""
    try:
        inpainted_path = storage.get_inpainted_path(data.image_id)
        output_path = await typesetter.typeset(
            inpainted_path,
            data.regions,
            data.translations,
            data.image_id
        )
        
        return {
            "image_id": data.image_id,
            "output_path": output_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/pipeline")
@limiter.limit("5/minute")
async def run_pipeline(request: Any, data: PipelineRequest):
    """Run the complete translation pipeline"""
    try:
        image_path = storage.get_image_path(data.image_id)
        
        # Step 1: Detect text regions
        regions = await detector.detect(image_path, data.cover_mode)
        
        # Filter out ignored regions
        if data.ignored_regions:
            regions = [r for i, r in enumerate(regions) if i not in data.ignored_regions]
        
        if not regions:
            return {
                "image_id": data.image_id,
                "status": "no_text_detected",
                "message": "No text regions detected"
            }
        
        # Step 2: Extract text with OCR
        texts = await ocr_service.extract_text(image_path, regions)
        
        # Step 3: Translate texts
        translations = await translator.translate_batch(
            texts,
            data.source_lang,
            "pt-BR"
        )
        
        # Step 4: Inpaint original text
        inpainted_path = await inpainter.inpaint(
            image_path,
            regions,
            data.image_id
        )
        
        # Step 5: Typeset translations
        output_path = await typesetter.typeset(
            inpainted_path,
            regions,
            translations,
            data.image_id
        )
        
        # Save project
        project_id = await storage.save_project(
            data.image_id,
            regions,
            texts,
            translations,
            data.source_lang
        )
        
        return {
            "image_id": data.image_id,
            "project_id": project_id,
            "regions": regions,
            "texts": texts,
            "translations": translations,
            "output_path": output_path,
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/project/{project_id}")
async def get_project(project_id: str):
    """Retrieve a saved project"""
    try:
        project = await storage.get_project(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        return project
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/project/update")
async def update_project(data: UpdateProjectRequest):
    """Update project with user edits"""
    try:
        await storage.update_project(
            data.project_id,
            data.regions,
            data.deleted_regions,
            data.ignored_regions
        )
        return {"status": "success", "project_id": data.project_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/image/{image_id}")
async def get_image(image_id: str, type: str = "original"):
    """Retrieve an image (original, inpainted, or output)"""
    try:
        if type == "original":
            path = storage.get_image_path(image_id)
        elif type == "inpainted":
            path = storage.get_inpainted_path(image_id)
        elif type == "output":
            path = storage.get_output_path(image_id)
        else:
            raise HTTPException(status_code=400, detail="Invalid image type")
        
        if not os.path.exists(path):
            raise HTTPException(status_code=404, detail="Image not found")
        
        return FileResponse(path)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "services": {
            "detector": detector.is_ready(),
            "ocr": ocr_service.is_ready(),
            "translator": translator.is_ready(),
            "inpainter": inpainter.is_ready(),
            "typesetter": typesetter.is_ready()
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
