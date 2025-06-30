import json
import re

results = []

# Process each input item
for item in _input.all():
    input_text = ""
    
    # Try to extract from OpenAI API response structure
    if "choices" in item.json and len(item.json["choices"]) > 0:
        if "message" in item.json["choices"][0] and "content" in item.json["choices"][0]["message"]:
            input_text = item.json["choices"][0]["message"]["content"]
    # Fallback to other possible structures
    elif "message" in item.json and "text" in item.json["message"]:
        input_text = item.json["message"]["text"]
    elif "output" in item.json:
        input_text = item.json["output"]
    elif "text" in item.json:
        input_text = item.json["text"]
    elif "content" in item.json:
        input_text = item.json["content"]

    # Process the extracted text
    try:
        # Get the input text
        raw_text = input_text.strip()
        
        # Step 1: Remove markdown code blocks if present
        # Remove ```json at the beginning
        cleaned_text = re.sub(r'^```json\s*', '', raw_text, flags=re.MULTILINE)
        # Remove ``` at the end
        cleaned_text = re.sub(r'\s*```$', '', cleaned_text, flags=re.MULTILINE)
        
        # Step 2: Replace escaped newlines with actual newlines
        cleaned_text = cleaned_text.replace('\\n', '\n')
        
        # Step 3: Try to parse as JSON
        parsed_json = json.loads(cleaned_text)
        
        # Success case
        results.append({
            "json": {
                "success": True,
                "json_ticket": parsed_json,
                "error": None
            }
        })
        
    except json.JSONDecodeError as e:
        # Try additional cleaning if first attempt fails
        try:
            # More aggressive cleaning
            # Remove any remaining escape characters
            alt_cleaned = re.sub(r'\\(.)', r'\1', raw_text)
            
            # Remove markdown blocks again
            alt_cleaned = re.sub(r'^```json\s*', '', alt_cleaned, flags=re.MULTILINE)
            alt_cleaned = re.sub(r'\s*```$', '', alt_cleaned, flags=re.MULTILINE)
            
            # Try parsing again
            parsed_json = json.loads(alt_cleaned)
            
            # Success on second attempt
            results.append({
                "json": {
                    "success": True,
                    "json_ticket": parsed_json,
                    "error": None
                }
            })
            
        except json.JSONDecodeError as e2:
            # Final failure
            results.append({
                "json": {
                    "success": False,
                    "json_ticket": None,
                    "error": f"JSON Parse Error: {str(e2)}",
                    "original_text": raw_text[:500] + "..." if len(raw_text) > 500 else raw_text
                }
            })

    except Exception as e:
        # Unexpected error
        results.append({
            "json": {
                "success": False,
                "json_ticket": None,
                "error": f"Unexpected Error: {str(e)}",
                "original_text": input_text[:500] + "..." if len(input_text) > 500 else input_text
            }
        })

return results