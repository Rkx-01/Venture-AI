import re

def validate_startup_idea(text: str) -> bool:
    """
    Validates if the provided text is a meaningful startup idea.
    
    Rules:
    - Minimum length: 10 characters
    - Must contain alphabetical characters
    - Minimum 3 words
    - Reject high-entropy/gibberish strings (basic heuristic)
    """
    if not text or len(text.strip()) < 10:
        return False

    # Check for at least some alphabetical characters
    if not re.search(r'[a-zA-Z]', text):
        return False

    # Check for at least 3 words
    words = text.split()
    if len(words) < 3:
        return False

    # Heuristic for gibberish: 
    # 1. Very long words with no vowels
    # 2. Too many repeating characters
    for word in words:
        if len(word) > 15:
            # Check vowel ratio in long words
            vowels = re.findall(r'[aeiouAEIOU]', word)
            if not vowels or len(vowels) / len(word) < 0.1:
                return False
        
        # Check for excessive repetition (e.g., "aaaaa")
        if re.search(r'(.)\1{4,}', word):
            return False

    return True
