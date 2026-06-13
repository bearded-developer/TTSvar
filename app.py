import os
import shutil
import subprocess
import sys
import uuid
import asyncio
import edge_tts
from flask import Flask, request, jsonify, send_file, render_template


def find_ffmpeg():
    """Find ffmpeg executable by checking PATH and common install locations."""
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg:
        return ffmpeg
    
    common_paths = [
        os.path.expanduser("~\\AppData\\Local\\Microsoft\\WinGet\\Packages\\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\\ffmpeg-*-full_build\\bin\\ffmpeg.exe"),
        "C:\\ProgramData\\chocolatey\\bin\\ffmpeg.exe",
        "C:\\Program Files\\ffmpeg\\bin\\ffmpeg.exe",
        "C:\\ffmpeg\\bin\\ffmpeg.exe",
    ]
    
    import glob
    for pattern in common_paths:
        results = glob.glob(pattern)
        if results:
            return results[0]
    
    return None


def find_ffprobe():
    """Find ffprobe executable."""
    ffprobe = shutil.which("ffprobe")
    if ffprobe:
        return ffprobe
    
    ffmpeg_path = find_ffmpeg()
    if ffmpeg_path:
        ffprobe_path = ffmpeg_path.replace("ffmpeg.exe", "ffprobe.exe")
        if os.path.exists(ffprobe_path):
            return ffprobe_path
    
    return None


ffmpeg_path = find_ffmpeg()
if ffmpeg_path:
    os.environ["FFMPEG_BINARY"] = ffmpeg_path
    os.environ["PATH"] = os.path.dirname(ffmpeg_path) + os.pathsep + os.environ.get("PATH", "")

from pydub import AudioSegment
if ffmpeg_path:
    AudioSegment.converter = ffmpeg_path

ffprobe_path = find_ffprobe()
if ffprobe_path:
    AudioSegment.ffprobe = ffprobe_path

app = Flask(__name__)
GENERATED_DIR = "generated"
MUSIC_DIR = "static/music"
os.makedirs(GENERATED_DIR, exist_ok=True)
os.makedirs(MUSIC_DIR, exist_ok=True)

# Narrator Style presets — defines the voice character (who is speaking)
VOICE_PRESETS = {
    "storyteller": {
        "voice": "en-US-GuyNeural",
        "rate": "-10%",
        "pitch": "-5Hz",
        "label": "Storyteller",
        "desc": "Expressive, warm narration"
    },
    "movie_narrator": {
        "voice": "en-US-DavisNeural",
        "rate": "-15%",
        "pitch": "-10Hz",
        "label": "Movie Narrator",
        "desc": "Deep, dramatic movie trailer voice"
    },
    "audiobook": {
        "voice": "en-US-JennyNeural",
        "rate": "-5%",
        "pitch": "-3Hz",
        "label": "Audiobook Reader",
        "desc": "Clear, engaging reading"
    },
    "news_anchor": {
        "voice": "en-US-TonyNeural",
        "rate": "0%",
        "pitch": "0Hz",
        "label": "News Anchor",
        "desc": "Formal broadcast style"
    },
    "bot_assistant": {
        "voice": "en-US-SaraNeural",
        "rate": "0%",
        "pitch": "0Hz",
        "label": "Bot / Assistant",
        "desc": "Neutral digital assistant"
    },
    "professional": {
        "voice": "en-US-SaraNeural",
        "rate": "0%",
        "pitch": "0Hz",
        "label": "Professional",
        "desc": "Polished corporate voice"
    }
}

# Expanded accent options with gender selection
ACCENT_VOICES = {
    "us": {
        "label": "🇺🇸 US English",
        "flag": "🇺🇸",
        "male": "en-US-GuyNeural",
        "female": "en-US-JennyNeural",
        "alt_voices": ["en-US-BrianNeural", "en-US-AndrewNeural", "en-US-AriaNeural", "en-US-EmmaNeural"]
    },
    "uk": {
        "label": "🇬🇧 British English",
        "flag": "🇬🇧",
        "male": "en-GB-RyanNeural",
        "female": "en-GB-SoniaNeural",
        "alt_voices": ["en-GB-ThomasNeural", "en-GB-LibbyNeural", "en-GB-MaisieNeural"]
    },
    "in": {
        "label": "🇮🇳 Indian English",
        "flag": "🇮🇳",
        "male": "en-IN-PrabhatNeural",
        "female": "en-IN-NeerjaNeural",
        "alt_voices": ["en-IN-NeerjaExpressiveNeural"]
    },
    "au": {
        "label": "🇦🇺 Australian English",
        "flag": "🇦🇺",
        "male": "en-AU-WilliamMultilingualNeural",
        "female": "en-AU-NatashaNeural",
        "alt_voices": []
    },
    "ca": {
        "label": "🇨🇦 Canadian English",
        "flag": "🇨🇦",
        "male": "en-CA-LiamNeural",
        "female": "en-CA-ClaraNeural",
        "alt_voices": []
    }
}

# Emotional delivery adjustments — applies on top of the narrator style
EMOTION_TWEAKS = {
    "neutral": {"rate": "0%", "pitch": "0Hz", "label": "Neutral"},
    "warm": {"rate": "-5%", "pitch": "-3Hz", "label": "Warm"},
    "dramatic": {"rate": "-15%", "pitch": "-15Hz", "label": "Dramatic"},
    "energetic": {"rate": "+15%", "pitch": "+10Hz", "label": "Energetic"},
    "gentle": {"rate": "-20%", "pitch": "-8Hz", "label": "Gentle"},
    "formal": {"rate": "-5%", "pitch": "+5Hz", "label": "Formal"},
    "excited": {"rate": "+25%", "pitch": "+20Hz", "label": "Excited"},
}

# Background music categories
MUSIC_CATEGORIES = {
    "none": {"label": "🎵 No Music", "file": None, "icon": "🔇"},
    "calm": {"label": "🌿 Calm & Ambient", "file": "calm.mp3", "icon": "🌿"},
    "happy": {"label": "☀️ Happy & Upbeat", "file": "happy.mp3", "icon": "☀️"},
    "sad": {"label": "🌧️ Sad & Emotional", "file": "sad.mp3", "icon": "🌧️"},
    "suspense": {"label": "⚡ Suspense & Thriller", "file": "suspense.mp3", "icon": "⚡"},
    "cinematic": {"label": "🎬 Cinematic & Epic", "file": "cinematic.mp3", "icon": "🎬"},
    "relaxing": {"label": "🧘 Relaxing & Peaceful", "file": "relaxing.mp3", "icon": "🧘"},
    "dreamy": {"label": "🌙 Dreamy & Soft", "file": "dreamy.mp3", "icon": "🌙"}
}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/voice-presets', methods=['GET'])
def get_voice_presets():
    presets = {k: {
        "label": v["label"],
        "voice": v["voice"],
        "desc": v["desc"]
    } for k, v in VOICE_PRESETS.items()}
    
    accents = {}
    for k, v in ACCENT_VOICES.items():
        accents[k] = {
            "label": v["label"],
            "flag": v["flag"],
            "male": v["male"],
            "female": v["female"],
            "alt_voices": v["alt_voices"]
        }
    
    emotions = {k: {"label": v["label"], "rate": v["rate"], "pitch": v["pitch"]} for k, v in EMOTION_TWEAKS.items()}
    
    music_options = {}
    for key, info in MUSIC_CATEGORIES.items():
        if key == "none":
            music_options[key] = {"label": info["label"], "available": True, "icon": info["icon"]}
        else:
            filepath = os.path.join(MUSIC_DIR, info["file"])
            music_options[key] = {"label": info["label"], "available": os.path.exists(filepath), "icon": info["icon"]}
    
    return jsonify({
        "presets": presets,
        "accents": accents,
        "emotions": emotions,
        "music_categories": music_options
    })


@app.route('/api/generate', methods=['POST'])
def generate_audio():
    data = request.json
    script = data.get('script', '').strip()
    
    if not script:
        return jsonify({"error": "Script cannot be empty"}), 400
    
    if len(script) > 10000:
        return jsonify({"error": "Script is too long (max 10000 characters)"}), 400
    
    try:
        preset_key = data.get('preset', 'storyteller')
        accent_key = data.get('accent', 'us')
        gender = data.get('gender', 'male')
        emotion_key = data.get('emotion', 'neutral')
        speed = float(data.get('speed', 1.0))
        music_category = data.get('music_category', 'none')
        music_volume = float(data.get('music_volume', 30)) / 100.0
        
        speed = max(0.3, min(3.0, speed))
        
        # Get narrator style preset
        if preset_key in VOICE_PRESETS:
            preset = VOICE_PRESETS[preset_key]
        else:
            preset = VOICE_PRESETS["storyteller"]
        
        # Get voice from accent + gender
        if accent_key in ACCENT_VOICES:
            accent_info = ACCENT_VOICES[accent_key]
            voice = accent_info.get(gender, accent_info["male"])
        else:
            voice = preset["voice"]
        
        # Start with preset rate/pitch
        rate_str = preset.get("rate", "0%")
        pitch_str = preset.get("pitch", "0Hz")
        
        # Apply emotion tweaks on top of the narrator style
        if emotion_key in EMOTION_TWEAKS:
            emotion = EMOTION_TWEAKS[emotion_key]
            preset_rate_val = parse_percentage(rate_str)
            emotion_rate_val = parse_percentage(emotion["rate"])
            combined_rate = preset_rate_val + emotion_rate_val
            rate_str = f"{combined_rate:+d}%"
            
            preset_pitch_val = parse_hz(pitch_str)
            emotion_pitch_val = parse_hz(emotion["pitch"])
            combined_pitch = preset_pitch_val + emotion_pitch_val
            pitch_str = f"{combined_pitch:+d}Hz"
        
        # Apply speed: edge-tts rate is percentage change.
        # speed=1.0 → 0% (normal), speed=0.5 → -50% (slower), speed=2.0 → +100% (faster)
        # Add to any preset/emotion rate adjustments
        base_rate = parse_percentage(rate_str)
        speed_rate = int((speed - 1.0) * 100)
        final_rate = base_rate + speed_rate
        rate_str = f"{final_rate:+d}%"
        
        file_id = str(uuid.uuid4())[:8]
        voice_filename = f"voice_{file_id}.mp3"
        output_filename = f"final_{file_id}.mp3"
        voice_path = os.path.join(GENERATED_DIR, voice_filename)
        output_path = os.path.join(GENERATED_DIR, output_filename)
        
        async def generate_speech():
            communicate = edge_tts.Communicate(script, voice, rate=rate_str, pitch=pitch_str)
            await communicate.save(voice_path)
        
        asyncio.run(generate_speech())
        
        speech_audio = AudioSegment.from_mp3(voice_path)
        
        if music_category != 'none' and music_category in MUSIC_CATEGORIES:
            music_info = MUSIC_CATEGORIES[music_category]
            if music_info["file"]:
                music_path = os.path.join(MUSIC_DIR, music_info["file"])
                if os.path.exists(music_path):
                    try:
                        music_audio = AudioSegment.from_mp3(music_path)
                        
                        if len(music_audio) < len(speech_audio):
                            repeats = (len(speech_audio) // len(music_audio)) + 1
                            music_audio = music_audio * repeats
                        
                        music_audio = music_audio[:len(speech_audio)]
                        
                        fade_duration = 3000
                        if len(music_audio) > fade_duration * 2:
                            music_audio = music_audio.fade_in(fade_duration).fade_out(fade_duration)
                        
                        music_audio = music_audio - (20 * (1 - music_volume))
                        speech_lowered = speech_audio - 3
                        combined = music_audio.overlay(speech_lowered)
                        combined.export(output_path, format="mp3", bitrate="192k")
                    except Exception:
                        speech_audio.export(output_path, format="mp3", bitrate="192k")
                else:
                    speech_audio.export(output_path, format="mp3", bitrate="192k")
            else:
                speech_audio.export(output_path, format="mp3", bitrate="192k")
        else:
            speech_audio.export(output_path, format="mp3", bitrate="192k")
        
        if os.path.exists(voice_path):
            os.remove(voice_path)
        
        return jsonify({
            "success": True,
            "filename": output_filename,
            "download_url": f"/api/download/{output_filename}",
            "preview_url": f"/api/preview/{output_filename}"
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/download/<filename>')
def download_audio(filename):
    filepath = os.path.join(GENERATED_DIR, filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True, download_name=filename, mimetype="audio/mpeg")
    return jsonify({"error": "File not found"}), 404


@app.route('/api/preview/<filename>')
def preview_audio(filename):
    filepath = os.path.join(GENERATED_DIR, filename)
    if os.path.exists(filepath):
        return send_file(filepath, mimetype="audio/mpeg")
    return jsonify({"error": "File not found"}), 404


def parse_percentage(val_str):
    if not val_str:
        return 0
    val_str = val_str.replace('%', '').strip()
    try:
        return int(val_str)
    except ValueError:
        return 0


def parse_hz(val_str):
    if not val_str:
        return 0
    val_str = val_str.replace('Hz', '').strip()
    try:
        return int(val_str)
    except ValueError:
        return 0


if __name__ == '__main__':
    print("=" * 60)
    print("  🎙️  Text to Speech Studio")
    print("   Narrator Styles · Emotions · Accents · Music")
    print("=" * 60)
    print(f"  Open: http://localhost:5000")
    print(f"  Music folder: {os.path.abspath(MUSIC_DIR)}")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)