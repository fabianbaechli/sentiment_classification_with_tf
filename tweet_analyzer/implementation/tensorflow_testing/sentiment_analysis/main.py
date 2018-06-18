import numpy as np
import tensorflow as tf
from os import listdir
from os.path import isfile, join

wordsList = []
with open('wordslist.txt', 'r') as file:
  wordsList = file.read().splitlines()
  print('loaded wordslist')

wordVectors = np.load('wordslist.npy')
print ('Loaded the word vectors!')

maxSeqLength = 10
numDimensions = 300
firstSentence = np.zeros((maxSeqLength), dtype='int32')
firstSentence[0] = wordsList.index("i")
firstSentence[1] = wordsList.index("thought")
firstSentence[2] = wordsList.index("the")
firstSentence[3] = wordsList.index("movie")
firstSentence[4] = wordsList.index("was")
firstSentence[5] = wordsList.index("incredible")
firstSentence[6] = wordsList.index("and")
firstSentence[7] = wordsList.index("inspiring")

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
print('The total number of files is', numFiles)
print('The total number of words in the files is', sum(numWords))
print('The average number of words in the files is', sum(numWords)/len(numWords))