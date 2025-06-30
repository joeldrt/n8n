import re

# Characters that need to be escaped in MarkdownV2
MARKDOWNV2_ESCAPE_CHARS = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']

def escape_markdownv2(text):
    """
    Escape all MarkdownV2 special characters in text
    """
    if not text:
        return ""
    
    # Convert to string if not already
    text = str(text)
    
    # Escape each special character
    for char in MARKDOWNV2_ESCAPE_CHARS:
        text = text.replace(char, '\\' + char)
    
    return text

def process_markdownv2_message(message):
    """
    Process a message to ensure it's correctly escaped for MarkdownV2
    Maintains markdown formatting but escapes special characters
    """
    if not message:
        return ""
    
    # Convert to string
    message = str(message).strip()
    
    # MarkdownV2 formatting patterns (correct syntax)
    # Bold: *text*
    bold_pattern = r'\*(.*?)\*'
    # Italic: _text_
    italic_pattern = r'_(.*?)_'
    # Underline: __text__
    underline_pattern = r'__(.*?)__'
    # Strikethrough: ~text~
    strikethrough_pattern = r'~(.*?)~'
    # Code: `text`
    code_pattern = r'`(.*?)`'
    # Spoiler: ||text||
    spoiler_pattern = r'\|\|(.*?)\|\|'
    
    # Find all markdown entities
    bold_matches = re.findall(bold_pattern, message)
    italic_matches = re.findall(italic_pattern, message)
    underline_matches = re.findall(underline_pattern, message)
    strikethrough_matches = re.findall(strikethrough_pattern, message)
    code_matches = re.findall(code_pattern, message)
    spoiler_matches = re.findall(spoiler_pattern, message)
    
    # Create temporary placeholders
    temp_message = message
    placeholders = {}
    counter = 0
    
    # Replace bold content with placeholders
    for match in bold_matches:
        placeholder = f"BOLDPLACEHOLDER{counter}"
        placeholders[placeholder] = f"*{escape_markdownv2(match)}*"
        temp_message = temp_message.replace(f"*{match}*", placeholder, 1)
        counter += 1
    
    # Replace italic content with placeholders
    for match in italic_matches:
        placeholder = f"ITALICPLACEHOLDER{counter}"
        placeholders[placeholder] = f"_{escape_markdownv2(match)}_"
        temp_message = temp_message.replace(f"_{match}_", placeholder, 1)
        counter += 1
    
    # Replace underline content with placeholders
    for match in underline_matches:
        placeholder = f"UNDERLINEPLACEHOLDER{counter}"
        placeholders[placeholder] = f"__{escape_markdownv2(match)}__"
        temp_message = temp_message.replace(f"__{match}__", placeholder, 1)
        counter += 1
    
    # Replace strikethrough content with placeholders
    for match in strikethrough_matches:
        placeholder = f"STRIKEPLACEHOLDER{counter}"
        placeholders[placeholder] = f"~{escape_markdownv2(match)}~"
        temp_message = temp_message.replace(f"~{match}~", placeholder, 1)
        counter += 1
    
    # Replace code content with placeholders (code content is not escaped)
    for match in code_matches:
        placeholder = f"CODEPLACEHOLDER{counter}"
        # Inside code entities, escape ` and \ characters only
        escaped_code = match.replace('\\', '\\\\').replace('`', '\\`')
        placeholders[placeholder] = f"`{escaped_code}`"
        temp_message = temp_message.replace(f"`{match}`", placeholder, 1)
        counter += 1
    
    # Replace spoiler content with placeholders
    for match in spoiler_matches:
        placeholder = f"SPOILERPLACEHOLDER{counter}"
        placeholders[placeholder] = f"||{escape_markdownv2(match)}||"
        temp_message = temp_message.replace(f"||{match}||", placeholder, 1)
        counter += 1
    
    # Escape the rest of the text
    escaped_message = escape_markdownv2(temp_message)
    
    # Restore placeholders with formatted content
    for placeholder, formatted_content in placeholders.items():
        escaped_message = escaped_message.replace(placeholder, formatted_content)
    
    return escaped_message

# Procesar cada item de entrada
results = []

for item in _input.all():
    # Obtener el mensaje del agente
    message = ""
    
    if "output" in item.json:
        message = item.json["output"]
    elif "message" in item.json:
        message = item.json["message"]
    elif "text" in item.json:
        message = item.json["text"]
    elif "content" in item.json:
        message = item.json["content"]
    else:
        # Si no encontramos el mensaje, usar todo el JSON como string
        message = str(item.json)
    
    # Procesar el mensaje
    try:
        escaped_message = process_markdownv2_message(message)
        
        results.append({
            "json": {
                "message": escaped_message,
                "original_message": message,
                "escaped": True,
                "success": True
            }
        })
        
    except Exception as e:
        # En caso de error, devolver mensaje sin escape como fallback
        results.append({
            "json": {
                "message": str(message),
                "original_message": message,
                "escaped": False,
                "success": False,
                "error": str(e)
            }
        })

return results