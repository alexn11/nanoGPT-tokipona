import re

from unidecode import unidecode

from language_core import nimi_ale, toki_pona_syllables, digits, punctuations, toki_pona_letters, non_toki_pona_letters

toki_pona_syllables_upper = [ s.upper() for s in toki_pona_syllables ]
tokens_multiletters = nimi_ale + toki_pona_syllables_upper
tokens_symbols_and_numbers = digits + punctuations
tokens_letters = toki_pona_letters + non_toki_pona_letters
tokens_single_letters = tokens_letters + tokens_symbols_and_numbers
language_tokens = tokens_multiletters + tokens_single_letters
unknown_token = len(language_tokens)
language_tokens += [ '#unk', ]

token_nimi_start_id = 0
token_nimi_end_id = len(nimi_ale)
token_syllable_start_id = len(nimi_ale)
token_syllable_end_id = len(nimi_ale + toki_pona_syllables)
token_punctuation_start_id = len(tokens_multiletters + tokens_letters + digits)
token_punctuation_end_id = len(tokens_multiletters + tokens_letters + digits + punctuations)
token_single_letters_start_id = len(tokens_multiletters)
token_letters_start_id = token_single_letters_start_id
token_letters_end_id = len(tokens_multiletters + tokens_letters)

# todo: tokipona tokenizer class
""" 
{
   '„': '"',
   '“': '"',
   '”': '"',
   '–': '-',
   'ß': 'ss',
   '€': 'euro',
   '\u200b': ' ',
   'â': 'a', 'ã', 'ç','т','е', 'л', 'о', '^'
   'ъ': '',
   'ь': '',
} """

def check_if_token_is_nimi(token_id):
    return token_nimi_start_id <= token_id < token_nimi_end_id

def check_if_token_is_syllable(token_id):
    return token_syllable_start_id <= token_id < token_syllable_end_id

def check_if_token_is_punctuation(token_id):
    return token_punctuation_start_id <= token_id < token_punctuation_end_id

def check_if_token_is_letter(token_id):
    return token_letters_start_id <= token_id < token_letters_end_id

#

def check_if_is_end_type_punctuation(character):
    return character in ',;:.!?>)]}'

def check_if_start_type_punctuation(character):
    return character in '([{<'

def normalise_characters(document: str) -> str:
    normalised_document = unidecode(document).lower()
    #normalised_document = re.sub(r'[„“]','"', normalised_document)
    #normalised_document = normalised_document.replace('–', '-')
    #normalised_document = normalised_document.replace('ß', 'ss')
    return normalised_document

# test:
# 'this is a test. try to see. if this work?! 1235498'
# 'this is a test . try to see . if this work ? ! 1 2 3 5 4 9 8'
def prepare_document(document: str) -> str: # "..._for_tokenizer" will be duplicate when inside class
    prepared_document = normalise_characters(document)
    prepared_document = re.sub(r'([a-z])([^a-z ])', r'\1 \2', prepared_document)
    prepared_document = re.sub(r'([^a-z ])([a-z])', r'\1 \2', prepared_document)
    prepared_document = re.sub(r'([^a-z ])([^a-z ])', r'\1 \2', prepared_document)
    prepared_document = re.sub(r'([^a-z ])([^a-z ])', r'\1 \2', prepared_document)
    prepared_document = prepared_document.strip()
    words_and_symbol = prepared_document.split()
    return words_and_symbol

# there must be a better way...
def split_into_syllables(word: str) -> list[str]:
    if(len(word) == 0):
        return []
    for syllable in toki_pona_syllables:
        if(word.startswith(syllable)):
            following_syllables = split_into_syllables(word[len(syllable):])
            if(following_syllables is None):
                return None
            return [ syllable.upper(), ] + following_syllables
    return None

# this is very slow
def get_tokens(word_or_symbol: str) -> list:
    if(word_or_symbol in nimi_ale):
        return [ language_tokens.index(word_or_symbol), ], []
    if(word_or_symbol.isalpha()):
        syllables = split_into_syllables(word_or_symbol)
        if(syllables is not None):
            return [ language_tokens.index(syllable) for syllable in syllables ], []
    tokens = []
    unknown_tokens = []
    for letter in word_or_symbol:
        try:
            token = language_tokens[token_single_letters_start_id:].index(letter)
            token += token_letters_start_id
        except ValueError:
            unknown_tokens.append(letter)
            token = unknown_token
        tokens.append(token)
    return tokens, unknown_tokens

def tokenize_document(document: str) -> list:
    words_and_symbols = prepare_document(document)
    unknown_tokens = []
    tokens = []
    for word_or_symbol in words_and_symbols:
        new_tokens, new_unknown_tokens = get_tokens(word_or_symbol)
        tokens += new_tokens
        unknown_tokens += new_unknown_tokens
    return tokens, unknown_tokens

def reconnect_tokens(token_ids, decoded_tokens):
    document_data = []
    for token_id, decoded_token in zip(token_ids, decoded_tokens):
        token_data = {
            'token_id': token_id,
            'text': decoded_token,
            'is_syllable': check_if_token_is_syllable(token_id),
            'is_nimi': check_if_token_is_nimi(token_id),
            'is_punctuation': check_if_token_is_punctuation(token_id),
            'is_letter': check_if_token_is_letter(token_id),
            'is_digit': decoded_token in '0123456789',
        }
        if(token_data['is_syllable']):
            token_data['text'] = token_data['text'].upper()
        if(token_data['is_punctuation']):
            token_data['is_start'] = check_if_start_type_punctuation(token_data['text'])
            token_data['is_end'] = check_if_is_end_type_punctuation(token_data['text'])
            token_data['is_default'] = (not token_data['is_start']) and (not token_data['is_end'])
        document_data.append(token_data)
    for token_i, token_data in enumerate(document_data):
        if(token_i == 0):
            token_data['previous'] = None
        else:
            token_data['previous'] = document_data[token_i - 1]
        #if(token_i == len(document_data) - 1):
        #    token_data['next'] = None
        #else:
        #    token_data['next'] = document_data[token_i + 1]

    document = ''
    for token_data in document_data:
        previous_token = token_data['previous']
        if(previous_token is not None):
            #if((token_data['text'] in '0123456789') and (previous_token['text'] in '.,')):
            #    # special case for digit point & comma
            #    pass
            if(token_data['is_nimi']):
                if(not ((previous_token['is_punctuation']) and (previous_token['is_start']))):
                    document += ' '
            elif(token_data['is_syllable']):
                if(not ((previous_token['is_punctuation']) and (previous_token['is_start']))):
                    if(previous_token['is_syllable']):
                        document += '-'
                    else:
                        document += ' '
            elif(token_data['is_punctuation']):
                if(not token_data['is_end']):
                    document += ' '
            elif(token_data['is_letter']):
                if(previous_token['is_letter'] or (previous_token['is_punctuation'] and previous_token['is_end'])):
                    pass
                else:
                    document += ' '
            elif(token_data['is_digit']):
                if(previous_token['is_digit'] or (previous_token['is_punctuation'] and previous_token['is_end'])):
                    pass
                else:
                    document += ' '
            else:
                document += ' '
        document += token_data['text']
    return document

def decode_document(token_ids: list[int]) -> str:
    decoded_tokens = []
    for token_id in token_ids:
        if(token_id < len(language_tokens)):
            decoded_tokens.append(language_tokens[token_id])
        else:
            decoded_tokens.append(unknown_token)
    document = reconnect_tokens(token_ids, decoded_tokens)
    return document


