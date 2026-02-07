"""
Text detection service using PaddleOCR detector
"""
from paddleocr import PaddleOCR
from PIL import Image
import numpy as np
import cv2
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class TextDetector:
    def __init__(self):
        """Initialize PaddleOCR detector"""
        try:
            # Initialize PaddleOCR with detection only
            self.ocr = PaddleOCR(
                use_angle_cls=True,
                lang='ch',  # Supports multiple languages including Japanese
                det=True,
                rec=False,  # Detection only
                show_log=False
            )
            self._ready = True
            logger.info("Text detector initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize text detector: {e}")
            self._ready = False
    
    def is_ready(self) -> bool:
        return self._ready
    
    async def detect(self, image_path: str, cover_mode: bool = False) -> List[Dict[str, Any]]:
        """
        Detect text regions in an image
        
        Args:
            image_path: Path to the image file
            cover_mode: If True, be more conservative with detection (filter large stylized text)
        
        Returns:
            List of region dictionaries with bbox and polygon
        """
        try:
            # Load image
            img = cv2.imread(image_path)
            if img is None:
                raise ValueError(f"Failed to load image: {image_path}")
            
            # Run detection
            result = self.ocr.ocr(img, det=True, rec=False, cls=False)
            
            if not result or not result[0]:
                return []
            
            regions = []
            img_height, img_width = img.shape[:2]
            
            for idx, detection in enumerate(result[0]):
                # Get polygon points
                points = detection
                if isinstance(points, list) and len(points) >= 4:
                    # Convert to numpy array for easier manipulation
                    poly = np.array(points, dtype=np.float32)
                    
                    # Calculate bounding box
                    x_coords = poly[:, 0]
                    y_coords = poly[:, 1]
                    x_min, x_max = int(x_coords.min()), int(x_coords.max())
                    y_min, y_max = int(y_coords.min()), int(y_coords.max())
                    
                    width = x_max - x_min
                    height = y_max - y_min
                    
                    # Skip very small regions (likely noise)
                    if width < 10 or height < 10:
                        continue
                    
                    # Cover mode: filter out very large regions (likely titles/logos)
                    if cover_mode:
                        # Calculate region size relative to image
                        region_area = width * height
                        image_area = img_width * img_height
                        relative_size = region_area / image_area
                        
                        # Skip regions that are very large (>15% of image area)
                        # or very wide/tall (aspect ratio filters)
                        if relative_size > 0.15:
                            continue
                        
                        # Also skip very tall or very wide regions (stylized text)
                        aspect_ratio = max(width, height) / min(width, height)
                        if aspect_ratio > 10:
                            continue
                    
                    region = {
                        "id": idx,
                        "bbox": {
                            "x": x_min,
                            "y": y_min,
                            "width": width,
                            "height": height
                        },
                        "polygon": poly.tolist(),
                        "area": width * height
                    }
                    regions.append(region)
            
            logger.info(f"Detected {len(regions)} text regions (cover_mode={cover_mode})")
            return regions
            
        except Exception as e:
            logger.error(f"Error during text detection: {e}")
            raise
