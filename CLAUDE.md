# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Status

This repository contains a Python-based screen recording tool for macOS applications.

## Project Overview

**record** is a macOS screen recording utility that:
- Records specific application windows or entire screen using ffmpeg
- Detects and lists currently running desktop applications
- Provides DRM protection warnings for streaming apps
- Features responsive ESC key detection to stop recording early
- Outputs recordings in .mov format for QuickTime compatibility
- Maintains Terminal focus during recording for reliable ESC key handling

## Configuration

- Claude Code permissions are configured in `.claude/settings.local.json` with specific tool allowances including system utilities, package management, and media processing tools
- The allowed tools are essential for the media processing functionality (ffmpeg, ffprobe) and system interactions required by the recording script

## Dependencies

- **Python 3**: Core language
- **ffmpeg**: Video recording engine (auto-installed via Homebrew if missing)
- **Homebrew**: Package manager for installing ffmpeg
- **macOS System Permissions**: Screen Recording permission required

## Usage

Run the script directly:
```bash
python3 record.py
```

The script will:
1. Check and install dependencies (ffmpeg via Homebrew)
2. List running applications
3. Allow selection of specific app or entire screen
4. Record for 60 seconds (or until ESC is pressed)
5. Save recording as timestamped .mov file

## Development Notes

- ESC key detection uses raw terminal mode with frequent polling (every 100ms)
- Window coordinate detection via AppleScript for precise app recording
- Terminal focus is maintained during recording for reliable user control