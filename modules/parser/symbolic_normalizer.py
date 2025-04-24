# symbolic_normalizer.py

try:
    from nltk.stem import WordNetLemmatizer
    lemmatizer = WordNetLemmatizer()
    _lemmatizer_available = True
except ImportError:
    lemmatizer = None
    _lemmatizer_available = False

def normalize_noun(word):
    if not isinstance(word, str):
        return word
    word = word.strip().lower()
    if _lemmatizer_available:
        return lemmatizer.lemmatize(word, pos='n')
    return word  # fallback: return original if lemmatizer is missing
