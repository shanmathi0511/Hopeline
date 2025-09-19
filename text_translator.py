from deep_translator import GoogleTranslator

def translate_text(text, target_lang="hi"):
    # Map friendly names to language codes
    lang_map = {
        "Hindi": "hi",
        "Tamil": "ta",
        "Telugu": "te",
        "English": "en"
    }

    try:
        # Get the language code
        lang_code = lang_map.get(target_lang, "en")
        
        # Translate the text
        translated = GoogleTranslator(source='auto', target=lang_code).translate(text)
        return translated
    except Exception as e:
        return f"⚠️ Translation failed: {e}"
