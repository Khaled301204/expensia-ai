import whisper
import os
import tempfile
from pathlib import Path
from typing import Dict

class SpeechService:
    
    def __init__(self):
        """
        Initialize Whisper model with FFmpeg path
        """
        # Set FFmpeg path for Windows (Chocolatey install location)
        ffmpeg_paths = [
            r"C:\ProgramData\chocolatey\bin",
            r"C:\ProgramData\chocolatey\lib\ffmpeg\tools\ffmpeg\bin",
            r"C:\ffmpeg\bin"
        ]
        
        # Add FFmpeg to PATH if found
        for ffmpeg_path in ffmpeg_paths:
            if os.path.exists(ffmpeg_path):
                os.environ["PATH"] = ffmpeg_path + os.pathsep + os.environ.get("PATH", "")
                print(f"✅ FFmpeg found at: {ffmpeg_path}")
                break
        
        print("Loading Whisper model... (first run downloads ~150MB)")
        self.model = whisper.load_model("small")  # Use "small" for better accuracy (vs "tiny")
        print("✅ Whisper model loaded successfully!")
    
    def transcribe_audio(
        self, 
        audio_content: bytes, 
        language: str = "ar"
    ) -> Dict:
        """
        Transcribe audio to text using OpenAI Whisper
        """
        try:
            # Save audio to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_audio:
                temp_audio.write(audio_content)
                temp_path = temp_audio.name
            
            try:
                # Transcribe with Whisper
                if language == "auto":
                    result = self.model.transcribe(temp_path)
                else:
                    result = self.model.transcribe(temp_path, language=language)
                
                # Extract results
                transcript = result["text"].strip()
                detected_language = result.get("language", language)
                
                # Estimate confidence
                no_speech_prob = result.get("segments", [{}])[0].get("no_speech_prob", 0.5) if result.get("segments") else 0.5
                confidence = 1.0 - no_speech_prob
                
                return {
                    "success": True,
                    "transcript": transcript,
                    "confidence": round(confidence, 2),
                    "language": language if language != "auto" else detected_language,
                    "detected_language": detected_language
                }
            
            finally:
                # Clean up temp file
                try:
                    os.unlink(temp_path)
                except:
                    pass
        
        except Exception as e:
            return {
                "success": False,
                "transcript": "",
                "confidence": 0.0,
                "language": language,
                "detected_language": "unknown",
                "error": str(e)
            }
    
    def transcribe_audio_bilingual(self, audio_content: bytes) -> Dict:
        """
        Auto-detect language and transcribe (Arabic or English)
        """
        return self.transcribe_audio(audio_content, language="auto")
    
    def get_supported_languages(self) -> list:
        """
        Get list of languages supported by Whisper
        """
        return [
            {"code": "ar", "name": "Arabic", "native_name": "العربية"},
            {"code": "en", "name": "English", "native_name": "English"},
            {"code": "auto", "name": "Auto Detect", "native_name": "Automatic"}
        ]