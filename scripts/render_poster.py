import json
import re
from datetime import datetime
import os

def json_to_html(json_data, output_file='poster.html', content_lst=None):

    if isinstance(json_data, str):
        try:
            data = json.loads(json_data)
        except json.JSONDecodeError as e:
            print(f"JSON parse error: {e}")
            return
    else:
        data = json_data
    

    if 'layouts' in data:
        layers = data['layouts']
      
        if isinstance(layers, list) and len(layers) > 0 and isinstance(layers[0], str):
            try:
         
                json_str = layers[0]
                if json_str.startswith('layouts:'):
                    json_str = json_str[8:]  
                layers = json.loads(json_str)
            except json.JSONDecodeError as e:
                print(f"JSON parse error: {e}")
                return
    elif 'layers' in data:
        layers = data['layers']
    else:
        print("Error: JSON data does not contain 'layouts' or 'layers' field")
        return
    

    if not isinstance(layers, list):
        print("Error: layers data is not a list format")
        return
    

    html_template = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{data.get('id', 'poster')}</title>
    <style>
    
        {generate_font_face_css(layers)}
       
        body {{
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            font-family: Arial, sans-serif;
            background-color: #f5f5f5;
        }}
        
        .poster-container {{
            position: relative;
            width: {data.get('width')}px;
            height: {data.get('height')}px;
            background-color: #83dec7 ;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        }}
        
        .text-layer {{
            position: absolute;
            display: flex;
            box-sizing: border-box;
            opacity: 1;
        }}
        
        {generate_layer_styles(layers)}
        
        .decoration {{
            position: absolute;
            background-color: rgba(0, 0, 0, 0.05);
        }}
    </style>
</head>
<body>
    <div class="poster-container">
        {generate_layer_html(layers, content_lst)}
    </div>
    
    <script>
        console.log('poster generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}');
    </script>
</body>
</html>"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_template)
    
    print(f"success generate poster: {output_file}")

def generate_layer_styles(layers):
    styles = []
    for i, layer in enumerate(layers):
        if not isinstance(layer, dict):
            continue
            
        try:
            box = layer.get('box', {})
            text_style = layer.get('textStyle', {})
            
            align_map = {
                'center': 'center',
                'left': 'flex-start',
                'right': 'flex-end'
            }
            align = align_map.get(text_style.get('textAlign', 'left'), 'flex-start')
            
            style = f"""
        #layer-{i} {{
            width: {box[0]}px;
            height: {box[1]}px;
            top: {box[2]}px;
            left: {box[3]}px;
            font-size: {text_style.get('fontSize', 16)}px;
            font-family: '{text_style.get('fontFamily', 'Arial')}';
            color: {hex_to_rgba(text_style.get('color', '#000000'))};
            text-align: {text_style.get('textAlign', 'left')};
            line-height: {text_style.get('lineHeight', 1.2)};
            font-weight: {text_style.get('fontWeight', 400)};
            writing-mode: {text_style.get('writingMode', 'horizontal-tb')};
            opacity: {layer.get('opacity', 1)};
            display: flex;
            justify-content: {align};
            align-items: {align};
            transform: matrix({', '.join(str(x) for x in layer.get("transform", (1.0, 0.0, 0.0, 1.0, 0.0, 0.0)))});

            {get_text_effects(layer)}
        }}"""
            
            styles.append(style)
        except Exception as e:
            print(f"error in layer {i}: {e}")
            continue
    
    return '\n'.join(styles)

def generate_layer_html(layers, content_lst=None):
    html = []
    for i, layer in enumerate(layers):
        if not isinstance(layer, dict):
            continue
            
        if content_lst is not None:
            content = content_lst[i]
        if '\\n' in content:
            content = content.replace('\\n', '<br>')
        content = re.sub(r'\\u([0-9a-fA-F]{4})', lambda m: chr(int(m.group(1), 16)), content)
        
        html.append(f'<div class="text-layer" id="layer-{i}">{content}</div>')
    
    return '\n        '.join(html)

def hex_to_rgba(hex_color):

    if not hex_color.startswith('#'):
        hex_color = '#' + hex_color
    
    hex_color = hex_color[:9]
    
    if len(hex_color) == 9:  
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
        a = int(hex_color[7:9], 16) / 255
        return f'rgba({r}, {g}, {b}, {a})'
    elif len(hex_color) == 7:  
        return hex_color
    else:
        return '#000000'  

def get_text_effects(layer):

    effects = []
    
    if 'textEffects' in layer and layer['textEffects']:
        for effect in layer['textEffects']:
            if effect.get('enable', True):

                if effect.get('stroke', {}).get('enable', False):
                    stroke = effect['stroke']
                    effects.append(f"-webkit-text-stroke: {stroke['width']}px {hex_to_rgba(stroke['color'])};")
                

                if effect.get('shadow', {}).get('enable', False):
                    shadow = effect['shadow']
                    effects.append(f"text-shadow: {shadow.get('offsetX', 0)}px {shadow.get('offsetY', 0)}px {shadow.get('blur', 0)}px {hex_to_rgba(shadow['color'])};")
                

                if effect.get('filling', {}).get('enable', False) and effect['filling'].get('type', 0) == 1:
                    gradient = effect['filling']['gradient']
                    stops = []
                    for stop in gradient['stops']:
                        stops.append(f"{hex_to_rgba(stop['color'])} {int(stop['offset']*100)}%")
                    gradient_css = f"background: linear-gradient({gradient.get('angle', 0)}deg, {', '.join(stops)});"
                    gradient_css += "-webkit-background-clip: text; background-clip: text;"
                    gradient_css += "-webkit-text-fill-color: transparent;"
                    effects.append(gradient_css)
    
    return '\n            '.join(effects)

def generate_font_face_css(layers):

    font_families = set()
    for layer in layers:
        if isinstance(layer, dict):
            text_style = layer.get('textStyle', {})
            font = text_style.get('fontFamily')
            if font:
                font_families.add(font)
    css = []
    for font in font_families:
        css.append(
            f"""@font-face {{
    font-family: '{font}';
    src: url('../../downloaded_fonts/{font}.ttf') format('truetype');
}}"""
        )
    return '\n'.join(css)


if __name__ == '__main__':
    with open('/results/layout.json', 'r', encoding='utf-8') as f:
        all_json = json.load(f)

    if isinstance(all_json, list):
        for idx, item in enumerate(all_json):

            layers = []
            if 'generated_layout' in item:
                generated_layout = item['generated_layout']
                if isinstance(generated_layout, str):
                    try:

                        if generated_layout.startswith('layouts:'):
                            json_str = generated_layout[8:]  
                        else:
                            json_str = generated_layout
                        
                        
                        item['layers'] = json.loads(json_str)
                        layers = item['layers']
                       
                        
                        if not isinstance(layers, list):
                            layers = []
                            
                    except json.JSONDecodeError as e:
                        print(f"JSON parse error: {e}")
                        print(f"original string: {generated_layout[:100]}...")
                        layers = []
                    except Exception as e:
                        print(f"error in generated_layout: {e}")
                        layers = []
                else:
                    layers = []
            else:
                if 'layers' in item:
                    layers = item['layers']
                else:
                    layers = []


            content_lst = item['content_lst']
            

            html_name = f'/html/{item.get("id", idx)}.html'
            os.makedirs(f'/html', exist_ok=True)
            if content_lst is not None and len(content_lst) == len(layers):
                json_to_html(item, html_name, content_lst)
            
    else:
        print("unknown json structure")



