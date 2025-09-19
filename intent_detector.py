# intent_detector.py

import re

# A basic example of intent detection based on keywords
def detect_intent(user_input):
    user_input = user_input.lower()

    if any(word in user_input for word in ['sad', 'depressed', 'lonely', 'upset', 'cry']):
        return "emotional_support"

    elif any(word in user_input for word in ['law', 'legal', 'rights', 'case', 'section', 'ipc']):
        return "legal_aid"

    elif any(word in user_input for word in ['help', 'emergency', 'suicide', 'abuse', 'violence']):
        return "emergency_support"

    elif any(word in user_input for word in ['doctor', 'counselor', 'therapy', 'clinic']):
        return "mental_health_resources"

    elif any(word in user_input for word in ['location', 'near me', 'closest', 'place']):
        return "location_based_support"

    return "general_support"
