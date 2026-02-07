"""
OCR service using PaddleOCR
"""
from paddleocr import PaddleOCR
import cv2
import numpy as np
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class OCRService:
    def __init__(self):
        """Initialize PaddleOCR with recognition"""
        try:
            # Initialize PaddleOCR with both detection and recognition
            self.ocr = PaddleOCR(
                use_angle_cls=True,
                lang='ch',  # Supports Chinese, Japanese, Korean
                det=False,  # We already have detections
                rec=True,
                show_log=False
            )
            self._ready = True
            logger.info("OCR service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize OCR service: {e}")
            self._ready = False
    
    def is_ready(self) -> bool:
        return self._ready
    
    async def extract_text(self, image_path: str, regions: List[Dict[str, Any]]) -> List[str]:
        """
        Extract text from detected regions
        
        Args:
            image_path: Path to the image file
            regions: List of region dictionaries with bbox information
        
        Returns:
            List of extracted text strings
        """
        try:
            # Load image
            img = cv2.imread(image_path)
            if img is None:
                raise ValueError(f"Failed to load image: {image_path}")
            
            texts = []
            
            for region in regions:
                bbox = region.get("bbox", {})
                x = bbox.get("x", 0)
                y = bbox.get("y", 0)
                width = bbox.get("width", 0)
                height = bbox.get("height", 0)
                
                # Add padding to improve OCR accuracy
                padding = 5
                x = max(0, x - padding)
                y = max(0, y - padding)
                width = min(img.shape[1] - x, width + 2 * padding)
                height = min(img.shape[0] - y, height + 2 * padding)
                
                # Crop region
                roi = img[y:y+height, x:x+width]
                
                if roi.size == 0:
                    texts.append("")
                    continue
                
                try:
                    # Run OCR on the region
                    result = self.ocr.ocr(roi, det=False, rec=True, cls=True)
                    
                    if result and len(result) > 0 and result[0]:
                        # Extract text from result
                        # PaddleOCR returns format: [[[text, confidence]]]
                        text_parts = []
                        for line in result[0]:
                            if isinstance(line, (list, tuple)) and len(line) >= 2:
                                text_parts.append(str(line[0]))
                        
                        text = " ".join(text_parts) if text_parts else ""
                    else:
                        text = ""
                    
                    texts.append(text.strip())
                    
                except Exception as e:
                    logger.warning(f"Failed to extract text from region: {e}")
                    texts.append("")
            
            logger.info(f"Extracted text from {len(texts)} regions")
            return texts
            
        except Exception as e:
            logger.error(f"Error during OCR: {e}")
            raise
