"""
Translation service using Google Gemini 2.5 Flash
"""
import google.generativeai as genai
import os
from typing import List
import logging
import asyncio

logger = logging.getLogger(__name__)

class TranslatorService:
    def __init__(self):
        """Initialize Gemini API"""
        try:
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                logger.warning("GEMINI_API_KEY not set - translator will not work")
                self._ready = False
                return
            
            genai.configure(api_key=api_key)
            
            # Use Gemini 2.5 Flash as specified
            self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
            
            self._ready = True
            logger.info("Gemini translator initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize translator: {e}")
            self._ready = False
    
    def is_ready(self) -> bool:
        return self._ready
    
    def _get_translation_prompt(self, text: str, source_lang: str, target_lang: str) -> str:
        """
        Generate the translation prompt for Gemini
        
        This prompt is tuned for manga translation to Brazilian Portuguese
        """
        lang_names = {
            "ja": "Japanese",
            "ko": "Korean",
            "zh-CN": "Chinese (Simplified)",
            "zh-TW": "Chinese (Traditional)",
            "en": "English",
            "es": "Spanish",
            "fr": "French"
        }
        
        source_name = lang_names.get(source_lang, source_lang)
        
        prompt = f"""You are a professional manga translator. Translate the following {source_name} text to Brazilian Portuguese (pt-BR).

Rules:
1. Translate naturally and conversationally, keeping the tone and emotional context
2. Preserve honorifics when culturally relevant (e.g., -san, -kun, -chan can be kept or adapted)
3. If the text is a sound effect (onomatopoeia), translate to an equivalent Brazilian Portuguese onomatopoeia or keep the original with a small pt-BR equivalent
4. Keep translations concise to fit in manga speech bubbles
5. Do NOT add explanations or notes - output ONLY the translated text
6. Preserve line breaks if present
7. If text is empty or just symbols, return it as-is

Text to translate:
{text}

Brazilian Portuguese translation:"""
        
        return prompt
    
    async def translate(self, text: str, source_lang: str, target_lang: str = "pt-BR") -> str:
        """
        Translate a single text using Gemini 2.5 Flash
        
        Args:
            text: Text to translate
            source_lang: Source language code (ja, ko, zh-CN, zh-TW, en, es, fr)
            target_lang: Target language (always pt-BR)
        
        Returns:
            Translated text
        """
        if not self._ready:
            raise RuntimeError("Translator not initialized - check GEMINI_API_KEY")
        
        if not text or not text.strip():
            return text
        
        try:
            prompt = self._get_translation_prompt(text, source_lang, target_lang)
            
            # Run in executor to avoid blocking
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.model.generate_content(prompt)
            )
            
            translated = response.text.strip()
            logger.debug(f"Translated: '{text}' -> '{translated}'")
            
            return translated
            
        except Exception as e:
            logger.error(f"Translation failed for text '{text}': {e}")
            # Return original text if translation fails
            return text
    
    async def translate_batch(
        self,
        texts: List[str],
        source_lang: str,
        target_lang: str = "pt-BR"
    ) -> List[str]:
        """
        Translate multiple texts
        
        Args:
            texts: List of texts to translate
            source_lang: Source language code
            target_lang: Target language (always pt-BR)
        
        Returns:
            List of translated texts
        """
        if not self._ready:
            raise RuntimeError("Translator not initialized - check GEMINI_API_KEY")
        
        # Translate each text sequentially to avoid rate limits
        # Could be optimized with batching if needed
        translations = []
        for text in texts:
            translated = await self.translate(text, source_lang, target_lang)
            translations.append(translated)
            # Small delay to avoid rate limiting
            await asyncio.sleep(0.5)
        
        logger.info(f"Translated {len(translations)} texts")
        return translations
