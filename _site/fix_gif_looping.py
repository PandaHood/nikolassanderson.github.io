#!/usr/bin/env python3
"""
Script to convert GIFs to loop infinitely.
Requires: pillow
Install with: pip install pillow
"""

from PIL import Image
import os
import sys

def make_gif_loop_infinitely(input_path, output_path=None):
    """
    Convert a GIF to loop infinitely.
    
    Args:
        input_path: Path to input GIF
        output_path: Path to output GIF (if None, overwrites input)
    """
    if output_path is None:
        output_path = input_path
    
    # Open the GIF
    img = Image.open(input_path)
    
    # Extract all frames
    frames = []
    durations = []
    
    try:
        while True:
            frames.append(img.copy())
            # Get duration if available, default to 100ms
            durations.append(img.info.get('duration', 100))
            img.seek(img.tell() + 1)
    except EOFError:
        pass
    
    # Save with infinite loop (loop=0 means infinite)
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,  # Infinite loop
        optimize=False  # Keep original quality
    )
    
    print(f"✓ Converted {input_path} to loop infinitely")

def process_directory(directory):
    """Process all GIFs in a directory."""
    gif_files = [f for f in os.listdir(directory) if f.lower().endswith('.gif')]
    
    if not gif_files:
        print(f"No GIF files found in {directory}")
        return
    
    print(f"Found {len(gif_files)} GIF files. Processing...\n")
    
    for gif_file in gif_files:
        input_path = os.path.join(directory, gif_file)
        try:
            make_gif_loop_infinitely(input_path)
        except Exception as e:
            print(f"✗ Error processing {gif_file}: {e}")
    
    print(f"\nDone! Processed {len(gif_files)} files.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        # Default to the new_imgs directory
        target = "assets/img/new_imgs"
    
    if os.path.isdir(target):
        process_directory(target)
    elif os.path.isfile(target) and target.lower().endswith('.gif'):
        make_gif_loop_infinitely(target)
    else:
        print("Usage: python fix_gif_looping.py [path_to_gif_or_directory]")
        print("Default: processes assets/img/new_imgs/")
        sys.exit(1)
