# AUDIO TRANSCRIPTION TOOL
## Converting Audio Files to Text with Whisper AI

---

## OVERVIEW

This tool automatically converts (transcribes) audio and video files to text.
It uses OpenAI's Whisper AI technology and is completely free.

**Features:**
- ✅ Works completely offline (no internet required)
- ✅ Supports 100+ languages ​​(including Turkish)
- ✅ Unlimited use
- ✅ Batch file processing
- ✅ Timestamped output
- ✅ SRT subtitle format support
- ✅ High accuracy rate

---

## INSTALLATION

### Step 1: Python Installation
Python 3.8 or higher is required.
To download: https://www.python.org/downloads/

### Step 2: Install Necessary Packages
Open the command prompt and run the following commands:

```bash
pip install openai-whisper
pip install torch
```
**Note:** The initial installation may require a 500MB-1GB download.

### Step 3: Download the Script
Save the `trankript.py` file to a folder.

---

## USAGE

### Basic Usage

```bash
python transkript.py -i FILE_PATH -o OUTPUT_FOLDER
```

### Examples

**1. Transcribe a single audio file:**
```bash
python transkript.py -i audio.mp3 -o transcripts/
```

**2. Process all audio files in the folder:**
```bash
python transcript.py -i audio_folder/ -o transcripts/
```
**3. For Turkish audio (recommended):**
```bash
python transcript.py -i audio.mp3 -o transcripts/ -l tr
```
**4. Create a timestamped transcript:**
```bash
python transcript.py -i audio.mp3 -o transcripts/ -t
```
**5. Higher quality (slower):**
```bash
python transcript.py -i audio.mp3 -o transcripts/ -s medium
```
**6. All options together:**
```bash
python transcript.py -i audio_folder/ -o transcripts/ -l tr -s medium -t
```

---
## DESCRIPTION OF PARAMETERS

### Required Parameters:
- `-i, --input`: Audio file or folder path
- `-o, --output`: Folder where transcripts will be saved

### Optional Parameters:

**-s, --model-size** (Model size)
- `tiny` - Fastest, low accuracy (~1GB RAM, 32x faster)
- `base` - Balanced (Default) (~1GB RAM)
- `small` - Good accuracy (~2GB RAM)
- `medium` - High accuracy (~5GB RAM) **[RECOMMENDED]**
- `large` - Highest accuracy (~10GB RAM, most (slow)

**-l, --language** (Language code)
- Example: `tr` (Turkish), `en` (English), `de` (German)
- Automatically detected if not specified
- Specifying the language improves accuracy

**-t, --timestamps** (Timestamps)
- Adds time information to the transcript
- Creates an SRT subtitle file
- Compatible with video editors

---

## SUPPORTED FILE FORMATS

**Audio Formats:**
- MP3
- WAV
- M4A
- OGG
- FLAC
- AAC
- WMA

**Video Formats:**
- MP4 (only the audio part is processed)

---

## OUTPUT FILES

The script creates two types of files:

### 1. Text File (.txt)
```
File: example_audio.mp3
Date: 2024-12-08 14:30:00
Detected language: tr
===============================================================================

=== TIME-STAMPED TRANSCRIPT === (optional)

[00:00:00 - 00:00:05] Hello, this is a test recording. [00:00:05 - 00:00:10] We are transcribing using Whisper AI.

================================================================================
=== FULL TEXT ===

Hello, this is a test recording. We are transcribing using Whisper AI.
```
### 2. SRT Subtitle File (.srt) - Only with -t parameter
```
1
00:00:00,000 --> 00:00:05,000
Hello, this is a test recording.

2
00:00:05,000 --> 00:00:10,000
We are transcribing using Whisper AI.
```

---

## PERFORMANCE TIPS

### Model Selection:
- **For fast processing:** `tiny` or `base`
- **Quality-speed balance:** `small`
- **Best results:** `medium` (recommended)
- **Professional use:** `large`

### Processing Times (approx.):
- **tiny**: 1 minute of audio = ~5 seconds
- **base**: 1 minute of audio = ~10 seconds
- **small**: 1 minute of audio = ~20 seconds
- **medium**: 1 minute of audio = ~40 seconds
- **large**: 1 minute of audio = ~2 minutes

**Note:** Times vary depending on computer hardware.

### Memory Requirements:
- tiny/base: 1-2 GB RAM
- small: 2-3 GB RAM
- medium: 5-6 GB RAM
- large: 10+ GB RAM

---
## TROUBLESHOOTING

### "openai-whisper package not installed" error:
```bash
pip install openai-whisper
```
### "torch" error:
```bash
pip install torch
```
### Model cannot be downloaded:
Check your internet connection. The model needs to be downloaded on the first use.

### Audio file not processed:
- Ensure the file format is supported.
- If the file path contains Turkish characters, replace them with English characters.
- Ensure the file is not corrupted.

### Running too slowly:
- Use a smaller model (`-s tiny` or `-s base`).
- Install CUDA for GPU support (optional, advanced).

### Incorrect language detected:
Explicitly specify the language parameter: `-l tr`

---

## LANGUAGE CODES

Commonly used language codes:

- `tr` - Turkish
- `en` - English
- `de` - German
- `fr` - French
- `es` - Spanish
- `it` - Italian
- `pt` - Portuguese
- `ru` - Russian
- `zh` - Chinese
- `ja` - Japanese
- `ko` - Korean
- `ar` - Arabic

A total of 100+ languages ​​are supported.
## EXAMPLE USAGE SCENARIOS

### Scenario 1: Transcribing a Podcast
```bash
python transcript.py -i podcast.mp3 -o transcripts/ -l tr -s medium -t
```
### Scenario 2: Meeting Recording
```bash
python transcript.py -i meeting.m4a -o meeting_notes/ -l tr -s small
```

### Scenario 3: Creating Video Subtitles
```bash
python transcript.py -i video.mp4 -o subtitles/ -l tr -s medium -t
```

### Scenario 4: Batch File Processing
```bash
python transcript.py -i audio_archive/ -o all_transcripts/ -l tr -s base
```

---

## FREQUENTLY FREQUENTLY ASKED QUESTIONS

**Q: Is an internet connection required?**
A: Only during the initial setup. After that, it works completely offline.

**Q: Is it paid?**
A: No, it's completely free and open source.

**Q: How many minutes of audio can it process?**
A: No limit. It can process hours of audio.

**Q: What is the accuracy rate?**
A: 90-95% with high-quality recordings. 70-85% with noisy recordings.

**Q: Is a GPU required?**
A: No, it also works with a CPU. It will be faster if you have a GPU.

**Q: Does it work on Mac/Linux?**
A: Yes, Windows, Mac, and Linux are supported.

---

## TECHNICAL DETAILS

**Technology Used:** OpenAI Whisper
**License:** MIT (Open Source)
**Python Version:** 3.8+
**Main Dependencies:**

- openai-whisper

- torch
- numpy

- ffmpeg (automatically installed)

---

## SUPPORT AND UPDATES

**Official Whisper Repository:**

https://github.com/openai/whisper

**Official Python Website:**

https://www.python.org/

---

## RELEASE DATE

December 2024

---

## QUICK START SUMMARY

1. Install Python
2. Run `pip install openai-whisper`
3. Run `python transcript.py -i audio.mp3 -o` Start with the command `ciktilar/ -l tr`
4. Find the results in the `ciktilar/` folder

Enjoy! 🎙️✨
