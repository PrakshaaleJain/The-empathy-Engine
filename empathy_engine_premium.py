"""
The Empathy Engine Premium
Advanced version with high-quality TTS engines
"""

import os
import asyncio
import argparse
from datetime import datetime
from typing import Dict, Tuple
import subprocess
import tempfile
from textblob import TextBlob


# Try for different version of TTS
try:
    import edge_tts
    EDGE_TTS_AVAILABLE = True
except ImportError:
    EDGE_TTS_AVAILABLE = False

try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False

try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False

class EmotionDetector:
    """Analyzes text and detects emotional content"""
    
    @staticmethod
    def analyze(text: str) -> Tuple[str, float, float]:
        """
        Analyze text for emotion and sentiment
        Returns: (emotion_category, polarity, intensity)
        """
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity 
        subjectivity = blob.sentiment.subjectivity 
        
        # Classify emotion based on polarity
        if polarity > 0.3:
            emotion = "happy"
        elif polarity < -0.3:
            emotion = "sad"
        elif polarity < -0.1:
            emotion = "frustrated"
        elif subjectivity > 0.6 and abs(polarity) < 0.3:
            emotion = "excited"
        else:
            emotion = "neutral"
        
        intensity = min(abs(polarity) + (subjectivity * 0.3), 1.0)
        
        return emotion, polarity, intensity

class PremiumVoiceModulator:
    """High-quality voice modulation with multiple TTS engines"""
    
    def __init__(self, engine_type="edge"):
        self.engine_type = engine_type
        self.available_engines = self._check_available_engines()
        
        # Voice profiles for different emotions
        self.edge_voices = {
            "happy": "en-US-JennyNeural",      # Cheerful female voice
            "excited": "en-US-AriaNeural",     # Energetic female voice
            "sad": "en-US-GuyNeural",          # Gentle male voice
            "frustrated": "en-US-DavisNeural", # Authoritative male voice
            "neutral": "en-US-JennyNeural"     # Balanced female voice
        }
        
        self.speaking_styles = {
            "happy": "cheerful",
            "excited": "excited",
            "sad": "sad", 
            "frustrated": "angry",
            "neutral": "friendly"
        }
        
        self.speaking_rates = {
            "happy": "+20%",
            "excited": "+30%", 
            "sad": "-20%",
            "frustrated": "+10%",
            "neutral": "+0%"
        }
        
        print(f"Premium Voice Engine initialized")
        print(f"Available engines: {', '.join(self.available_engines)}")
        
        if engine_type == "edge" and "edge-tts" not in self.available_engines:
            print("Edge TTS not available, falling back to next best option")
            if "gtts" in self.available_engines:
                self.engine_type = "gtts"
            elif "espeak" in self.available_engines:
                self.engine_type = "espeak"
    
    def _check_available_engines(self):
        """Check which TTS engines are available"""
        engines = []
        
        if EDGE_TTS_AVAILABLE:
            engines.append("edge-tts")
        
        if GTTS_AVAILABLE:
            engines.append("gtts")
            
        if PYTTSX3_AVAILABLE:
            engines.append("espeak")
            
        # Check if espeak system command is available
        try:
            subprocess.run(["espeak", "--version"], capture_output=True, check=True)
            if "espeak-cmd" not in engines:
                engines.append("espeak-cmd")
        except:
            pass
            
        return engines
    
    async def synthesize_edge_tts(self, text: str, emotion: str, intensity: float, output_file: str):
        """Generate speech using Microsoft Edge TTS (highest quality)"""
        try:
            voice = self.edge_voices.get(emotion, self.edge_voices["neutral"])
            style = self.speaking_styles.get(emotion, "friendly")
            rate = self.speaking_rates.get(emotion, "+0%")
            
            # Adjust style intensity based on emotion intensity
            if intensity < 0.3:
                style = "friendly"  # Use neutral style for low intensity
            
            print(f"Using Edge TTS")
            print(f"    - Voice: {voice}")
            print(f"    - Style: {style}")
            print(f"    - Rate: {rate}")
            print(f"    - Emotion intensity: {intensity:.1%}")
            
            # Clean the text to avoid any issues with special characters
            clean_text = text.replace('<', '&lt;').replace('>', '&gt;').replace('&', '&amp;')
            
            # Try simple text first, fallback to SSML if needed
            try:
                # Simple approach - just use the voice and text
                communicate = edge_tts.Communicate(clean_text, voice, rate=rate)
                await communicate.save(output_file)
                
                if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
                    print(f"High-quality audio saved to: {output_file}")
                    return True
                else:
                    raise Exception("No audio file generated with simple method")
                    
            except Exception as simple_error:
                print(f"    ⚠️  Simple method failed, trying SSML: {simple_error}")
                
                # Fallback to SSML with proper formatting
                style_degree = min(max(intensity + 0.5, 0.5), 2.0)  # Clamp between 0.5 and 2.0
                
                ssml = f'''<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="en-US">
<voice name="{voice}">
<mstts:express-as style="{style}" styledegree="{style_degree:.1f}">
<prosody rate="{rate}">
{clean_text}
</prosody>
</mstts:express-as>
</voice>
</speak>'''
                
                communicate = edge_tts.Communicate(ssml, voice)
                await communicate.save(output_file)
                
                if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
                    print(f"High-quality audio saved to: {output_file}")
                    return True
                else:
                    print(f"Failed to generate audio file")
                    return False
                
        except Exception as e:
            print(f"Edge TTS error: {e}")
            return False
    
    def synthesize_gtts(self, text: str, emotion: str, intensity: float, output_file: str):
        """Generate speech using Google TTS (good quality)"""
        try:
            print(f"  🌐 Using Google TTS")
            print(f"    - Emotion: {emotion}")
            print(f"    - Intensity: {intensity:.1%}")
            
            # Clean the text and add subtle emotional emphasis without emojis or metadata
            clean_text = text.strip()
            
            # Add emotional emphasis to text (subtle punctuation only)
            if intensity > 0.5:
                if emotion == "excited" and not clean_text.endswith('!'):
                    clean_text = clean_text.rstrip('.') + "!"
                elif emotion == "sad" and not clean_text.endswith('...'):
                    clean_text = clean_text.rstrip('.') + "..."
                elif emotion == "frustrated" and not clean_text.endswith('!'):
                    clean_text = clean_text.rstrip('.') + "!"
            
            # Use slower speech for sad emotions, faster for excited
            slow = emotion == "sad" and intensity > 0.5
            
            print(f"    - Processing text: \"{clean_text}\"")
            print(f"    - Slow speech: {slow}")
            
            tts = gTTS(text=clean_text, lang='en', slow=slow)
            tts.save(output_file)
            
            if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
                print(f"Audio saved to: {output_file}")
                return True
            else:
                print(f"Failed to generate audio file")
                return False
                
        except Exception as e:
            print(f"Google TTS error: {e}")
            return False
    
    def synthesize_espeak_cmd(self, text: str, emotion: str, intensity: float, output_file: str):
        """Generate speech using espeak command line with better settings"""
        try:
            print(f"Using Enhanced Espeak")
            voice_map = {
                "happy": "en-us+f3",      # Female voice, higher pitch
                "excited": "en-us+f4",    # Female voice, even higher
                "sad": "en-gb+m3",        # Male voice, lower pitch
                "frustrated": "en-us+m2", # Male voice, firm
                "neutral": "en-us+f2"     # Balanced female voice
            }
            
            voice = voice_map.get(emotion, "en-us+f2")
            
            # Adjust speed and pitch based on emotion
            speed = 160  # Base speed
            pitch = 50   # Base pitch
            
            if emotion == "happy":
                speed = int(speed * 1.2)
                pitch = int(pitch * 1.3)
            elif emotion == "excited": 
                speed = int(speed * 1.4)
                pitch = int(pitch * 1.5)
            elif emotion == "sad":
                speed = int(speed * 0.8)
                pitch = int(pitch * 0.7)
            elif emotion == "frustrated":
                speed = int(speed * 1.1)
                pitch = int(pitch * 0.8)
            
            # Apply intensity scaling
            speed = int(speed * (1 + intensity * 0.2))
            
            print(f"    - Voice: {voice}")
            print(f"    - Speed: {speed} wpm")
            print(f"    - Pitch: {pitch}")
            
            # Generate audio with espeak
            cmd = [
                "espeak",
                "-v", voice,
                "-s", str(speed),
                "-p", str(pitch),
                "-a", "100",  # Amplitude
                "-g", "5",    # Gap between words
                "-w", output_file,
                text
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0 and os.path.exists(output_file):
                print(f"Audio saved to: {output_file}")
                return True
            else:
                print(f"Espeak failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"Espeak command error: {e}")
            return False
    
    async def synthesize(self, text: str, emotion: str, intensity: float, output_file: str):
        """Generate speech with the best available engine"""
        
        # Ensure output file has .wav extension
        if not output_file.endswith('.wav'):
            output_file = output_file.replace('.txt', '.wav')
        
        # Make sure the output directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        success = False
        
        # Try engines in order of quality
        if self.engine_type == "edge" and "edge-tts" in self.available_engines:
            success = await self.synthesize_edge_tts(text, emotion, intensity, output_file)
        
        if not success and "gtts" in self.available_engines:
            print("  Falling back to Google TTS...")
            success = self.synthesize_gtts(text, emotion, intensity, output_file)
        
        if not success and "espeak-cmd" in self.available_engines:
            print("  Falling back to Enhanced Espeak...")
            success = self.synthesize_espeak_cmd(text, emotion, intensity, output_file)
        
        if not success:
            # Create fallback text file
            fallback_file = output_file.replace('.wav', '.txt')
            with open(fallback_file, 'w') as f:
                f.write(f"Text: {text}\n")
                f.write(f"Emotion: {emotion}\n")
                f.write(f"Intensity: {intensity:.2f}\n")
                f.write(f"Available engines: {', '.join(self.available_engines)}\n")
                f.write(f"Note: All TTS engines failed\n")
            print(f"    ⚠️  All engines failed. Text saved to: {fallback_file}")

class PremiumEmpathyEngine:
    """Premium empathy engine with high-quality voice synthesis"""
    
    def __init__(self, engine_type="edge"):
        self.emotion_detector = EmotionDetector()
        self.voice_modulator = PremiumVoiceModulator(engine_type)
        self.output_dir = "output"
        
        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
    
    async def process_text(self, text: str, output_filename: str = None) -> str:
        """Process text through the premium empathy engine"""
        print("\n" + "="*60)
        print("THE PREMIUM EMPATHY ENGINE")
        print("="*60)
        
        # Step 1: Analyze emotion
        print(f"\n Input Text: \"{text}\"")
        print("\n Analyzing emotion...")
        
        emotion, polarity, intensity = self.emotion_detector.analyze(text)
        
        print(f"\n Emotion Analysis:")
        print(f"  - Detected Emotion: {emotion.upper()}")
        print(f"  - Sentiment Polarity: {polarity:+.2f}")
        print(f"  - Emotional Intensity: {intensity:.1%}")
        
        # Step 2: Generate filename if not provided
        if not output_filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"{emotion}_{timestamp}.wav"
        
        output_path = os.path.join(self.output_dir, output_filename)
        
        # Step 3: Synthesize speech with premium quality
        print(f"\n Synthesizing premium quality speech...")
        await self.voice_modulator.synthesize(text, emotion, intensity, output_path)
        
        print(f"\n Processing complete!")
        print("="*60)
        
        return output_path

async def main():
    """CLI interface for the Premium Empathy Engine"""
    parser = argparse.ArgumentParser(
        description="The Premium Empathy Engine - High-quality emotionally aware TTS",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python empathy_engine_premium.py "I'm so happy to see you!"
  python empathy_engine_premium.py "This is terrible news." -o sad_news.wav --engine edge
  python empathy_engine_premium.py --demo --engine gtts
        """
    )
    
    parser.add_argument(
        "text",
        nargs="?",
        help="Text to convert to emotionally-aware speech"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output filename (default: auto-generated)"
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run demo with sample texts"
    )
    parser.add_argument(
        "--engine",
        choices=["edge", "gtts", "espeak"],
        default="edge",
        help="TTS engine to use (default: edge for best quality)"
    )
    
    args = parser.parse_args()
    
    engine = PremiumEmpathyEngine(engine_type=args.engine)
    
    if args.demo:
        # Demo mode with various emotional texts
        demo_texts = [
            ("I just got promoted! This is the best day ever!", "promotion_premium.wav"),
            ("I'm feeling really down today. Nothing seems to go right.", "sad_day_premium.wav"),
            ("The meeting is at 3 PM in conference room B.", "meeting_info_premium.wav"),
            ("Why does this keep happening? I'm so frustrated!", "frustrated_premium.wav"),
            ("Oh my goodness, I can't believe we won!", "excitement_premium.wav"),
        ]
        
        print("\n🎬 PREMIUM DEMO MODE - Processing sample texts...")
        for text, filename in demo_texts:
            await engine.process_text(text, filename)
            print("\n" + "-"*50)
    
    elif args.text:
        # Process single text input
        await engine.process_text(args.text, args.output)
    
    else:
        # Interactive mode
        print("\n🎭 THE PREMIUM EMPATHY ENGINE - Interactive Mode")
        print("Type 'quit' to exit\n")
        
        while True:
            try:
                text = input("\n💬 Enter text: ").strip()
                if text.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                if text:
                    await engine.process_text(text)
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
