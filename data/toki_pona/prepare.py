"""
Prepare the toki pona dataset with custom toki pona Tokenizer.
Will save train.bin, val.bin containing the ids, and meta.pkl containing the
encoder and decoder and some other related info.
"""
import os
import pickle
import numpy as np
import sys

sys.path.append('.')

# expect the input.txt file to be ready
input_file_path = os.path.join(os.path.dirname(__file__), 'input.txt')

with open(input_file_path, 'r') as f:
    data = f.readlines()

print(f"length of dataset in documents: {len(data):,}")


from tokipona.tokipona_tokenizer import tokenize_document, check_if_token_is_nimi

characters_to_remove = '"\'*\u200e' # strict cleanup
tokenized_documents = [
                        tokenize_document(doc.strip(), characters_to_remove=characters_to_remove)[0]
                        for doc in data
                      ]
# drop documents that don't contain pure toki pona tokens
tokenized_documents = [
                        doc
                        for doc in tokenized_documents
                        if(any([ check_if_token_is_nimi(t) for t in doc ]))
                      ]
print(f'nb documents after filtering: {len(tokenized_documents):,}')

tokenized_data = [ token for doc in tokenized_documents for token in doc ]


# create the train and test splits
n = len(tokenized_data)
print(f'total nb tokens: {n:,}')
train_data = tokenized_data[:int(n*0.9)]
val_data = tokenized_data[int(n*0.9):]

# encode both to integers
print(f"train has {len(train_data):,} tokens")
print(f"val has {len(val_data):,} tokens")

# export to bin files
train_ids = np.array(train_data, dtype=np.uint16)
val_ids = np.array(val_data, dtype=np.uint16)
train_ids.tofile(os.path.join(os.path.dirname(__file__), 'train.bin'))
val_ids.tofile(os.path.join(os.path.dirname(__file__), 'val.bin'))

# save the meta information as well, to help us encode/decode later
meta = {
    'vocab_size': 512, # len(tokipona_tokenizer.language_tokens) == 414
    #'itos': itos,
    #'stoi': stoi,
}
with open(os.path.join(os.path.dirname(__file__), 'meta.pkl'), 'wb') as f:
    pickle.dump(meta, f)
#
