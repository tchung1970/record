# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Status

This repository is currently in an initial state with minimal setup. The project appears to be named "record" based on the directory structure.

## Configuration

- Claude Code permissions are configured in `.claude/settings.local.json` with specific tool allowances including system utilities, package management, and media processing tools
- The allowed tools suggest potential use cases involving system administration, media processing (ffmpeg, ffprobe), and package management

## Development Setup

This repository does not currently contain standard development configuration files (package.json, requirements.txt, Cargo.toml, etc.). When adding development dependencies:

- Choose appropriate package management based on the technology stack
- Add build, test, and lint commands to the package configuration
- Update this file with relevant development commands once established

## Next Steps

Future instances of Claude Code should:
1. Determine the intended technology stack and purpose of the "record" project
2. Initialize appropriate project structure and dependencies
3. Update this CLAUDE.md with specific build, test, and development commands
4. Document the architecture and key components as they are developed