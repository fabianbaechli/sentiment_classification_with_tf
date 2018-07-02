import numpy as np
import tensorflow as tf
import re
import socket

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

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('localhost', 9090))
serversocket.listen(5)

while True:
    connection, address = serversocket.accept()
    while True:
        buf = connection.recv(64)
        if len(buf) > 0:
          input = buf.decode()
          print(type(input))
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