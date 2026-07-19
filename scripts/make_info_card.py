import os

def generate_info_card():
    title = "shivam@github ~"
    fields = [
        {"key": "Role", "value": "Software Engineer"},
        {"key": "Stack", "value": "Python, TypeScript, React, Go"},
        {"key": "Currently", "value": "Building cool side projects"},
        {"key": "Learning", "value": "SVG Animations & GitHub Actions"},
        {"key": "Hobbies", "value": "Design, Open Source, Automation"}
    ]
    
    width = 490
    height = 250
    
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">\n'
    svg += '  <style>\n'
    svg += '    .bg { fill: #0d1117; stroke: #30363d; stroke-width: 1; rx: 6px; }\n'
    svg += '    .text { font-family: "Courier New", monospace; font-size: 14px; }\n'
    svg += '    .title { fill: #58a6ff; font-weight: bold; }\n'
    svg += '    .key { fill: #3fb950; font-weight: bold; }\n'
    svg += '    .value { fill: #c9d1d9; }\n'
    svg += '    .line { opacity: 0; }\n'
    
    svg += '    @keyframes fadeSlideIn {\n'
    svg += '      0% { opacity: 0; transform: translateX(-10px); }\n'
    svg += '      100% { opacity: 1; transform: translateX(0); }\n'
    svg += '    }\n'
    
    is_static = os.environ.get("STATIC") == "1"
    
    if not is_static:
        for i in range(len(fields) + 2):
            delay = 0.5 + i * 0.2
            svg += f'    .line-{i} {{ animation: fadeSlideIn 0.4s ease forwards {delay}s; }}\n'
    else:
        svg += '    .line { opacity: 1; }\n'
        
    svg += '  </style>\n'
    
    svg += f'  <rect class="bg" x="5" y="5" width="{width-10}" height="{height-10}" />\n'
    
    svg += f'  <g class="line line-0">\n'
    svg += f'    <text class="text title" x="25" y="40">{title}</text>\n'
    svg += f'    <text class="text value" x="25" y="55">{"-" * 40}</text>\n'
    svg += f'  </g>\n'
    
    y_offset = 85
    for i, field in enumerate(fields):
        svg += f'  <g class="line line-{i+1}">\n'
        svg += f'    <text class="text key" x="25" y="{y_offset}">{field["key"]}</text>\n'
        svg += f'    <text class="text value" x="120" y="{y_offset}">: {field["value"]}</text>\n'
        svg += f'  </g>\n'
        y_offset += 25
        
    colors = ['#ff7b72', '#ffa657', '#3fb950', '#a5d6ff', '#79c0ff', '#d2a8ff']
    svg += f'  <g class="line line-{len(fields)+1}">\n'
    for i, color in enumerate(colors):
        svg += f'    <rect x="{25 + i * 20}" y="{height - 40}" width="15" height="15" fill="{color}" rx="2" />\n'
    svg += f'  </g>\n'
        
    svg += '</svg>'
    
    with open("info-card.svg", "w") as f:
        f.write(svg)
    print("Generated info-card.svg successfully.")

if __name__ == "__main__":
    generate_info_card()
