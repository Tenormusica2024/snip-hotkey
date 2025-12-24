# snip_hotkey

[日本語](README.md) | **English**

A Windows utility that automatically saves screenshots copied via Snipping Tool to PNG files and inputs their paths (with quotes) into the active PowerShell (Claude CLI) window.

## Features

- **Hotkey**: F8 (Global)
- **Save Location**: `C:\Users\{USERNAME}\Documents\snips` (customizable via `SNIP_HOTKEY_SAVE_DIR` environment variable)
- **Log File**: `snip_hotkey.log` (same directory)
- **Retry Logic**: Attempts to grab image from clipboard up to 5 times with 0.1-second intervals before saving
- **Auto Input**: Inputs file path with quotes like `"C:\path\to\file.png"` into active window
- **Long-term Stability**: Uses Win32 `RegisterHotKey` API to prevent hotkey disconnection during extended operation
- **Detailed Specification**: See `snip_hotkey_spec.md`

## Setup Instructions

1. Clone this repository or download the files
2. Navigate to the directory containing `snip_hotkey.py`
3. Install Python libraries:
   ```cmd
   pip install Pillow keyboard
   ```
4. Run the application:
   - **Background mode (recommended)**: `pythonw snip_hotkey.py`
   - **Normal mode (with log display)**: `python snip_hotkey.py`

## Auto-Startup Setup (Windows)

Copy the startup batch file to Windows Startup folder:
```cmd
copy snip_hotkey_start.cmd "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\"
```

Alternatively, you can manually copy `snip_hotkey_start.cmd` to:
`C:\Users\{USERNAME}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\`

## Usage

1. Copy an image to clipboard using **Snipping Tool** or any screenshot tool
2. **Focus** on Claude CLI's PowerShell window
3. Press **F8** - the image will be saved to the `snips` folder and the file path will be automatically typed into PowerShell (if the path doesn't appear immediately, try pressing arrow keys to refresh the display)

## Environment Variables

You can customize the behavior using these environment variables:

- `SNIP_HOTKEY_SAVE_DIR`: Image save directory (default: `%USERPROFILE%\Documents\snips`)
- `SNIP_HOTKEY_LOG_PATH`: Log file path (default: `snip_hotkey.log`)

## Manual Restart

Use `restart_snip_hotkey.cmd` to manually restart the application:
- Stops any existing `snip_hotkey.py` processes
- Restarts in hidden mode using `pythonw`

## Requirements

- **Windows OS**
- **Python 3.7+**
- **Required Libraries**:
  - `Pillow` (PIL) - for image processing
  - `keyboard` - for hotkey functionality

## File Structure

```
snip_hotkey/
├── snip_hotkey.py          # Main application
├── restart_snip_hotkey.cmd # Manual restart script
├── snip_hotkey_start.cmd   # Startup script for auto-launch
├── README.md               # Japanese documentation
├── README_EN.md            # English documentation
└── snip_hotkey_spec.md     # Detailed specifications
```

## Troubleshooting

### "RegisterHotKey failed" Error
- This typically means another instance of `snip_hotkey.py` is already running
- Use `restart_snip_hotkey.cmd` to stop the existing process and restart

### F8 Key Not Working
- Check if another application is using the F8 global hotkey
- Verify that the application is running by checking `snip_hotkey.log`

### Permission Errors
- Ensure the save directory exists and is writable
- Run PowerShell as Administrator if necessary

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## License

This project is open source. Please check the repository for license information.

---

**Note**: This tool is designed primarily for use with Claude CLI, but it can be adapted for other PowerShell-based workflows where automatic file path input is useful.