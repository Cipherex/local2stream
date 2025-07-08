"""
Local2Stream - Transfer your local music collection to streaming platforms
Supports: Spotify
Made by Aryan
"""

import os
import json
import sys
import time
import difflib
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
from datetime import datetime
import argparse

# Third-party imports
try:
    import spotipy
    from spotipy.oauth2 import SpotifyOAuth
    from mutagen.mp3 import MP3
    from mutagen.flac import FLAC
    from mutagen.mp4 import MP4
    from mutagen.id3 import ID3NoHeaderError
except ImportError as e:
    print(f"❌ Missing required package: {e}")
    print("Please install required packages:")
    print("pip install spotipy mutagen")
    sys.exit(1)

@dataclass
class TrackMetadata:
    """Data class for track metadata"""
    title: str
    artist: str
    album: str
    file_path: str
    duration: Optional[int] = None

@dataclass
class MatchResult:
    """Data class for match results"""
    track_id: str
    track_name: str
    artist_name: str
    match_type: str  # 'exact' or 'fuzzy'
    confidence: float
    platform: str

class ConfigManager:
    """Manages configuration and user input"""
    
    def __init__(self):
        self.config_file = "local2stream_config.json"
        self.config = self.load_config()
    
    def load_config(self) -> Dict:
        """Load configuration from file"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_config(self, config: Dict):
        """Save configuration to file"""
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
    
    def get_user_input(self) -> Dict:
        """Get configuration from user input"""
        print("🎵 Welcome to Local2Stream!")
        print("=" * 50)
        
        # Music directory
        default_music_dir = self.config.get('music_directory', str(Path.home() / 'Music'))
        music_dir = input(f"Enter your music directory [{default_music_dir}]: ").strip()
        if not music_dir:
            music_dir = default_music_dir
        
        if not os.path.exists(music_dir):
            print(f"❌ Directory not found: {music_dir}")
            sys.exit(1)
        
        # Platform selection (only Spotify now)
        print("\nSelect streaming platform:")
        print("1. Spotify")
        platform_choice = input("Enter choice (1): ").strip()
        platforms = []
        if platform_choice in ['', '1']:
            platforms.append('spotify')
        else:
            print("❌ Invalid choice. Exiting.")
            sys.exit(1)
        
        # Playlist name
        default_playlist = self.config.get('playlist_name', 'Local2Stream Collection')
        playlist_name = input(f"Enter playlist name [{default_playlist}]: ").strip()
        if not playlist_name:
            playlist_name = default_playlist
        
        # Platform-specific credentials
        spotify_config = {}
        if 'spotify' in platforms:
            spotify_config = self.get_spotify_config()
        
        config = {
            'music_directory': music_dir,
            'playlist_name': playlist_name,
            'platforms': platforms,
            'spotify': spotify_config
        }
        
        # Ask to save config
        save_config = input("\nSave this configuration for future use? (y/n): ").strip().lower()
        if save_config == 'y':
            self.save_config(config)
            print("✅ Configuration saved!")
        
        return config
    
    def get_spotify_config(self) -> Dict:
        """Get Spotify configuration"""
        print("\n🎧 Spotify Configuration")
        print("To get Spotify credentials:")
        print("1. Go to https://developer.spotify.com/dashboard")
        print("2. Create a new app")
        print("3. Copy Client ID and Client Secret")
        print("4. Add redirect URI: http://localhost:8888/callback")
        
        client_id = self.config.get('spotify', {}).get('client_id', '')
        client_secret = self.config.get('spotify', {}).get('client_secret', '')
        
        if not client_id:
            client_id = input("Enter Spotify Client ID: ").strip()
        else:
            new_id = input(f"Enter Spotify Client ID [{client_id[:10]}...]: ").strip()
            if new_id:
                client_id = new_id
        
        if not client_secret:
            client_secret = input("Enter Spotify Client Secret: ").strip()
        else:
            new_secret = input(f"Enter Spotify Client Secret [{client_secret[:10]}...]: ").strip()
            if new_secret:
                client_secret = new_secret
        
        return {
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': 'http://localhost:8888/callback'
        }

class AudioMetadataExtractor:
    """Extracts metadata from audio files"""
    
    SUPPORTED_FORMATS = ['.mp3', '.flac', '.m4a', '.mp4', '.wav', '.ogg']
    
    @staticmethod
    def extract_metadata(file_path: str) -> Optional[TrackMetadata]:
        """Extract metadata from audio file"""
        try:
            file_ext = Path(file_path).suffix.lower()
            
            if file_ext == '.mp3':
                return AudioMetadataExtractor._extract_mp3_metadata(file_path)
            elif file_ext == '.flac':
                return AudioMetadataExtractor._extract_flac_metadata(file_path)
            elif file_ext in ['.m4a', '.mp4']:
                return AudioMetadataExtractor._extract_mp4_metadata(file_path)
            else:
                return AudioMetadataExtractor._extract_from_filename(file_path)
                
        except Exception as e:
            print(f"❌ Error extracting metadata from {file_path}: {e}")
            return None
    
    @staticmethod
    def _extract_mp3_metadata(file_path: str) -> Optional[TrackMetadata]:
        """Extract metadata from MP3 file"""
        try:
            audio = MP3(file_path)
            title = str(audio.get('TIT2', [''])[0])
            artist = str(audio.get('TPE1', [''])[0])
            album = str(audio.get('TALB', [''])[0])
            duration = int(audio.info.length) if audio.info else None
            
            return TrackMetadata(
                title=title or AudioMetadataExtractor._get_title_from_filename(file_path),
                artist=artist or AudioMetadataExtractor._get_artist_from_filename(file_path),
                album=album,
                file_path=file_path,
                duration=duration
            )
        except (ID3NoHeaderError, Exception):
            return AudioMetadataExtractor._extract_from_filename(file_path)
    
    @staticmethod
    def _extract_flac_metadata(file_path: str) -> Optional[TrackMetadata]:
        """Extract metadata from FLAC file"""
        try:
            audio = FLAC(file_path)
            title = audio.get('TITLE', [''])[0]
            artist = audio.get('ARTIST', [''])[0]
            album = audio.get('ALBUM', [''])[0]
            duration = int(audio.info.length) if audio.info else None
            
            return TrackMetadata(
                title=title or AudioMetadataExtractor._get_title_from_filename(file_path),
                artist=artist or AudioMetadataExtractor._get_artist_from_filename(file_path),
                album=album,
                file_path=file_path,
                duration=duration
            )
        except Exception:
            return AudioMetadataExtractor._extract_from_filename(file_path)
    
    @staticmethod
    def _extract_mp4_metadata(file_path: str) -> Optional[TrackMetadata]:
        """Extract metadata from MP4/M4A file"""
        try:
            audio = MP4(file_path)
            title = audio.get('\xa9nam', [''])[0]
            artist = audio.get('\xa9ART', [''])[0]
            album = audio.get('\xa9alb', [''])[0]
            duration = int(audio.info.length) if audio.info else None
            
            return TrackMetadata(
                title=title or AudioMetadataExtractor._get_title_from_filename(file_path),
                artist=artist or AudioMetadataExtractor._get_artist_from_filename(file_path),
                album=album,
                file_path=file_path,
                duration=duration
            )
        except Exception:
            return AudioMetadataExtractor._extract_from_filename(file_path)
    
    @staticmethod
    def _extract_from_filename(file_path: str) -> TrackMetadata:
        """Extract metadata from filename"""
        filename = Path(file_path).stem
        
        # Try to parse "Artist - Title" format
        if ' - ' in filename:
            parts = filename.split(' - ', 1)
            artist = parts[0].strip()
            title = parts[1].strip()
        else:
            artist = ""
            title = filename
        
        return TrackMetadata(
            title=title,
            artist=artist,
            album="",
            file_path=file_path
        )
    
    @staticmethod
    def _get_title_from_filename(file_path: str) -> str:
        """Get title from filename"""
        return Path(file_path).stem.split(' - ')[-1].strip()
    
    @staticmethod
    def _get_artist_from_filename(file_path: str) -> str:
        """Get artist from filename"""
        filename = Path(file_path).stem
        if ' - ' in filename:
            return filename.split(' - ')[0].strip()
        return ""

class StreamingPlatformBase:
    """Base class for streaming platforms"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.platform_name = "Unknown"
    
    def authenticate(self) -> bool:
        """Authenticate with the platform"""
        raise NotImplementedError
    
    def search_track(self, metadata: TrackMetadata) -> Optional[MatchResult]:
        """Search for a track on the platform"""
        raise NotImplementedError
    
    def create_playlist(self, name: str, description: str = "") -> Optional[str]:
        """Create a new playlist"""
        raise NotImplementedError
    
    def add_tracks_to_playlist(self, playlist_id: str, track_ids: List[str]) -> bool:
        """Add tracks to playlist"""
        raise NotImplementedError
    
    @staticmethod
    def clean_string(text: str) -> str:
        """Clean and normalize text for better matching"""
        if not text:
            return ""
        
        # Remove common patterns that might differ
        text = re.sub(r'\([^)]*\)', '', text)  # Remove parentheses content
        text = re.sub(r'\[[^\]]*\]', '', text)  # Remove bracket content
        text = re.sub(r'\s*-\s*', ' ', text)    # Replace dashes with spaces
        text = re.sub(r'[^\w\s]', '', text)     # Remove special characters
        text = re.sub(r'\s+', ' ', text)        # Multiple spaces to single
        
        return text.strip().lower()

class SpotifyHandler(StreamingPlatformBase):
    """Handle Spotify operations"""
    
    def __init__(self, config: Dict):
        super().__init__(config)
        self.platform_name = "Spotify"
        self.sp = None
    
    def authenticate(self) -> bool:
        """Authenticate with Spotify"""
        try:
            scope = "playlist-modify-public playlist-modify-private"
            self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
                client_id=self.config['client_id'],
                client_secret=self.config['client_secret'],
                redirect_uri=self.config['redirect_uri'],
                scope=scope
            ))
            
            # Test authentication
            user = self.sp.me()
            print(f"✅ Authenticated with Spotify as: {user['display_name']}")
            return True
            
        except Exception as e:
            print(f"❌ Spotify authentication failed: {e}")
            return False
    
    def _fuzzy_match(self, a: str, b: str) -> float:
        """Improved fuzzy matching for song/artist names"""
        a_clean = self.clean_string(a)
        b_clean = self.clean_string(b)
        # Try direct ratio
        ratio = difflib.SequenceMatcher(None, a_clean, b_clean).ratio()
        # Try partial ratio (substring)
        if a_clean in b_clean or b_clean in a_clean:
            ratio = max(ratio, 0.85)
        # Try ignoring extra characters (remove all non-alphanum)
        a_alnum = re.sub(r'[^a-zA-Z0-9]', '', a_clean)
        b_alnum = re.sub(r'[^a-zA-Z0-9]', '', b_clean)
        ratio = max(ratio, difflib.SequenceMatcher(None, a_alnum, b_alnum).ratio())
        return ratio

    def search_track(self, metadata: TrackMetadata) -> Optional[MatchResult]:
        """Search for track on Spotify with improved fuzzy matching"""
        if not self.sp:
            return None
        try:
            title = metadata.title
            artist = metadata.artist
            if not title:
                return None
            # Try exact search first
            if artist:
                query = f'track:"{title}" artist:"{artist}"'
            else:
                query = f'track:"{title}"'
            results = self.sp.search(q=query, type='track', limit=20)
            if results['tracks']['items']:
                # Check for exact match
                for track in results['tracks']['items']:
                    track_title = self.clean_string(track['name'])
                    track_artist = self.clean_string(track['artists'][0]['name'])
                    search_title = self.clean_string(title)
                    search_artist = self.clean_string(artist)
                    if (track_title == search_title and 
                        (not search_artist or track_artist == search_artist)):
                        return MatchResult(
                            track_id=track['id'],
                            track_name=track['name'],
                            artist_name=track['artists'][0]['name'],
                            match_type='exact',
                            confidence=1.0,
                            platform='spotify'
                        )
                # Try improved fuzzy matching
                best_match = None
                best_score = 0
                for track in results['tracks']['items']:
                    track_title = track['name']
                    track_artist = track['artists'][0]['name']
                    search_title = title
                    search_artist = artist
                    title_score = self._fuzzy_match(track_title, search_title)
                    artist_score = 1.0
                    if search_artist:
                        artist_score = self._fuzzy_match(track_artist, search_artist)
                    combined_score = (title_score * 0.7) + (artist_score * 0.3)
                    if combined_score > best_score and combined_score > 0.55:
                        best_score = combined_score
                        best_match = track
                if best_match:
                    return MatchResult(
                        track_id=best_match['id'],
                        track_name=best_match['name'],
                        artist_name=best_match['artists'][0]['name'],
                        match_type='fuzzy',
                        confidence=best_score,
                        platform='spotify'
                    )
            return None
        except Exception as e:
            print(f"❌ Error searching Spotify: {e}")
            return None
    
    def create_playlist(self, name: str, description: str = "") -> Optional[str]:
        """Create Spotify playlist"""
        try:
            user_id = self.sp.me()['id']
            playlist = self.sp.user_playlist_create(
                user=user_id,
                name=name,
                public=False,
                description=description
            )
            return playlist['id']
        except Exception as e:
            print(f"❌ Error creating Spotify playlist: {e}")
            return None
    
    def add_tracks_to_playlist(self, playlist_id: str, track_ids: List[str]) -> bool:
        """Add tracks to Spotify playlist"""
        try:
            # Convert track IDs to URIs
            track_uris = [f"spotify:track:{track_id}" for track_id in track_ids]
            
            # Add in batches of 100
            batch_size = 100
            for i in range(0, len(track_uris), batch_size):
                batch = track_uris[i:i + batch_size]
                self.sp.playlist_add_items(playlist_id, batch)
                time.sleep(0.1)  # Rate limiting
            
            return True
        except Exception as e:
            print(f"❌ Error adding tracks to Spotify playlist: {e}")
            return False

class Local2Stream:
    """Main application class"""
    
    def __init__(self):
        self.config_manager = ConfigManager()
        self.platforms = {}
        self.stats = {
            'total_files': 0,
            'processed': 0,
            'found_exact': 0,
            'found_fuzzy': 0,
            'not_found': 0,
            'errors': 0
        }
        self.results = {
            'added_tracks': [],
            'not_found_tracks': [],
            'errors': []
        }
    
    def initialize_platforms(self, config: Dict):
        """Initialize streaming platforms"""
        if 'spotify' in config['platforms']:
            spotify_handler = SpotifyHandler(config['spotify'])
            if spotify_handler.authenticate():
                self.platforms['spotify'] = spotify_handler
        if not self.platforms:
            print("❌ No platforms authenticated successfully!")
            return False
        return True
    
    def scan_music_directory(self, directory: str) -> List[str]:
        """Scan directory for music files"""
        music_files = []
        
        print(f"📁 Scanning directory: {directory}")
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                if any(file.lower().endswith(ext) for ext in AudioMetadataExtractor.SUPPORTED_FORMATS):
                    music_files.append(os.path.join(root, file))
        
        print(f"🎵 Found {len(music_files)} music files")
        return music_files
    
    def process_music_files(self, music_files: List[str], config: Dict):
        """Process music files and transfer to streaming platforms"""
        self.stats['total_files'] = len(music_files)
        # Create playlists on each platform
        playlist_ids = {}
        description = f"Auto-generated by Local2Stream - {len(music_files)} files processed on {datetime.now().strftime('%Y-%m-%d %H:%M')} | Made by Aryan"
        for platform_name, platform_handler in self.platforms.items():
            playlist_id = platform_handler.create_playlist(
                config['playlist_name'],
                description
            )
            if playlist_id:
                playlist_ids[platform_name] = playlist_id
                print(f"✅ Created playlist on {platform_handler.platform_name}: {config['playlist_name']}")
            else:
                print(f"❌ Failed to create playlist on {platform_handler.platform_name}")
        # Process each file
        platform_tracks = {platform: [] for platform in self.platforms.keys()}
        for i, file_path in enumerate(music_files):
            print(f"\n🎵 Processing {i+1}/{len(music_files)}: {Path(file_path).name}")
            # Extract metadata
            metadata = AudioMetadataExtractor.extract_metadata(file_path)
            if not metadata:
                print("  ❌ Could not extract metadata")
                self.stats['errors'] += 1
                self.results['errors'].append({
                    'file_path': file_path,
                    'error': 'Could not extract metadata'
                })
                continue
            print(f"  📀 {metadata.artist} - {metadata.title}")
            # Search on each platform
            found_on_platforms = []
            for platform_name, platform_handler in self.platforms.items():
                match_result = platform_handler.search_track(metadata)
                if match_result:
                    platform_tracks[platform_name].append(match_result.track_id)
                    found_on_platforms.append(platform_name)
                    icon = "✅" if match_result.match_type == 'exact' else "🔍"
                    print(f"  {icon} {platform_handler.platform_name}: {match_result.artist_name} - {match_result.track_name}")
                    if match_result.match_type == 'exact':
                        self.stats['found_exact'] += 1
                    else:
                        self.stats['found_fuzzy'] += 1
                else:
                    print(f"  ❌ {platform_handler.platform_name}: No match found")
            if found_on_platforms:
                self.results['added_tracks'].append({
                    'local_file': file_path,
                    'title': metadata.title,
                    'artist': metadata.artist,
                    'platforms': found_on_platforms
                })
            else:
                self.stats['not_found'] += 1
                self.results['not_found_tracks'].append({
                    'file_path': file_path,
                    'title': metadata.title,
                    'artist': metadata.artist
                })
            self.stats['processed'] += 1
            # Add tracks to playlists in batches
            if i % 25 == 0 and i > 0:
                self.add_tracks_to_playlists(playlist_ids, platform_tracks)
                platform_tracks = {platform: [] for platform in self.platforms.keys()}
        # Add remaining tracks
        if any(tracks for tracks in platform_tracks.values()):
            self.add_tracks_to_playlists(playlist_ids, platform_tracks)
    
    def add_tracks_to_playlists(self, playlist_ids: Dict[str, str], platform_tracks: Dict[str, List[str]]):
        """Add tracks to playlists"""
        for platform_name, track_ids in platform_tracks.items():
            if track_ids and platform_name in playlist_ids:
                platform_handler = self.platforms[platform_name]
                success = platform_handler.add_tracks_to_playlist(playlist_ids[platform_name], track_ids)
                if success:
                    print(f"  ✅ Added {len(track_ids)} tracks to {platform_handler.platform_name}")
                else:
                    print(f"  ❌ Failed to add tracks to {platform_handler.platform_name}")
    
    def print_summary(self):
        """Print transfer summary"""
        print("\n" + "="*60)
        print("🎵 LOCAL2STREAM TRANSFER SUMMARY (Made by Aryan)")
        print("="*60)
        print(f"Total files found: {self.stats['total_files']}")
        print(f"Successfully processed: {self.stats['processed']}")
        print(f"Exact matches found: {self.stats['found_exact']}")
        print(f"Fuzzy matches found: {self.stats['found_fuzzy']}")
        print(f"Not found: {self.stats['not_found']}")
        print(f"Errors: {self.stats['errors']}")
        if self.stats['total_files'] > 0:
            success_rate = ((self.stats['found_exact'] + self.stats['found_fuzzy']) / self.stats['total_files']) * 100
            print(f"Success rate: {success_rate:.1f}%")
        print(f"\nPlatforms used: {', '.join(handler.platform_name for handler in self.platforms.values())}")
        print("Made by Aryan")
    
    def save_results(self):
        """Save results to JSON files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Save added tracks
        if self.results['added_tracks']:
            added_file = f"added_tracks_{timestamp}.json"
            with open(added_file, 'w', encoding='utf-8') as f:
                json.dump(self.results['added_tracks'], f, indent=2, ensure_ascii=False)
            print(f"📋 Added tracks: {added_file}")
        # Save not found tracks
        if self.results['not_found_tracks']:
            not_found_file = f"not_found_tracks_{timestamp}.json"
            with open(not_found_file, 'w', encoding='utf-8') as f:
                json.dump(self.results['not_found_tracks'], f, indent=2, ensure_ascii=False)
            print(f"📋 Not found tracks: {not_found_file}")
        # Save detailed results
        results_file = f"local2stream_results_{timestamp}.json"
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump({
                'stats': self.stats,
                'results': self.results,
                'timestamp': timestamp,
                'platforms': list(self.platforms.keys()),
                'made_by': 'Aryan'
            }, f, indent=2, ensure_ascii=False)
        print(f"\n📊 Results saved to: {results_file}")
    
    def run(self):
        """Main run method"""
        try:
            # Get configuration
            config = self.config_manager.get_user_input()
            
            # Initialize platforms
            if not self.initialize_platforms(config):
                return
            
            # Scan music directory
            music_files = self.scan_music_directory(config['music_directory'])
            
            if not music_files:
                print("❌ No music files found in the specified directory!")
                return
            
            # Confirm before processing
            print(f"\n🚀 Ready to process {len(music_files)} files")
            print(f"Platforms: {', '.join(handler.platform_name for handler in self.platforms.values())}")
            print(f"Playlist: {config['playlist_name']}")
            
            confirm = input("\nProceed with transfer? (y/n): ").strip().lower()
            if confirm != 'y':
                print("Transfer cancelled.")
                return
            
            # Process files
            print("\n🎵 Starting music transfer...")
            self.process_music_files(music_files, config)
            
            # Show summary and save results
            self.print_summary()
            self.save_results()
            
            print("\n🎉 Transfer complete!")
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Transfer interrupted by user")
            if self.results['added_tracks']:
                print("Saving partial results...")
                self.save_results()
        except Exception as e:
            print(f"\n❌ An error occurred: {e}")
            if self.results['added_tracks']:
                print("Saving partial results...")
                self.save_results()

def main():
    """Main function with command line argument support"""
    parser = argparse.ArgumentParser(
        description='Local2Stream - Transfer your local music collection to streaming platforms',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python local2stream.py                    # Interactive mode
  python local2stream.py --help            # Show this help
  
Supported platforms:
  - Spotify (requires app credentials)
  
Supported audio formats:
  - MP3, FLAC, M4A, MP4, WAV, OGG
        """
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='Local2Stream 2.0.0'
    )
    
    parser.add_argument(
        '--config',
        help='Use saved configuration file',
        action='store_true'
    )
    
    args = parser.parse_args()
    
    print("🎵 Local2Stream v2.0.0")
    print("Transfer your local music collection to streaming platforms")
    print("Supports: Spotify")
    print("-" * 60)
    
    # Check for required packages
    required_packages = ['spotipy', 'mutagen']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"  - {package}")
        print("\nInstall missing packages with:")
        print(f"pip install {' '.join(missing_packages)}")
        return
    
    # Initialize and run
    app = Local2Stream()
    app.run()

if __name__ == "__main__":
    main()