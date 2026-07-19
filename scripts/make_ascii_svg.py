import sys
import os
from PIL import Image

RAMP = " .`:-=+*cs#%@"

def make_ascii_svg(image_path, output_path, width=100):
    if not os.path.exists(image_path):
        print(f"Error: Could not find prepped image at {image_path}")
        sys.exit(1)
        
    try:
        img = Image.open(image_path).convert('L')
    except Exception as e:
        print(f"Error opening image: {e}")
        return

    aspect_ratio = img.height / img.width
    new_height = int(width * aspect_ratio * 0.5)
    img = img.resize((width, new_height))
    
    pixels = img.getdata()
    ascii_str = ""
    for pixel in pixels:
        index = int((255 - pixel) / 255 * (len(RAMP) - 1))
        ascii_str += RAMP[index]
    
    lines = [ascii_str[i:i+width] for i in range(0, len(ascii_str), width)]
    
    svg_height = new_height * 12 + 20
    svg_width = width * 7 + 20
    
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">\n'
    svg += '  <style>\n'
    svg += '    text { font-family: monospace; font-size: 12px; fill: #a3b3cc; white-space: pre; }\n'
    svg += '  </style>\n'
    svg += '  <rect width="100%" height="100%" fill="transparent" />\n'
    
    for i, line in enumerate(lines):
        y = 20 + i * 12
        line = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        
        svg += f'  <clipPath id="clip-{i}">\n'
        svg += f'    <rect x="0" y="{y-10}" width="0" height="15">\n'
        svg += f'      <animate attributeName="width" from="0" to="{svg_width}" dur="0.5s" begin="{i*0.02}s" fill="freeze" />\n'
        svg += f'    </rect>\n'
        svg += f'  </clipPath>\n'
        
        svg += f'  <text x="10" y="{y}" clip-path="url(#clip-{i})">{line}</text>\n'
        
    svg += '</svg>\n'
    
    with open(output_path, 'w') as f:
        f.write(svg)
    print(f"Generated {output_path} successfully.")

if __name__ == "__main__":
    img_path = "source-prepped.png"
    if len(sys.argv) > 1:
        img_path = sys.argv[1]
    make_ascii_svg(img_path, "avi-ascii.svg")
