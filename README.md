# Screen Recording Tool for macOS

A simple Python script for recording specific macOS applications using ffmpeg. This tool provides intelligent app detection, DRM protection warnings, and flexible recording controls.

## Features

- 🎯 **Smart App Detection** - Automatically detects running desktop applications with visible windows
- 🔒 **DRM Protection Warnings** - Identifies and warns about apps that may show black screen due to copyright protection (Netflix, Apple TV, etc.)
- ⏱️ **Flexible Duration** - Default 60-second recording with live countdown timer
- ⚡ **Responsive ESC Detection** - Press ESC during recording to stop early (Terminal stays focused)
- 🎨 **Clean Interface** - Intuitive command-line interface with clear prompts
- 📱 **Window-Specific Recording** - Records only the selected app window, not the entire screen
- 🚀 **Auto-Installation** - Automatically installs missing dependencies (ffmpeg) via Homebrew

## Requirements

- macOS (tested on macOS Sonoma and later)
- Python 3.6+
- Homebrew (for automatic dependency installation)
- Screen Recording permission enabled in System Preferences

## Installation

1. Clone the repository:
```bash
git clone https://github.com/tchung1970/record.git
cd record
```

2. Run the script (dependencies will be installed automatically):
```bash
python record.py
```

## Usage

### Basic Usage

Simply run the script and follow the interactive prompts:

```bash
python record.py
```

### Example Session

```
Screen Recording Tool for macOS
================================
✓ ffmpeg found

Currently running applications:
1. Speedtest
2. TV (DRM Protected)
3. Safari
4. Calculator

⚠️  Warning: DRM Protected apps will show black screen during recording
   due to copyright protection. Choose non-DRM apps for successful recording.

Found 4 running application(s).

Enter number (1-4) to select app, press Enter for default (1), or type 'exit' to quit: 

💡 Tip: Press ESC during recording to stop early

Record Speedtest for 60 seconds? (Y/n): 
Recording Speedtest window at 1280x720
Terminal kept in focus for ESC key detection
Starting screen recording for 60 seconds...
3...
2...
1...
Recording!
Recording... 60s remaining (Press ESC to stop)
Recording... 59s remaining (Press ESC to stop)
...
Recording completed! Saved as: screen_recording_20250901_115859.mov
```

## Configuration

The script automatically handles:
- **Dependency checking** - Verifies ffmpeg installation
- **Permission setup** - Guides you through macOS Screen Recording permissions
- **App filtering** - Excludes system processes and background apps
- **Window detection** - Gets precise coordinates for app-specific recording

## DRM-Protected Applications

The following apps are detected as DRM-protected and may show black screen during recording:

- Apple TV
- Apple Music
- Netflix
- Disney+
- Amazon Prime Video
- HBO Max
- Hulu
- Spotify (Premium content)
- And other streaming services

Choose non-DRM apps like Safari, Calculator, or development tools for successful recordings.

## Troubleshooting

### Screen Recording Permission
If you get a black screen:
1. Go to **System Preferences > Security & Privacy > Privacy > Screen Recording**
2. Add Terminal (or your terminal app) to the list
3. Restart Terminal and try again

### Missing Dependencies
The script will automatically prompt to install missing dependencies:
- ffmpeg (via Homebrew)
- Homebrew itself (if not installed)

### Recording Quality
The default settings provide:
- **Resolution**: Native app window size
- **Frame Rate**: 30 FPS
- **Format**: MOV (H.264)
- **Quality**: Optimized for file size and compatibility

## Output Files

Recordings are saved in the current directory with timestamps:
- Format: `screen_recording_YYYYMMDD_HHMMSS.mov`
- Example: `screen_recording_20250901_115859.mov`

## Technical Details

- **Recording Engine**: ffmpeg with avfoundation framework
- **Window Detection**: AppleScript integration for precise app window coordinates
- **Input Handling**: Raw terminal mode for ESC key detection
- **Process Management**: Safe subprocess handling with proper cleanup

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## Acknowledgments

- Built with [Claude Code](https://claude.ai/code)
- Uses ffmpeg for robust video recording
- Leverages macOS AppleScript for window management

## Author

Thomas Chung  
Created: September 1, 2025

## License

This project is open source and available under the MIT [LICENSE](LICENSE).