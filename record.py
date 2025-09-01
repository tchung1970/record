#!/usr/bin/env python3
"""
record.py
by Thomas Chung
on 2025-09-01

This script records screen activity of specific macOS applications using ffmpeg.
It detects running desktop applications, allows user selection, and provides
features like DRM protection warnings, countdown timers, and ESC key to stop recording.

Screen recording script for macOS that records currently opened apps (excluding Terminal).
Records for 60 seconds by default with option to stop early using ESC key.
"""

import subprocess
import os
import sys
import time
import select
import termios
import tty
from datetime import datetime


def check_for_escape():
    """Check if ESC key is pressed (non-blocking)."""
    # Check multiple times with small delays to catch keypresses more reliably
    for _ in range(10):  # Check 10 times over 100ms
        if select.select([sys.stdin], [], [], 0.01) == ([sys.stdin], [], []):
            try:
                ch = sys.stdin.read(1)
                if ch == '\x1b':  # ESC key
                    # Clear any remaining input buffer
                    while select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
                        sys.stdin.read(1)
                    return True
            except:
                pass
    return False


def is_drm_protected_app(app_name):
    """Check if an app is known to have DRM protection."""
    drm_apps = [
        'TV',           # Apple TV
        'Music',        # Apple Music  
        'Netflix',
        'Disney+',
        'Amazon Prime Video',
        'HBO Max',
        'Hulu',
        'Spotify',      # Premium content
        'Paramount+',
        'Apple TV+',
        'Peacock',
        'Discovery+',
        'ESPN+',
        'YouTube TV'
    ]
    return app_name in drm_apps


def check_dependencies():
    """Check for required dependencies and prompt for installation."""
    missing_deps = []
    
    # Check for ffmpeg
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        print("✓ ffmpeg found")
    except (subprocess.CalledProcessError, FileNotFoundError):
        missing_deps.append(('ffmpeg', 'brew install ffmpeg'))
    
    # Check for brew (required for installing ffmpeg)
    if missing_deps:
        try:
            subprocess.run(['brew', '--version'], capture_output=True, check=True)
            print("✓ Homebrew found")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("✗ Homebrew not found")
            print("Homebrew is required to install dependencies.")
            print("Please install Homebrew first: https://brew.sh/")
            return False
    
    if missing_deps:
        print("\nMissing dependencies:")
        for dep_name, install_cmd in missing_deps:
            print(f"✗ {dep_name}")
        
        print(f"\nTo install missing dependencies, run:")
        for dep_name, install_cmd in missing_deps:
            print(f"  {install_cmd}")
        
        install_now = input(f"\nInstall missing dependencies now? (Y/n): ").strip().lower()
        if install_now in ['', 'y', 'yes']:
            for dep_name, install_cmd in missing_deps:
                print(f"\nInstalling {dep_name}...")
                try:
                    subprocess.run(install_cmd.split(), check=True)
                    print(f"✓ {dep_name} installed successfully")
                except subprocess.CalledProcessError as e:
                    print(f"✗ Failed to install {dep_name}: {e}")
                    return False
            print("\nAll dependencies installed successfully!")
            return True
        else:
            print("Installation cancelled. Dependencies are required to run this script.")
            return False
    
    return True


def get_running_apps():
    """Get list of currently running desktop applications excluding system processes."""
    try:
        # Use osascript to get list of running applications
        script = '''
        tell application "System Events"
            set appList to {}
            repeat with proc in (every process whose background only is false)
                try
                    if (count of windows of proc) > 0 then
                        set appList to appList & (name of proc)
                    end if
                end try
            end repeat
            return appList
        end tell
        '''
        result = subprocess.run(['osascript', '-e', script], 
                              capture_output=True, text=True, check=True)
        
        apps_str = result.stdout.strip()
        if apps_str:
            apps = apps_str.split(', ')
        else:
            apps = []
        
        # Filter out Terminal, system processes, and background apps
        system_processes = [
            'Terminal', 'Finder', 'Dock', 'SystemUIServer', 'Control Center',
            'WindowServer', 'loginwindow', 'Spotlight', 'NotificationCenter',
            'StatusBarServer', 'UserEventAgent', 'TextInputMenuAgent'
        ]
        
        filtered_apps = [app for app in apps if app not in system_processes and app.strip()]
        
        # Sort alphabetically for better user experience
        filtered_apps.sort()
        return filtered_apps
        
    except subprocess.CalledProcessError as e:
        print(f"Error getting running apps: {e}")
        return []


def get_app_window_info(app_name):
    """Get window information for the specified app."""
    try:
        script = f'''
        tell application "System Events"
            tell process "{app_name}"
                if exists window 1 then
                    set pos to position of window 1
                    set sz to size of window 1
                    return (item 1 of pos as string) & "," & (item 2 of pos as string) & "," & (item 1 of sz as string) & "," & (item 2 of sz as string)
                end if
            end tell
        end tell
        '''
        result = subprocess.run(['osascript', '-e', script], 
                              capture_output=True, text=True, check=True)
        coords = result.stdout.strip()
        if coords:
            x, y, width, height = map(int, coords.split(','))
            return {'x': x, 'y': y, 'width': width, 'height': height}
        return None
    except (subprocess.CalledProcessError, ValueError):
        return None


def record_screen(duration=60, output_file=None, window_info=None):
    """Record the screen for specified duration using ffmpeg."""
    if output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"screen_recording_{timestamp}.mov"
    
    print(f"Starting screen recording for {duration} seconds...")
    print("3...")
    time.sleep(1)
    print("2...")
    time.sleep(1)
    print("1...")
    time.sleep(1)
    print("Recording!")
    
    try:
        # Use ffmpeg to record the screen (no audio)
        cmd = [
            'ffmpeg',
            '-f', 'avfoundation',
            '-i', '1',  # Screen capture device only
            '-t', str(duration),
            '-r', '30',  # 30 fps
            '-vcodec', 'libx264',
            '-preset', 'ultrafast',
            '-pix_fmt', 'yuv420p',  # Better compatibility
            '-y',  # Overwrite output file
        ]
        
        if window_info:
            # Add crop filter for specific window
            cmd.extend(['-vf', f'crop={window_info["width"]}:{window_info["height"]}:{window_info["x"]}:{window_info["y"]}'])
        
        cmd.append(output_file)
        
        # Start ffmpeg in background and show timer
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Set terminal to raw mode for ESC detection
        old_settings = termios.tcgetattr(sys.stdin)
        tty.setraw(sys.stdin.fileno())
        
        try:
            # Show timer during recording with more frequent ESC checking
            start_time = time.time()
            last_second = -1
            
            while time.time() - start_time < duration:
                elapsed = int(time.time() - start_time)
                remaining = duration - elapsed
                
                # Only update display once per second to avoid flickering
                if elapsed != last_second:
                    print(f"\rRecording... {remaining}s remaining (Press ESC to stop)", end="", flush=True)
                    last_second = elapsed
                
                # Check for ESC key press more frequently (every 0.1s)
                if check_for_escape():
                    print("\n\nStopping recording...")
                    process.terminate()
                    process.wait()
                    break
                    
                time.sleep(0.1)  # Check ESC every 100ms instead of 1 second
            else:
                # Wait for process to complete if not interrupted
                process.wait()
                
        finally:
            # Restore terminal settings
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
        
        print(f"\nRecording completed! Saved as: {output_file}")
        return output_file
        
    except subprocess.CalledProcessError as e:
        print(f"Error during recording: {e}")
        print("Make sure Screen Recording permission is enabled in System Preferences > Security & Privacy > Privacy > Screen Recording")
        return None
    except FileNotFoundError:
        print("Error: ffmpeg not found. Please install ffmpeg using: brew install ffmpeg")
        return None


def main():
    # Clear the screen first
    os.system('clear')
    
    print("Screen Recording Tool for macOS")
    print("=" * 32)
    
    # Check dependencies first
    if not check_dependencies():
        print("Exiting due to missing dependencies.")
        sys.exit(1)
    
    print()  # Add blank line after dependency check
    
    # Get running applications
    apps = get_running_apps()
    
    if not apps:
        print("No suitable applications found for recording.")
        return
    
    print("Currently running applications:")
    has_drm_apps = False
    for i, app in enumerate(apps, 1):
        drm_label = " (DRM Protected)" if is_drm_protected_app(app) else ""
        if drm_label:
            has_drm_apps = True
        print(f"{i}. {app}{drm_label}")
    
    # Show warning if DRM apps are present
    if has_drm_apps:
        print("\n⚠️  Warning: DRM Protected apps will show black screen during recording")
        print("   due to copyright protection. Choose non-DRM apps for successful recording.")
    
    # Let user choose which app to focus on (optional)
    print(f"\nFound {len(apps)} running application(s).")
    
    if len(apps) == 1:
        selected_app = apps[0]
        print(f"Will record with {selected_app} in focus.")
    else:
        try:
            choice = input(f"\nEnter number (1-{len(apps)}) to select app, press Enter for default (1), or type 'exit' to quit: ").strip()
            if choice.lower() in ['exit', 'quit', 'q']:
                print("Exiting...")
                sys.exit(0)
            elif choice:
                selected_app = apps[int(choice) - 1]
                print(f"Selected: {selected_app}")
            else:
                selected_app = apps[0]  # Default to first app
                print(f"Selected: {selected_app} (default)")
        except (ValueError, IndexError):
            print("Invalid selection. Using default (first app).")
            selected_app = apps[0]
    
    # Confirm recording
    print("\n💡 Tip: Press ESC during recording to stop early")
    confirm = input(f"\nRecord {selected_app} for 60 seconds? (Y/n): ").strip().lower()
    
    if confirm in ['', 'y', 'yes']:
        # Get window info but keep Terminal in focus for ESC key detection
        window_info = None
        if selected_app != "entire screen":
            try:
                # Temporarily bring selected app to front to get window info
                subprocess.run(['osascript', '-e', f'tell application "{selected_app}" to activate'], 
                             check=True)
                time.sleep(0.5)  # Brief pause to get window info
                
                # Get window coordinates
                window_info = get_app_window_info(selected_app)
                
                # Bring Terminal back to front for ESC key detection
                subprocess.run(['osascript', '-e', 'tell application "Terminal" to activate'], 
                             check=True)
                time.sleep(0.5)  # Give Terminal time to come to front
                
                if window_info:
                    print(f"Recording {selected_app} window at {window_info['width']}x{window_info['height']}")
                    print("Terminal kept in focus for ESC key detection")
                else:
                    print(f"Could not get window info for {selected_app}, recording entire screen")
                    
            except subprocess.CalledProcessError:
                print(f"Could not manage window focus, recording anyway...")
        
        # Start recording
        output_file = record_screen(duration=60, window_info=window_info)
        
        if output_file and os.path.exists(output_file):
            print("Recording session complete.")
    else:
        print("Recording cancelled.")
        sys.exit(0)


if __name__ == "__main__":
    main()