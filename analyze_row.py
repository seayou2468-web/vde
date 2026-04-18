from PIL import Image
import os

def analyze(path):
    if not os.path.exists(path): return
    img = Image.open(path).convert("RGB")
    w, h = img.size
    print(f"Analyzing {path} ({w}x{h})")
    
    # Check for red regions
    reds = []
    for y in range(h):
        for x in range(w):
            r, g, b = img.getpixel((x, y))
            if r > 150 and g < 130 and b < 130:
                reds.append((x, y))
                
    if reds:
        print(f"  Found {len(reds)} red pixels.")
        # Calculate bounding box
        min_x = min(p[0] for p in reds)
        max_x = max(p[0] for p in reds)
        min_y = min(p[1] for p in reds)
        max_y = max(p[1] for p in reds)
        print(f"  Red BBox: ({min_x}, {min_y}) to ({max_x}, {max_y})")
        print(f"  Center: ({(min_x+max_x)/2}, {(min_y+max_y)/2})")
    else:
        print("  No red pixels found.")

analyze("screenshots/s9_row_visual.png")
