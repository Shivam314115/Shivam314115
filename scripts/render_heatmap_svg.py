import json
import os

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]

def render_heatmap():
    try:
        with open("data/contributions.json", "r") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Could not read data: {e}")
        return

    days = data.get("days", [])
    total = data.get("total", 0)
    
    width = 860
    height = 200
    box_size = 11
    gap = 4
    
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">\n'
    svg += '  <style>\n'
    svg += '    .text { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; font-size: 12px; fill: #7d8590; }\n'
    svg += '    .stat { font-size: 14px; fill: #c9d1d9; font-weight: bold; }\n'
    svg += '    .box { opacity: 0; rx: 2px; ry: 2px; }\n'
    svg += '    @keyframes slideDown {\n'
    svg += '      0% { opacity: 0; transform: translateY(-10px); }\n'
    svg += '      100% { opacity: 1; transform: translateY(0); }\n'
    svg += '    }\n'
    svg += '  </style>\n'
    
    svg += f'  <rect width="{width}" height="{height}" fill="transparent" />\n'
    svg += f'  <text class="text stat" x="20" y="30">{total:,} contributions in the last year</text>\n'
    
    g_x = 20
    g_y = 50
    svg += f'  <g transform="translate({g_x}, {g_y})">\n'
    
    col = 0
    row = 0
    
    for i, day in enumerate(days):
        level = min(day.get("level", 0), len(PALETTE) - 1)
        color = PALETTE[level]
        
        x = col * (box_size + gap)
        y = row * (box_size + gap)
        
        delay = (col * 0.02) + (row * 0.05)
        
        svg += f'    <rect class="box" x="{x}" y="{y}" width="{box_size}" height="{box_size}" fill="{color}">\n'
        svg += f'      <animate attributeName="opacity" values="0;1" dur="0.5s" begin="{delay}s" fill="freeze" />\n'
        svg += f'      <animateTransform attributeName="transform" type="translate" from="0 -10" to="0 0" dur="0.5s" begin="{delay}s" fill="freeze" />\n'
        svg += f'    </rect>\n'
        
        row += 1
        if row >= 7:
            row = 0
            col += 1
            
    svg += '  </g>\n'
    
    legend_x = width - 150
    legend_y = g_y + 7 * (box_size + gap) + 15
    svg += f'  <g transform="translate({legend_x}, {legend_y})">\n'
    svg += f'    <text class="text" x="0" y="10">Less</text>\n'
    for i, color in enumerate(PALETTE):
        svg += f'    <rect x="{35 + i * (box_size + 4)}" y="0" width="{box_size}" height="{box_size}" fill="{color}" rx="2" ry="2" />\n'
    svg += f'    <text class="text" x="{35 + len(PALETTE) * (box_size + 4) + 5}" y="10">More</text>\n'
    svg += '  </g>\n'
    
    svg += '</svg>'
    
    with open("contrib-heatmap.svg", "w") as f:
        f.write(svg)
    print("Generated contrib-heatmap.svg successfully.")

if __name__ == "__main__":
    render_heatmap()
