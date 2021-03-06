import numpy as	np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('input', help='Single embedding file')
parser.add_argument('output', help='Output basename without extension')
args = parser.parse_args()

embeddings_file = args.output + '.npy'
vocabulary_file = args.output + '.txt'
words = []
vectors = []

with open(args.input, 'rb') as f:
  for line in f:
    fields = line.split()
    word = fields[0].decode('utf-8')
    vector = np.fromiter((float(x) for x in fields[1:]), dtype=np.float)
    words.append(word)
    vectors.append(vector)

matrix = np.array(vectors)
np.save(embeddings_file, matrix)
text = '\n'.join(words)
with open(vocabulary_file, 'wb') as f:
    f.write(text.encode('utf-8'))