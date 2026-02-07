"""
Inpainting service using OpenCV (fallback) or advanced techniques
"""
import cv2
import numpy as np
from typing import List, Dict, Any
import os
import logging

logger = logging.getLogger(__name__)

class InpainterService:
    def __init__(self):
        """Initialize inpainting service"""
        self._ready = True
        logger.info("Inpainter service initialized (using OpenCV)")
    
    def is_ready(self) -> bool:
        return self._ready
    
    async def inpaint(
        self,
        image_path: str,
        regions: List[Dict[str, Any]],
        image_id: str
    ) -> str:
        """
        Remove text from image using inpainting
        
        Args:
            image_path: Path to the original image
            regions: List of regions to inpaint
            image_id: Unique image identifier
        
        Returns:
            Path to the inpainted image
        """
        try:
            # Load image
            img = cv2.imread(image_path)
            if img is None:
                raise ValueError(f"Failed to load image: {image_path}")
            
            # Create mask from regions
            mask = np.zeros(img.shape[:2], dtype=np.uint8)
            
            for region in regions:
                polygon = region.get("polygon")
                if polygon:
                    # Convert polygon to numpy array
                    pts = np.array(polygon, dtype=np.int32)
                    # Fill polygon in mask
                    cv2.fillPoly(mask, [pts], 255)
                else:
                    # Fallback to bbox
                    bbox = region.get("bbox", {})
                    x = bbox.get("x", 0)
                    y = bbox.get("y", 0)
                    width = bbox.get("width", 0)
                    height = bbox.get("height", 0)
                    cv2.rectangle(mask, (x, y), (x + width, y + height), 255, -1)
            
            # Dilate mask slightly to ensure text edges are covered
            kernel = np.ones((3, 3), np.uint8)
            mask = cv2.dilate(mask, kernel, iterations=1)
            
            # Perform inpainting using OpenCV's Telea method
            # This is a fast method suitable for text removal
            inpainted = cv2.inpaint(img, mask, 3, cv2.INPAINT_TELEA)
            
            # Save inpainted image
            output_dir = "/app/data/inpainted"
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, f"{image_id}.png")
            cv2.imwrite(output_path, inpainted)
            
            logger.info(f"Inpainted image saved to {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error during inpainting: {e}")
            raise
