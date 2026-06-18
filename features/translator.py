from deep_translator import GoogleTranslator
def transletor(text):
    translated = GoogleTranslator(
        source='fa',
        target='en'
    ).translate(text)

    return translated