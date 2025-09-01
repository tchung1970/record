# CLAUDE.md - Developer Documentation

This file provides technical guidance for Claude Code when working with the screen recording tool codebase.

## Architecture Overview

The screen recording tool is a single-file Python script (`record.py`) with the following key components:

### Core Functions

- `check_for_escape()`: Non-blocking ESC key detection with input buffer management
- `get_running_apps()`: AppleScript-based application discovery and filtering
- `get_app_window_info()`: Window coordinate extraction for targeted recording
- `record_screen()`: Main recording logic with ffmpeg subprocess management
- `check_dependencies()`: Automatic dependency installation via Homebrew

### Key Technical Decisions

1. **Raw Terminal Mode**: Uses `termios` and `tty` for direct keyboard input handling
2. **AppleScript Integration**: Leverages macOS scripting for window management and app control
3. **ffmpeg Subprocess**: Background process management with proper cleanup
4. **Focus Management**: Maintains Terminal focus during recording for reliable ESC detection

## Development Guidelines

### ESC Key Detection
The `check_for_escape()` function has been optimized for reliability:
- Polls input 10 times over 100ms to catch keypresses
- Clears input buffer to handle multi-byte escape sequences  
- Recording loop checks ESC every 100ms instead of 1 second

### Window Management
Focus handling sequence:
1. Briefly activate target app (0.5s) to get window coordinates
2. Return focus to Terminal for ESC key detection
3. Record target app window using stored coordinates

### Error Handling
- Graceful fallback when window info unavailable (records full screen)
- Safe subprocess termination on ESC or completion
- Terminal settings restoration in finally block

## Configuration

### Claude Code Permissions
Required tools in `.claude/settings.local.json`:
- `system_profiler`, `brew`, `python3`: System utilities
- `ffmpeg`, `ffprobe`: Media processing
- `osascript`: AppleScript execution
- `open`, `chmod`: File operations

### Dependencies
- **Python 3.6+**: Core runtime
- **ffmpeg**: Video encoding (auto-installed)
- **Homebrew**: Package manager
- **macOS Screen Recording Permission**: System permission required

## Code Quality Standards

- Single-file architecture for simplicity
- Comprehensive error handling with user-friendly messages
- AppleScript integration for native macOS functionality
- Proper resource cleanup (terminal settings, subprocess termination)
- DRM app detection for user guidance

## Testing Considerations

When modifying the code:
1. Test ESC key responsiveness across different terminal emulators
2. Verify window coordinate detection for various app types
3. Confirm Terminal focus is maintained during recording
4. Test dependency auto-installation on clean systems
5. Validate output file format compatibility with QuickTime