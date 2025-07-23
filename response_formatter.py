def format_response(question, result):
    if "error" in result:
        return "⚠️ Error: " + result["error"]
    if not result:
        return "No results found."
    
    values = list(result[0].values())
    return f"Answer: {values[0]}"
