# Local2Stream GUI 🎵

Transfer your local music collection to streaming platforms with intelligent matching and fuzzy search capabilities - now with a user-friendly graphical interface!

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Spotify](https://img.shields.io/badge/Platform-Spotify-1DB954.svg)](https://spotify.com)
[![GUI](https://img.shields.io/badge/Interface-PyQt5-blue.svg)](https://pypi.org/project/PyQt5/)

## Features ✨

- **User-Friendly GUI**: Intuitive graphical interface built with PyQt5
- **Smart Music Matching**: Intelligent track matching with fuzzy search algorithms
- **Multiple Audio Formats**: Supports MP3, FLAC, M4A, MP4, WAV, OGG
- **Batch Processing**: Process entire music libraries efficiently
- **Real-time Progress**: Live progress bar and detailed logging
- **Metadata Extraction**: Automatically extracts title, artist, and album information
- **Fallback Strategies**: Multiple search strategies for better match rates
- **Detailed Reporting**: Comprehensive results with success rates and error logs
- **Rate Limiting**: Respects platform API limits to avoid throttling

## Supported Platforms 🎧

- **Spotify** ✅ (Full support with playlist creation)
- More platforms coming soon!

## Installation 🚀

### Prerequisites

- Python 3.7 or higher
- Spotify Developer Account (for Spotify integration)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/cipherex/local2stream.git
   cd local2stream
   ```

2. **Install dependencies**
   ```bash
   pip install spotipy mutagen PyQt5
   ```

3. **Set up Spotify credentials**
   
   **Step-by-step Spotify setup:**
   
   1. **Create Spotify App:**
      - Visit [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
      - Log in with your Spotify account
      - Click "Create App"
      - Fill in app details:
        - App Name: `Local2Stream` (or any name you prefer)
        - App Description: `Transfer local music to Spotify playlists`
        - Redirect URI: `http://localhost:8888/callback`
        - Check "Web API" and agree to terms
      - Click "Save"
   
   2. **Get Your Credentials:**
      - In your new app's dashboard, click "Settings"
      - Copy your **Client ID** (visible by default)
      - Click "View client secret" and copy your **Client Secret**
      - **Important:** Keep these credentials secure and never share them publicly
   
   3. **Verify Redirect URI:**
      - Ensure `http://localhost:8888/callback` is listed in your app's redirect URIs
      - This exact URI is required for authentication to work

## Usage 📖

### GUI Application

Run the graphical interface:

```bash
python local2stream_gui.py
```

### Command Line Version

For the command-line version:

```bash
python local2stream_cli.py
```

### Using the GUI

1. **Select Music Directory**: Click "Browse" to choose your music folder
2. **Enter Playlist Name**: Choose a name for your new Spotify playlist
3. **Enter Spotify Credentials**: 
   - Input your Spotify Client ID
   - Input your Spotify Client Secret (hidden for security)
4. **Start Transfer**: Click "Start Transfer" to begin the process
5. **Monitor Progress**: Watch the real-time progress bar and detailed logs

## GUI Features 🖥️

### Main Interface Elements

- **Music Directory Selection**: Browse and select your music folder
- **Playlist Configuration**: Set your desired playlist name
- **Spotify Authentication**: Secure credential input with password masking
- **Real-time Progress Bar**: Visual progress indicator
- **Live Logging**: Detailed process logs with colored status indicators
- **Status Bar**: Quick status updates and notifications

### Progress Indicators

- 📁 Directory scanning
- 🎵 File discovery
- 🔍 Track searching
- ✅ Successful matches
- ❌ Failed matches
- 🎉 Completion summary

## How It Works 🔍

### Metadata Extraction
- Extracts metadata from audio file tags (ID3, FLAC, MP4)
- Falls back to filename parsing if metadata is missing
- Supports common filename formats like "Artist - Title"

### Intelligent Matching
1. **Exact Match**: Direct title and artist matching
2. **Fuzzy Match**: Similarity-based matching with confidence scores
3. **Title-Only Search**: When artist information is unavailable
4. **Artist Fallback**: Search by artist, then match titles

### Match Types in GUI
- **[Exact]**: Perfect title and artist match
- **[Fuzzy]**: High similarity match with confidence scoring
- **[Title Only]**: Match based on title when artist is unavailable
- **[Artist Fallback]**: Found through artist search with title matching

## Supported Audio Formats 🎵

| Format | Extension | Metadata Support |
|--------|-----------|------------------|
| MP3    | `.mp3`    | ✅ ID3 tags      |
| FLAC   | `.flac`   | ✅ Vorbis tags   |
| M4A/MP4| `.m4a`, `.mp4` | ✅ iTunes tags |
| WAV    | `.wav`    | ⚠️ Filename only |
| OGG    | `.ogg`    | ⚠️ Filename only |

## Example GUI Output 📈

```
📁 Scanning directory: /Users/username/Music
🎵 Found 1,245 music files
✅ Created playlist: My Local Collection
🔍 Searching: The Beatles - Hey Jude
✅ [Exact] The Beatles - Hey Jude
🔍 Searching: Unknown Artist - Great Song
🔍 [Fuzzy] Various Artists - Great Song
❌ Not found: Obscure Artist - Rare Track

==== SUMMARY ====
Total files: 1,245
Exact matches: 987
Fuzzy matches: 156
Title only matches: 45
Artist fallback matches: 55
Not found: 102
Success rate: 91.8%
```

## Troubleshooting 🔧

### Common Issues

**GUI Won't Start**
- Ensure PyQt5 is installed: `pip install PyQt5`
- Check Python version compatibility (3.7+)

**Authentication Error**
- Verify your Spotify credentials are correct
- Ensure redirect URI is set to `http://localhost:8888/callback`
- Check that your Spotify app has the required scopes

**No Matches Found**
- Ensure your music files have proper metadata
- Check filename format (use "Artist - Title" format)
- Verify file formats are supported

**Transfer Stops or Freezes**
- Large collections may take time to process
- The GUI will remain responsive during processing
- Check the log area for detailed error messages

## File Structure 📁

```
local2stream/
├── local2stream_gui.py          # GUI application
├── local2stream_cli.py          # Command-line version
├── README.md                    # This file
├── LICENSE                      # MIT License
└── requirements.txt             # Python dependencies
```

## Contributing 🤝

Contributions are welcome! Please feel free to:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

### Development Setup

For GUI development:
```bash
pip install PyQt5 spotipy mutagen
```

## Roadmap 🗺️

- [ ] Apple Music support
- [ ] YouTube Music support
- [ ] Batch playlist management
- [ ] Enhanced GUI features (dark mode, themes)
- [ ] Docker support
- [ ] Duplicate detection
- [ ] Advanced matching algorithms
- [ ] Drag-and-drop functionality
- [ ] Multi-language support

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer ⚠️

This tool is for personal use only. Please respect the terms of service of streaming platforms and ensure you have the right to upload/transfer your music collection.

## Support 💬

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/cipherex/local2stream/issues) page
2. Create a new issue with detailed information
3. Include error logs and configuration details
4. For GUI-specific issues, include your operating system and Python version

## Acknowledgments 🙏

- [Spotipy](https://spotipy.readthedocs.io/) for Spotify API integration
- [Mutagen](https://mutagen.readthedocs.io/) for audio metadata handling
- [PyQt5](https://pypi.org/project/PyQt5/) for the graphical interface
- The open-source community for inspiration and support

---

**Made with ❤️ by [Aryan](https://github.com/cipherex)**

*Local2Stream v2.0.0 - Bringing your local music to the streaming world with style*