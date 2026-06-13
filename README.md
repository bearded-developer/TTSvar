# TTSvar — Text to Speech Studio

> **TTS** (Text-to-Speech) × **Svar** (स्वर — tone/voice in Sanskrit)

A full-featured, local text-to-speech web application with narrator styles, emotional delivery, accent & gender selection, and background music mixing — all running on your own machine.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![edge-tts](https://img.shields.io/badge/edge--tts-latest-orange)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## ✨ Features

| Feature | Details |
|---|---|
| 🎭 **Narrator Styles** | Choose from 6 voice characters — Storyteller, Movie Narrator, Audiobook Reader, News Anchor, Bot/Assistant, Professional |
| 😊 **Emotional Delivery** | Add emotional tone — Neutral, Warm, Dramatic, Energetic, Gentle, Formal, Excited |
| 🌍 **Accent & Gender** | 5 English accents (US, UK, Indian, Australian, Canadian) × Male/Female voice |
| ⚡ **Speed Control** | Adjust playback speed from 0.3× to 3.0× |
| 🎵 **Background Music** | Apply ambient music with volume control (auto-loop, crossfade) |
| 🎧 **Instant Preview** | Stream generated audio directly in the browser |
| ⬇️ **Download MP3** | Download finished audio as a high-quality 192k MP3 |
| 🔒 **100% Local** | All processing runs on your machine — no cloud services, no data leakage |

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+**
- **FFmpeg** (required for audio mixing with background music)

<details>
<summary><b>Install FFmpeg on Windows</b></summary>

```powershell
# Using winget (recommended)
winget install Gyan.FFmpeg

# Or download manually from https://ffmpeg.org/download.html
```

</details>

<details>
<summary><b>Install FFmpeg on macOS</b></summary>

```bash
brew install ffmpeg
```

</details>

<details>
<summary><b>Install FFmpeg on Linux</b></summary>

```bash
sudo apt install ffmpeg
```

</details>

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/TTSvar.git
cd TTSvar

# 2. Create a virtual environment (recommended)
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python app.py
```

Open **http://localhost:5000** in your browser.

---

## 🧠 How It Works

### Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Browser   │────▶│  Flask API   │────▶│  edge-tts   │
│  (HTML/JS)  │     │  (app.py)    │     │  (TTS eng.) │
└─────────────┘     └──────────────┘     └──────┬──────┘
                     │                          │
                     │                          ▼
                     │                   ┌──────────────┐
                     │                   │ Audio & Mix  │
                     │                   │  (pydub +    │
                     │                   │   ffmpeg)    │
                     │                   └──────┬───────┘
                     │                          │
                     ▼                          ▼
               ┌─────────────────────────────────────┐
               │          output MP3 file             │
               └─────────────────────────────────────┘
```

### Processing Pipeline

1. **Text input** — Script pasted by the user
2. **Narrator Style** — Defines the base voice character and its rate/pitch profile
3. **Accent + Gender** — Selects the regional voice and gender
4. **Emotion** — Applies emotional rate/pitch adjustments on top of the narrator style
5. **Speed** — Multiplies final rate by the speed factor
6. **edge-tts** — Generates raw speech audio via Microsoft Edge's TTS engine
7. **Background Music** — If selected, loops and crossfades music under the speech
8. **Export** — Final mixed audio saved as 192kbps MP3

---

## 🎛️ Configuration Reference

### Narrator Style Presets

| Preset | Default Voice | Rate | Pitch | Best For |
|---|---|---|---|---|
| Storyteller | Guy (US Male) | -10% | -5Hz | Expressive narration |
| Movie Narrator | Davis (US Male) | -15% | -10Hz | Trailer / dramatic |
| Audiobook Reader | Jenny (US Female) | -5% | -3Hz | Long-form reading |
| News Anchor | Tony (US Male) | 0% | 0Hz | Broadcast / formal |
| Bot / Assistant | Sara (US Female) | 0% | 0Hz | Digital assistant |
| Professional | Sara (US Female) | 0% | 0Hz | Corporate / polished |

### Emotion Adjustments

| Emotion | Rate Change | Pitch Change | Effect |
|---|---|---|---|
| Neutral | 0% | 0Hz | No adjustment |
| Warm | -5% | -3Hz | Slightly slower, warmer |
| Dramatic | -15% | -15Hz | Slow, deep, intense |
| Energetic | +15% | +10Hz | Faster, brighter |
| Gentle | -20% | -8Hz | Slow, soft, soothing |
| Formal | -5% | +5Hz | Measured, crisp |
| Excited | +25% | +20Hz | Fast, high-pitched |

> **Note:** Emotion adjustments are *added* to the Narrator Style's base rate/pitch. For example, "Dramatic" + "Movie Narrator" combines -15% + -15% = -30% rate and -15Hz + -10Hz = -25Hz pitch.

### Available Accents

| Accent | Flag | Male Voice | Female Voice |
|---|---|---|---|
| US English | 🇺🇸 | Guy / Brian / Andrew | Jenny / Aria / Emma |
| British English | 🇬🇧 | Ryan / Thomas | Sonia / Libby / Maisie |
| Indian English | 🇮🇳 | Prabhat | Neerja |
| Australian English | 🇦🇺 | William | Natasha |
| Canadian English | 🇨🇦 | Liam | Clara |

---

## 📁 Project Structure

```
TTSvar/
├── app.py                  # Flask backend — API endpoints & TTS logic
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── templates/
│   └── index.html          # Single-page frontend (HTML)
├── static/
│   ├── css/
│   │   └── style.css       # Dark theme UI styles
│   ├── js/
│   │   └── app.js          # Frontend logic & API calls
│   └── music/              # 📥 Drop your .mp3 files here
│       ├── calm.mp3        # Calm & Ambient
│       ├── happy.mp3       # Happy & Upbeat
│       ├── sad.mp3         # Sad & Emotional
│       ├── suspense.mp3    # Suspense & Thriller
│       ├── cinematic.mp3   # Cinematic & Epic
│       ├── relaxing.mp3    # Relaxing & Peaceful
│       └── dreamy.mp3      # Dreamy & Soft
└── generated/              # Auto-generated — output MP3s
```

---

## 🎵 Adding Background Music

Place `.mp3` files in the `static/music/` directory with these filenames:

| Filename | Category |
|---|---|
| `calm.mp3` | 🌿 Calm & Ambient |
| `happy.mp3` | ☀️ Happy & Upbeat |
| `sad.mp3` | 🌧️ Sad & Emotional |
| `suspense.mp3` | ⚡ Suspense & Thriller |
| `cinematic.mp3` | 🎬 Cinematic & Epic |
| `relaxing.mp3` | 🧘 Relaxing & Peaceful |
| `dreamy.mp3` | 🌙 Dreamy & Soft |

Music automatically loops if shorter than the speech and applies 3-second fade-in/fade-out.

---

## 📡 API Reference

### `GET /api/voice-presets`

Returns all available narrator styles, accents, emotions, and music options.

**Response:**
```json
{
  "presets": {
    "storyteller": { "label": "Storyteller", "voice": "en-US-GuyNeural", "desc": "Expressive, warm narration" }
  },
  "accents": {
    "us": { "label": "🇺🇸 US English", "flag": "🇺🇸", "male": "en-US-GuyNeural", "female": "en-US-JennyNeural", "alt_voices": [] }
  },
  "emotions": {
    "neutral": { "label": "Neutral", "rate": "0%", "pitch": "0Hz" }
  },
  "music_categories": {
    "none": { "label": "🎵 No Music", "available": true, "icon": "🔇" }
  }
}
```

### `POST /api/generate`

Generates audio from text with selected options.

**Request body:**
```json
{
  "script": "Your text here...",
  "preset": "storyteller",
  "accent": "us",
  "gender": "male",
  "emotion": "dramatic",
  "speed": 1.0,
  "music_category": "calm",
  "music_volume": 30
}
```

**Response:**
```json
{
  "success": true,
  "filename": "final_abc12345.mp3",
  "download_url": "/api/download/final_abc12345.mp3",
  "preview_url": "/api/preview/final_abc12345.mp3"
}
```

### `GET /api/download/<filename>`

Downloads the generated MP3 file.

### `GET /api/preview/<filename>`

Streams the generated MP3 for browser playback.

---

## 💻 Tech Stack

| Component | Technology | Role |
|---|---|---|
| **Backend** | Python + Flask | REST API server |
| **TTS Engine** | edge-tts | Microsoft Edge online TTS (free, no API key) |
| **Audio Processing** | pydub + FFmpeg | MP3 export, music mixing, crossfade |
| **Frontend** | Vanilla HTML/CSS/JS | No framework needed — fast, lightweight |
| **UI Theme** | Custom dark theme | Modern gradient-based UI with CSS variables |

---

## 🧪 Running Tests

```bash
# Start the server
python app.py

# In another terminal, test the API
curl http://localhost:5000/api/voice-presets

# Generate test audio
curl -X POST http://localhost:5000/api/generate \
  -H "Content-Type: application/json" \
  -d '{"script":"Hello world","preset":"storyteller","accent":"us","gender":"male","emotion":"neutral","speed":1.0,"music_category":"none","music_volume":0}'
```

---

## 🤝 Contributing

Contributions are welcome! Here are some ideas:

- [ ] Add more accents (ES, FR, DE, JP, CN voices)
- [ ] Multi-language support (non-English scripts)
- [ ] Save/load preset profiles
- [ ] Batch processing multiple scripts
- [ ] Export as WAV / FLAC
- [ ] Voice cloning support
- [ ] Real-time streaming (WebSocket)
- [ ] Docker containerization

---

## 📜 License

MIT License — free to use, modify, and distribute.

---

## 🙏 Credits

- [edge-tts](https://github.com/rany2/edge-tts) — Free Microsoft Edge TTS engine wrapper
- [pydub](https://github.com/jiaaro/pydub) — Audio processing library
- Microsoft — For providing free Neural TTS voices via Edge

---

<p align="center">Made with 🎙️ by <a href="https://github.com/YOUR_USERNAME">Your Name</a></p>