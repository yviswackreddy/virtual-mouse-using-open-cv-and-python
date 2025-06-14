# Virtual Mouse Control

A Python project that uses hand tracking to control the mouse cursor via webcam. It supports cursor movement, clicking, and scrolling using hand gestures.

## Requirements
- Python 3.8+
- Webcam
- Libraries listed in `requirements.txt`

## Installation
1. Clone or download this project.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the script:
   ```bash
   python virtual_mouse.py
   ```

## Usage
- Cursor Movement**: Move your index finger to control the cursor.
- Click: Bring your thumb and index finger close together.
- Scroll: Extend index and middle fingers; move middle finger up/down relative to index finger to scroll up/down.
- Exit: Press 'q' to quit.

## Notes
- Ensure good lighting for better hand detection.
- Adjust `smoothening`, `click_threshold`, and `scroll_threshold` in the code for sensitivity.
- The webcam feed is flipped horizontally for intuitive control.
- A cooldown prevents rapid accidental clicks.

## Troubleshooting
- If the webcam doesn't open, check if it's accessible by other applications.
- If hand detection is poor, ensure proper lighting and hand visibility.
- For PyAutoGUI issues, ensure you have proper permissions on your system.
