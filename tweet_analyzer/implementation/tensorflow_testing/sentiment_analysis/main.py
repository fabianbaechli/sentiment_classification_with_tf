import numpy as np
import tensorflow as tf
import re

numDimensions = 300
maxSeqLength = 250
batchSize = 24
lstmUnits = 64
numClasses = 2
iterations = 100000

wordsList = []
with open('wordslist.txt', 'r') as file:
  wordsList = file.read().splitlines()
  print('loaded wordslist')
wordsList = [word for word in wordsList] #Encode words as UTF-8
wordVectors = np.load('wordslist.npy')

tf.reset_default_graph()

labels = tf.placeholder(tf.float32, [batchSize, numClasses])
input_data = tf.placeholder(tf.int32, [batchSize, maxSeqLength])

data = tf.Variable(tf.zeros([batchSize, maxSeqLength, numDimensions]),dtype=tf.float32)
data = tf.nn.embedding_lookup(wordVectors,input_data)

lstmCell = tf.contrib.rnn.BasicLSTMCell(lstmUnits)
lstmCell = tf.contrib.rnn.DropoutWrapper(cell=lstmCell, output_keep_prob=0.25)
value, _ = tf.nn.dynamic_rnn(lstmCell, tf.cast(data, tf.float32), dtype=tf.float32)

weight = tf.Variable(tf.truncated_normal([lstmUnits, numClasses]))
bias = tf.Variable(tf.constant(0.1, shape=[numClasses]))
value = tf.transpose(value, [1, 0, 2])
last = tf.gather(value, int(value.get_shape()[0]) - 1)
prediction = (tf.matmul(last, weight) + bias)

correctPred = tf.equal(tf.argmax(prediction,1), tf.argmax(labels,1))
accuracy = tf.reduce_mean(tf.cast(correctPred, tf.float32))

sess = tf.InteractiveSession()
saver = tf.train.Saver()
saver.restore(sess, tf.train.latest_checkpoint('models'))

strip_special_chars = re.compile("[^A-Za-z0-9 ]+")

def cleanSentences(string):
  string = string.lower().replace("<br />", " ")
  return re.sub(strip_special_chars, "", string.lower())

def getSentenceMatrix(sentence):
    arr = np.zeros([batchSize, maxSeqLength])
    sentenceMatrix = np.zeros([batchSize,maxSeqLength], dtype='int32')
    cleanedSentence = cleanSentences(sentence)
    split = cleanedSentence.split()
    for indexCounter,word in enumerate(split):
        try:
            sentenceMatrix[0,indexCounter] = wordsList.index(word)
        except ValueError:
            sentenceMatrix[0,indexCounter] = 399999 #Vector for unkown words
    return sentenceMatrix

inputText = ["Just returning from the Great State of Minnesota where we had an incredible rally with 9,000 people, and at least 10,000 who could not get in - I will return! Congratulations to @PeteStauber who is loved and respected in Minnesota!", 
  "Thank you Duluth, Minnesota. Together, we are MAKING AMERICA GREAT AGAIN!", 
  "So sorry, people wanting to get into the already packed arena - I LOVE YOU ALL!",
  "Just landed in Duluth, Minnesota. Two events planned - looking forward to them and being with @PeteStauber and his wonderful family!",
  "Look what Fake ABC News put out. I guess they had it prepared from the 13 Angry Democrats leading the Witch Hunt! #StopTheBias",
  "Had a great meeting with the House GOP last night at the Capitol. They applauded and laughed loudly when I mentioned my experience with Mark Sanford. I have never been a fan of his!",
  "“FBI texts have revealed anti-Trump Bias.” @FoxNews  Big News, but the Fake News doesn’t want to cover. Total corruption - the Witch Hunt has turned out to be a scam! At some point soon the Mainstream Media will have to cover correctly, too big a story!",
  "It is hard to believe that the historic North Korea / Kim Jong Un summit was exactly one week ago. Truly amazing to see the lengths the left / the media will go through to change the narrative.",
  "It’s the Democrats fault, they won’t give us the votes needed to pass good immigration legislation. They want open borders, which breeds horrible crime. Republicans want security. But I am working on something - it never ends!",
  "The Fake News is not mentioning the safety and security of our Country when talking about illegal immigration. Our immigration laws are the weakest and worst anywhere in the world, and the Dems will do anything not to change them & to obstruct-want open borders which means crime!",
  "Earlier today, @FLOTUS Melania and I were honored to welcome King Felipe VI and Queen Letizia of Spain to the @WhiteHouse!",
  "Homeland Security @SecNielsen did a fabulous job yesterday at the press conference explaining security at the border and for our country, while at the same time recommending changes to obsolete & nasty laws, which force family separation. We want “heart” and security in America!",
  "I want to take a moment to address the current illegal immigration crisis on the Southern Border...it has been going on for many, many decades..."]

for input in inputText:
  matrix = getSentenceMatrix(input)
  predictedSentiment = sess.run(prediction, {input_data: matrix})[0]
  print ("positive: " + np.format_float_positional(predictedSentiment[0]) + " negative: " + np.format_float_positional(predictedSentiment[1]))
  if (predictedSentiment[0] > predictedSentiment[1]):
    print ("Positive Sentiment")
  elif (abs(predictedSentiment[0] - predictedSentiment[1]) <= 1):
    print ("Neutral sentiment")
  else:
    print ("Negative Sentiment" )
  print ("\n\n")