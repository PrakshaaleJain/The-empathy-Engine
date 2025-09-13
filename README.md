# 🎭 The Premium Empathy Engine

An advanced emotionally-aware text-to-speech engine with multiple high-quality voice options.

## 🌟 Voice Quality Options (Best to Basic)

1. **Microsoft Edge TTS** (Highest Quality) - Requires: `edge-tts`
   - Natural human-like voices
   - Emotional speaking styles
   - Multiple voice personalities

2. **Google Text-to-Speech** (High Quality) - Requires: `gtts`
   - Very natural sounding
   - Good emotional variation
   - Requires internet connection

3. **Enhanced Espeak** (Good Quality) - Built-in
   - Improved voice selection
   - Better emotional modulation
   - Works completely offline

## 🚀 Quick Start

### Option 1: Virtual Environment (Recommended)
```bash
# Create virtual environment
python3 -m venv empathy_env
source empathy_env/bin/activate

# Install premium packages
pip install textblob gtts edge-tts pygame

# Test with best quality
python3 empathy_engine_premium.py "Hello world!" --engine edge
```

### Option 2: System Installation
```bash
# Install system packages
sudo apt install espeak ffmpeg python3-pip

# Install Python packages (if allowed)
pip install --break-system-packages textblob gtts edge-tts pygame

# Or use the setup script
./setup_premium.sh
```

### Option 3: Minimal Setup (Works immediately)
```bash
# Just install textblob for basic functionality
pip install --break-system-packages textblob

# Use with enhanced espeak (already installed)
python3 empathy_engine_premium.py "Hello!" --engine espeak
```

## 🎯 Usage Examples

```bash
# Best quality (Microsoft Edge TTS)
python3 empathy_engine_premium.py "I'm so excited!" --engine edge

# Good quality (Google TTS) 
python3 empathy_engine_premium.py "This is amazing!" --engine gtts

# Enhanced offline quality
python3 empathy_engine_premium.py "Hello there!" --engine espeak

# Run demo with all emotion types
python3 empathy_engine_premium.py --demo --engine edge

# Interactive mode
python3 empathy_engine_premium.py --engine edge
```

## 🎨 Supported Emotions

- **Happy**: Cheerful, upbeat voice
- **Excited**: Energetic, fast-paced speech  
- **Sad**: Gentle, slower, lower pitch
- **Frustrated**: Firm, slightly aggressive tone
- **Neutral**: Balanced, professional tone

## 📁 Output

Audio files are saved in the `output/` directory as high-quality `.wav` files.

## 🔧 Troubleshooting

1. **"Module not found" errors**: Install missing packages in a virtual environment
2. **"Audio file not created"**: Check internet connection for cloud TTS engines
3. **Robotic voice**: Try different engines (edge > gtts > espeak)
4. **Permission errors**: Use virtual environment instead of system packages

## 🆚 Voice Quality Comparison

| Engine | Quality | Internet | Setup | Best For |
|--------|---------|----------|-------|----------|
| Edge TTS | ⭐⭐⭐⭐⭐ | Required | Medium | Production use |
| Google TTS | ⭐⭐⭐⭐ | Required | Easy | General use |  
| Enhanced Espeak | ⭐⭐⭐ | No | Minimal | Offline/testing |

## I have taken the help to AI in some portion of the code rather than writing the whole code from sccrath by them.