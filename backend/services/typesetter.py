"""
Typesetting service - renders translated text onto images
"""
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from typing import List, Dict, Any
import os
import logging

logger = logging.getLogger(__name__)

class TypesetterService:
    def __init__(self):
        """Initialize typesetter with WildWorlds font"""
        self._ready = True
        self.font_path = "/app/fonts/WildWorlds.ttf"
        logger.info("Typesetter service initialized")
    
    def is_ready(self) -> bool:
        return self._ready
    
    def _get_font(self, size: int) -> ImageFont.FreeTypeFont:
        """Get font with specified size"""
        if os.path.exists(self.font_path):
            return ImageFont.truetype(self.font_path, size)
        else:
            logger.warning("WildWorlds font not found, using default")
            return ImageFont.load_default()
    
    def _find_optimal_font_size(
        self,
        text: str,
        bbox_width: int,
        bbox_height: int,
        max_size: int = 100,
        min_size: int = 12
    ) -> tuple:
        """
        Find optimal font size to fit text in bbox with line wrapping
        
        Returns:
            (font_size, wrapped_lines)
        """
        for size in range(max_size, min_size - 1, -2):
            font = self._get_font(size)
            
            # Try to wrap text
            words = text.split()
            lines = []
            current_line = []
            
            for word in words:
                test_line = ' '.join(current_line + [word])
                bbox = font.getbbox(test_line)
                width = bbox[2] - bbox[0]
                
                if width <= bbox_width - 10:  # 10px padding
                    current_line.append(word)
                else:
                    if current_line:
                        lines.append(' '.join(current_line))
                        current_line = [word]
                    else:
                        # Single word too long, add it anyway
                        lines.append(word)
            
            if current_line:
                lines.append(' '.join(current_line))
            
            # Check total height
            line_height = font.getbbox('Ay')[3] - font.getbbox('Ay')[1]
            total_height = len(lines) * line_height * 1.2  # 1.2 for line spacing
            
            if total_height <= bbox_height - 10:  # 10px padding
                return size, lines
        
        # If no size works, return minimum
        return min_size, [text]
    
    async def typeset(
        self,
        image_path: str,
        regions: List[Dict[str, Any]],
        translations: List[str],
        image_id: str
    ) -> str:
        """
        Render translated text onto the inpainted image
        
        Args:
            image_path: Path to the inpainted image
            regions: List of text regions
            translations: List of translated texts
            image_id: Unique image identifier
        
        Returns:
            Path to the output image
        """
        try:
            # Load image with PIL for better text rendering
            img_cv = cv2.imread(image_path)
            if img_cv is None:
                raise ValueError(f"Failed to load image: {image_path}")
            
            # Convert BGR to RGB for PIL
            img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(img_rgb)
            draw = ImageDraw.Draw(pil_img)
            
            # Render each translation
            for region, translation in zip(regions, translations):
                if not translation or not translation.strip():
                    continue
                
                bbox = region.get("bbox", {})
                x = bbox.get("x", 0)
                y = bbox.get("y", 0)
                width = bbox.get("width", 100)
                height = bbox.get("height", 50)
                
                # Find optimal font size and wrap text
                font_size, lines = self._find_optimal_font_size(
                    translation,
                    width,
                    height
                )
                font = self._get_font(font_size)
                
                # Calculate line height
                line_bbox = font.getbbox('Ay')
                line_height = (line_bbox[3] - line_bbox[1]) * 1.2
                
                # Calculate starting y to center text vertically
                total_text_height = len(lines) * line_height
                start_y = y + (height - total_text_height) / 2
                
                # Draw each line
                for i, line in enumerate(lines):
                    # Get text bbox for centering
                    text_bbox = font.getbbox(line)
                    text_width = text_bbox[2] - text_bbox[0]
                    
                    # Center horizontally
                    text_x = x + (width - text_width) / 2
                    text_y = start_y + i * line_height
                    
                    # Draw text with outline for readability
                    # Outline
                    for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                        draw.text(
                            (text_x + dx, text_y + dy),
                            line,
                            font=font,
                            fill=(0, 0, 0)  # Black outline
                        )
                    
                    # Main text
                    draw.text(
                        (text_x, text_y),
                        line,
                        font=font,
                        fill=(255, 255, 255)  # White text
                    )
            
            # Convert back to OpenCV format
            result_rgb = np.array(pil_img)
            result_bgr = cv2.cvtColor(result_rgb, cv2.COLOR_RGB2BGR)
            
            # Save output image
            output_dir = "/app/data/output"
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, f"{image_id}.png")
            cv2.imwrite(output_path, result_bgr)
            
            logger.info(f"Typeset image saved to {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error during typesetting: {e}")
            raise
