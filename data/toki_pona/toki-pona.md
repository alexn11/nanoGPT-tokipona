
- copy the toki pona texts file as `input.txt`, eg from tokenizer repo:
```cp outputs/data/toki-ale.txt ../nanoGPT/data/toki_pona/input.txt```

- prepare the data (tokenize the documents, train-eval split):
`python data/toki_pona/prepare.py`
- train the model
`python train.py config/train_toki_pona.py`
- generate some random texts:
`python sample.py --out_dir=out-toki-pona`