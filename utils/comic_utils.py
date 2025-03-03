import nltk
import logging

# Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Download punkt tokenizer (if not already downloaded)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    logging.info("Downloading punkt tokenizer...")
    nltk.download('punkt')

def split_into_scenes(text):
    """Splits the text into scenes."""
    if not text:
        logging.warning("Received empty text to split into scenes.")
        return []

    try:
        # Use nltk to split the text into sentences
        sentences = nltk.sent_tokenize(text)
        scenes = [sentence.strip() for sentence in sentences if sentence.strip()]
        logging.info(f"Text successfully split into {len(scenes)} scenes.")
        return scenes
    except Exception as e:
        logging.error(f"Error splitting the text into scenes: {e}")
        return []