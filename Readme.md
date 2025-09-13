# 🎭 The Empathy Engine MVP

A Python service that detects emotions in text and generates emotionally-modulated speech, bridging the gap between text-based sentiment and expressive, human-like audio output.

## 🌟 Features

- **Emotion Detection**: Analyzes text to detect 5 distinct emotional states (Happy, Sad, Frustrated, Excited, Neutral)
- **Voice Modulation**: Dynamically adjusts speech rate, volume, and pitch based on detected emotion
- **Intensity Scaling**: Modulates voice parameters proportionally to emotional intensity
- **Multiple Modes**: CLI, interactive, and demo modes for easy testing

## 📋 Prerequisites

- Python 3.7+
- pip (Python package manager)
- Working speakers/audio output

## 🚀 Quick Setup

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd empathy-engine
```

2. **Create a virtual environment** (recommended)
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Download TextBlob corpora** (required for sentiment analysis)
```bash
python -m textblob.download_corpora
```

## 💻 Usage

### Interactive Mode
Run without arguments for interactive text input:
```bash
python empathy_engine.py
```

### Direct Text Input
Process a single text:
```bash
python empathy_engine.py "I'm so excited about this project!"
```

### Demo Mode
Run with sample texts showcasing different emotions:
```bash
python empathy_engine.py --demo
```

### Custom Output
Specify output filename:
```bash
python empathy_engine.py "This is amazing news!" -o good_news.wav
```

## 🎯 How It Works

### 1. Emotion Detection
- Uses TextBlob for sentiment analysis
- Calculates polarity (-1 to +1) and subjectivity (0 to 1)
- Maps sentiment scores to emotion categories

### 2. Emotion-to-Voice Mapping

| Emotion | Rate Change | Volume Change | Pitch Direction |
|---------|------------|---------------|-----------------|
| Happy | +15% | +10% | Higher (+20) |
| Sad | -15% | -15% | Lower (-15) |
| Frustrated | +10% | +15% | Lower (-10) |
| Excited | +25% | +20% | Higher (+25) |
| Neutral | 0% | 0% | No change |

### 3. Intensity Scaling
- Emotional intensity (0-1) scales the voice modifications
- Stronger emotions = more pronounced voice changes

## 📂 Project Structure
```
empathy-engine/
├── empathy_engine.py    # Main application
├── requirements.txt      # Python dependencies
├── README.md            # This file
└── output/              # Generated audio files (created automatically)
```

## 🔧 Design Choices

1. **TextBlob for Sentiment**: Chosen for simplicity and no API requirements. Provides quick, offline sentiment analysis.

2. **pyttsx3 for TTS**: Platform-independent, works offline, and allows real-time parameter adjustment.

3. **Emotion Categories**: Five emotions provide good coverage while keeping the MVP simple:
   - Happy/Sad: Basic positive/negative
   - Frustrated: Captures anger/annoyance
   - Excited: High-energy positive
   - Neutral: Baseline/informational

4. **Parameter Modulation**: 
   - **Rate**: Most noticeable change, reflects energy level
   - **Volume**: Subtle but effective for emotional emphasis
   - **Pitch**: Limited by pyttsx3, but voice selection provides variation

## 🚦 Testing Examples

Try these texts to see the emotion engine in action:

- **Happy**: "This is wonderful! I couldn't be happier!"
- **Sad**: "I'm feeling really down today."
- **Frustrated**: "Why won't this work? This is so annoying!"
- **Excited**: "OH MY GOD! We actually did it! This is incredible!"
- **Neutral**: "The meeting is scheduled for 3 PM."

## 🎯 Future Enhancements

- [ ] Web interface with real-time audio playback
- [ ] More granular emotions (surprised, concerned, angry)
- [ ] SSML integration for fine-grained control
- [ ] Multiple voice profiles
- [ ] Emotion mixing (e.g., happy + excited)
- [ ] Better pitch control with advanced TTS engines

## 📝 Notes

- Audio files are saved in WAV format in the `output/` directory
- The actual pitch modulation depends on available system voices
- First run may take longer as TextBlob downloads required corpora

## 🤝 Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## 📄 License

MIT License - feel free to use this code for your projects!