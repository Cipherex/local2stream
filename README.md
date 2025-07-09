# Local2Stream 🎵

Transfer your local music collection to streaming platforms with intelligent matching and fuzzy search capabilities.

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Spotify](https://img.shields.io/badge/Platform-Spotify-1DB954.svg)](https://spotify.com)

## Features ✨

- **Smart Music Matching**: Intelligent track matching with fuzzy search algorithms
- **Multiple Audio Formats**: Supports MP3, FLAC, M4A, MP4, WAV, OGG
- **Batch Processing**: Process entire music libraries efficiently
- **Metadata Extraction**: Automatically extracts title, artist, and album information
- **Fallback Strategies**: Multiple search strategies for better match rates
- **Configuration Management**: Save and reuse settings for future runs
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
   pip install spotipy mutagen
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

### Interactive Mode

Run the script and follow the prompts:

```bash
python local2stream_cli.py
```

### Command Line Options

```bash
python local2stream_cli.py --help        # Show help
python local2stream_cli.py --version     # Show version
python local2stream_cli.py --config      # Use saved configuration
```

### First Run Setup

1. **Music Directory**: Enter the path to your music collection
2. **Playlist Name**: Choose a name for your new playlist
3. **Spotify Credentials**: Enter your Client ID and Client Secret
4. **Configuration**: Option to save settings for future use

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

## Configuration 🛠️

The tool creates a `local2stream_config.json` file to store your preferences:

```json
{
  "music_directory": "/path/to/your/music",
  "playlist_name": "Local2Stream Collection",
  "platforms": ["spotify"],
  "spotify": {
    "client_id": "your_client_id",
    "client_secret": "your_client_secret",
    "redirect_uri": "http://localhost:8888/callback"
  }
}
```

## Output Files 📊

After processing, the tool generates several files:

- `added_tracks_YYYYMMDD_HHMMSS.json`: Successfully added tracks
- `not_found_tracks_YYYYMMDD_HHMMSS.json`: Tracks that couldn't be matched
- `local2stream_results_YYYYMMDD_HHMMSS.json`: Detailed results and statistics

## Example Output 📈

```
🎵 LOCAL2STREAM TRANSFER SUMMARY
============================================
Total files found: 1,245
Successfully processed: 1,245
Exact matches found: 987
Fuzzy matches found: 156
Not found: 102
Errors: 0
Success rate: 91.8%

Platforms used: Spotify
```

## Supported Audio Formats 🎵

| Format | Extension | Metadata Support |
|--------|-----------|------------------|
| MP3    | `.mp3`    | ✅ ID3 tags      |
| FLAC   | `.flac`   | ✅ Vorbis tags   |
| M4A/MP4| `.m4a`, `.mp4` | ✅ iTunes tags |
| WAV    | `.wav`    | ⚠️ Filename only |
| OGG    | `.ogg`    | ⚠️ Filename only |

## Troubleshooting 🔧

### Common Issues

**Authentication Error**
- Verify your Spotify credentials are correct
- Ensure redirect URI is set to `http://localhost:8888/callback`
- Check that your Spotify app has the required scopes

**No Matches Found**
- Ensure your music files have proper metadata
- Check filename format (use "Artist - Title" format)
- Verify file formats are supported

**Rate Limiting**
- The tool automatically handles rate limiting
- For large collections, processing may take time

## Contributing 🤝

Contributions are welcome! Please feel free to:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Roadmap 🗺️

- [ ] Apple Music support
- [ ] YouTube Music support
- [ ] Batch playlist management
- [ ] GUI interface
- [ ] Docker support
- [ ] Duplicate detection
- [ ] Advanced matching algorithms

## Roadmap 🗺️

- [ ] Apple Music support
- [ ] YouTube Music support
- [ ] Batch playlist management
- [ ] GUI interface
- [ ] Docker support
- [ ] Duplicate detection
- [ ] Advanced matching algorithms

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer ⚠️

This tool is for personal use only. Please respect the terms of service of streaming platforms and ensure you have the right to upload/transfer your music collection.

## Support 💬

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/cipherex/local2stream/issues) page
2. Create a new issue with detailed information
3. Include error logs and configuration details

## Acknowledgments 🙏

- [Spotipy](https://spotipy.readthedocs.io/) for Spotify API integration
- [Mutagen](https://mutagen.readthedocs.io/) for audio metadata handling
- The open-source community for inspiration and support

---

**Made with ❤️ by [Aryan](https://github.com/cipherex)**

*Local2Stream v2.0.0 - Bringing your local music to the streaming world*