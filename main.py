"""
The Empathy Engine MVP
A service that detects emotions in text and generates emotionally-modulated speech
"""

import os
import pyttsx3
from textblob import TextBlob
import argparse
from datetime import datetime
from typing import Dict, Tuple

class EmotionDetector:
    """Analyzes text and detects emotional content"""
    
    @staticmethod
    def analyze(text: str) -> Tuple[str, float, float]:
        """
        Analyze text for emotion and sentiment
        Returns: (emotion_category, polarity, intensity)
        """
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity  # -1 to 1
        subjectivity = blob.sentiment.subjectivity  # 0 to 1
        
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
        
        # Calculate intensity (0 to 1)
        intensity = min(abs(polarity) + (subjectivity * 0.3), 1.0)
        
        return emotion, polarity, intensity

class VoiceModulator:
    """Modulates TTS parameters based on emotion"""
    
    def __init__(self):
        self.engine = pyttsx3.init()
        self.base_rate = 150  # Words per minute
        self.base_volume = 0.9  # 0.0 to 1.0
        
        # Emotion-to-voice parameter mappings
        self.emotion_profiles = {
            "happy": {
                "rate_modifier": 1.15,  # 15% faster
                "volume_modifier": 1.1,  # 10% louder
                "pitch_shift": 20  # Higher pitch
            },
            "sad": {
                "rate_modifier": 0.85,  # 15% slower
                "volume_modifier": 0.85,  # 15% quieter
                "pitch_shift": -15  # Lower pitch
            },
            "frustrated": {
                "rate_modifier": 1.1,  # 10% faster
                "volume_modifier": 1.15,  # 15% louder
                "pitch_shift": -10  # Slightly lower pitch
            },
            "excited": {
                "rate_modifier": 1.25,  # 25% faster
                "volume_modifier": 1.2,  # 20% louder
                "pitch_shift": 25  # Higher pitch
            },
            "neutral": {
                "rate_modifier": 1.0,
                "volume_modifier": 1.0,
                "pitch_shift": 0
            }
        }
    
    def apply_emotion_settings(self, emotion: str, intensity: float):
        """Apply voice settings based on emotion and intensity"""
        profile = self.emotion_profiles.get(emotion, self.emotion_profiles["neutral"])
        
        # Scale modifications by intensity
        rate = self.base_rate * (1 + (profile["rate_modifier"] - 1) * intensity)
        volume = min(self.base_volume * (1 + (profile["volume_modifier"] - 1) * intensity), 1.0)
        
        # Set engine properties
        self.engine.setProperty('rate', int(rate))
        self.engine.setProperty('volume', volume)
        
        # Note: Pitch control varies by TTS engine and OS
        # This is a simplified approach
        voices = self.engine.getProperty('voices')
        if voices:
            # Try to select voice based on pitch preference
            if profile["pitch_shift"] > 0 and len(voices) > 1:
                self.engine.setProperty('voice', voices[1].id)  # Often a higher-pitched voice
            else:
                self.engine.setProperty('voice', voices[0].id)
        
        return rate, volume, profile["pitch_shift"]

    def synthesize(self, text: str, emotion: str, intensity: float, output_file: str):
        """Generate speech with emotional modulation"""
        rate, volume, pitch = self.apply_emotion_settings(emotion, intensity)
        
        print(f"  Voice Settings:")
        print(f"    - Rate: {rate:.0f} wpm")
        print(f"    - Volume: {volume:.2f}")
        print(f"    - Pitch adjustment: {pitch:+d}")
        
        # Generate speech
        self.engine.save_to_file(text, output_file)
        self.engine.runAndWait()

class EmpathyEngine:
    """Main service orchestrating emotion detection and voice synthesis"""
    
    def __init__(self):
        self.emotion_detector = EmotionDetector()
        self.voice_modulator = VoiceModulator()
        self.output_dir = "output"
        
        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
    
    def process_text(self, text: str, output_filename: str = None) -> str:
        """
        Process text through the empathy engine pipeline
        Returns: Path to generated audio file
        """
        print("\n" + "="*50)
        print("🎭 THE EMPATHY ENGINE")
        print("="*50)
        
        # Step 1: Analyze emotion
        print(f"\n📝 Input Text: \"{text}\"")
        print("\n🔍 Analyzing emotion...")
        
        emotion, polarity, intensity = self.emotion_detector.analyze(text)
        
        print(f"\n📊 Emotion Analysis:")
        print(f"  - Detected Emotion: {emotion.upper()}")
        print(f"  - Sentiment Polarity: {polarity:+.2f}")
        print(f"  - Emotional Intensity: {intensity:.2%}")
        
        # Step 2: Generate filename if not provided
        if not output_filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"{emotion}_{timestamp}.wav"
        
        output_path = os.path.join(self.output_dir, output_filename)
        
        # Step 3: Synthesize speech with emotion
        print(f"\n🎙️ Synthesizing speech with {emotion} emotion...")
        self.voice_modulator.synthesize(text, emotion, intensity, output_path)
        
        print(f"\n✅ Audio saved to: {output_path}")
        print("="*50)
        
        return output_path

def main():
    """CLI interface for the Empathy Engine"""
    parser = argparse.ArgumentParser(
        description="The Empathy Engine - Emotionally aware text-to-speech",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python empathy_engine.py "I'm so happy to see you!"
  python empathy_engine.py "This is terrible news." -o sad_news.wav
  python empathy_engine.py --demo
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
    
    args = parser.parse_args()
    
    engine = EmpathyEngine()
    
    if args.demo:
        # Demo mode with various emotional texts
        demo_texts = [
            ("I just got promoted! This is the best day ever!", "promotion.wav"),
            ("I'm feeling really down today. Nothing seems to go right.", "sad_day.wav"),
            ("The meeting is at 3 PM in conference room B.", "meeting_info.wav"),
            ("Why does this keep happening? I'm so frustrated!", "frustrated.wav"),
            ("Oh my goodness, I can't believe we won!", "excitement.wav"),
        ]
        
        print("\n🎬 DEMO MODE - Processing sample texts...")
        for text, filename in demo_texts:
            engine.process_text(text, filename)
            print("\n" + "-"*50)
    
    elif args.text:
        # Process single text input
        engine.process_text(args.text, args.output)
    
    else:
        # Interactive mode
        print("\n🎭 THE EMPATHY ENGINE - Interactive Mode")
        print("Type 'quit' to exit\n")
        
        while True:
            try:
                text = input("\n💬 Enter text: ").strip()
                if text.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                if text:
                    engine.process_text(text)
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()