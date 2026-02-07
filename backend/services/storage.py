"""
Storage service for managing projects and files
"""
import os
import json
import shutil
from datetime import datetime
from typing import Dict, Any, List, Optional
import aiofiles
import logging

logger = logging.getLogger(__name__)

class StorageService:
    def __init__(self):
        """Initialize storage service"""
        self.data_dir = "/app/data"
        self.uploads_dir = os.path.join(self.data_dir, "uploads")
        self.projects_dir = os.path.join(self.data_dir, "projects")
        self.inpainted_dir = os.path.join(self.data_dir, "inpainted")
        self.output_dir = os.path.join(self.data_dir, "output")
        
        # Create directories
        for directory in [self.uploads_dir, self.projects_dir, self.inpainted_dir, self.output_dir]:
            os.makedirs(directory, exist_ok=True)
        
        logger.info("Storage service initialized")
    
    async def save_upload(self, image_id: str, file) -> str:
        """Save uploaded file"""
        file_path = os.path.join(self.uploads_dir, f"{image_id}.png")
        
        # Read file content
        content = await file.read()
        
        # Save file
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(content)
        
        logger.info(f"Saved upload: {file_path}")
        return file_path
    
    def get_image_path(self, image_id: str) -> str:
        """Get path to original uploaded image"""
        return os.path.join(self.uploads_dir, f"{image_id}.png")
    
    def get_inpainted_path(self, image_id: str) -> str:
        """Get path to inpainted image"""
        return os.path.join(self.inpainted_dir, f"{image_id}.png")
    
    def get_output_path(self, image_id: str) -> str:
        """Get path to final output image"""
        return os.path.join(self.output_dir, f"{image_id}.png")
    
    async def save_detection(self, image_id: str, regions: List[Dict[str, Any]]) -> None:
        """Save detection results"""
        data = {
            "image_id": image_id,
            "regions": regions,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        file_path = os.path.join(self.projects_dir, f"{image_id}_detection.json")
        async with aiofiles.open(file_path, 'w') as f:
            await f.write(json.dumps(data, indent=2))
    
    async def save_ocr(self, image_id: str, texts: List[str]) -> None:
        """Save OCR results"""
        data = {
            "image_id": image_id,
            "texts": texts,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        file_path = os.path.join(self.projects_dir, f"{image_id}_ocr.json")
        async with aiofiles.open(file_path, 'w') as f:
            await f.write(json.dumps(data, indent=2))
    
    async def save_project(
        self,
        image_id: str,
        regions: List[Dict[str, Any]],
        texts: List[str],
        translations: List[str],
        source_lang: str
    ) -> str:
        """
        Save complete project data
        
        Returns:
            project_id
        """
        project_id = image_id
        
        project_data = {
            "project_id": project_id,
            "image_id": image_id,
            "source_lang": source_lang,
            "target_lang": "pt-BR",
            "regions": regions,
            "texts": texts,
            "translations": translations,
            "deleted_regions": [],
            "ignored_regions": [],
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }
        
        file_path = os.path.join(self.projects_dir, f"{project_id}.json")
        async with aiofiles.open(file_path, 'w') as f:
            await f.write(json.dumps(project_data, indent=2))
        
        logger.info(f"Saved project: {project_id}")
        return project_id
    
    async def get_project(self, project_id: str) -> Optional[Dict[str, Any]]:
        """Load project data"""
        file_path = os.path.join(self.projects_dir, f"{project_id}.json")
        
        if not os.path.exists(file_path):
            return None
        
        async with aiofiles.open(file_path, 'r') as f:
            content = await f.read()
            return json.loads(content)
    
    async def update_project(
        self,
        project_id: str,
        regions: List[Dict[str, Any]],
        deleted_regions: List[int],
        ignored_regions: List[int]
    ) -> None:
        """Update project with user edits"""
        project = await self.get_project(project_id)
        if not project:
            raise ValueError(f"Project not found: {project_id}")
        
        project["regions"] = regions
        project["deleted_regions"] = deleted_regions
        project["ignored_regions"] = ignored_regions
        project["updated_at"] = datetime.utcnow().isoformat()
        
        file_path = os.path.join(self.projects_dir, f"{project_id}.json")
        async with aiofiles.open(file_path, 'w') as f:
            await f.write(json.dumps(project, indent=2))
        
        logger.info(f"Updated project: {project_id}")
