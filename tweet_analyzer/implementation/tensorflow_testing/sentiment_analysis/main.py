import numpy as np
import tensorflow as tf
from os import listdir
from os.path import isfile, join
import re

wordsList = []
with open('wordslist.txt', 'r') as file:
  wordsList = file.read().splitlines()
  print('loaded wordslist')

wordVectors = np.load('wordslist.npy')
print ('Loaded the word vectors!')

positiveFiles = ['./pos/' + f for f in listdir('./pos/') if isfile(join('./pos/', f))]
negativeFiles = ['./neg/' + f for f in listdir('./neg/') if isfile(join('./neg/', f))]
numWords = []
for pf in positiveFiles:
  with open(pf, "r", encoding='utf-8') as f:
    line=f.readline()
    counter = len(line.split())
    numWords.append(counter)       
print('Positive files finished')

for nf in negativeFiles:
  with open(nf, "r", encoding='utf-8') as f:
    line=f.readline()
    counter = len(line.split())
    numWords.append(counter)  
print('Negative files finished')

numFiles = len(numWords)

maxSeqLength = 250
strip_special_chars = re.compile("[^A-Za-z0-9 ]+")