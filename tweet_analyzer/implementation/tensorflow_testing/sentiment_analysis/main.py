import numpy as np
import tensorflow as tf
from os import listdir
from os.path import isfile, join
import re
from random import randint
import datetime

wordsList = []
with open('wordslist.txt', 'r') as file:
  wordsList = file.read().splitlines()
  print('loaded wordslist')

wordVectors = np.load('wordslist.npy')
print ('Loaded the word vectors!')

maxSeqLength = 10 #Maximum length of sentence
numDimensions = 300 #Dimensions for each word vector
firstSentence = np.zeros((maxSeqLength), dtype='int32')
firstSentence[0] = wordsList.index("i")
firstSentence[1] = wordsList.index("thought")
firstSentence[2] = wordsList.index("the")
firstSentence[3] = wordsList.index("movie")
firstSentence[4] = wordsList.index("was")
firstSentence[5] = wordsList.index("incredible")
firstSentence[6] = wordsList.index("and")
firstSentence[7] = wordsList.index("inspiring")
#firstSentence[8] and firstSentence[9] are going to be 0

with tf.Session() as sess:
    print(tf.nn.embedding_lookup(wordVectors,firstSentence).eval().shape)

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
def cleanSentences(string):
  string = string.lower().replace("<br />", " ")
  return re.sub(strip_special_chars, "", string.lower())

ids = np.load('idsMatrix.npy')
print('Loaded id\'s matrix')

def getTrainBatch():
    labels = []
    arr = np.zeros([batchSize, maxSeqLength])
    for i in range(batchSize):
        if (i % 2 == 0): 
            num = randint(1,11499)
            labels.append([1,0])
        else:
            num = randint(13499,24999)
            labels.append([0,1])
        arr[i] = ids[num-1:num]
    return arr, labels

def getTestBatch():
    labels = []
    arr = np.zeros([batchSize, maxSeqLength])
    for i in range(batchSize):
        num = randint(11499,13499)
        if (num <= 12499):
            labels.append([1,0])
        else:
            labels.append([0,1])
        arr[i] = ids[num-1:num]
    return arr, labels

batchSize = 24
lstmUnits = 64
numClasses = 2
iterations = 100000

tf.reset_default_graph()
labels = tf.placeholder(tf.float32, [batchSize, numClasses])
input_data = tf.placeholder(tf.int32, [batchSize, maxSeqLength])
data = tf.Variable(tf.zeros([batchSize, maxSeqLength, numDimensions]),dtype=tf.float32)
data = tf.nn.embedding_lookup(wordVectors,input_data)
lstmCell = tf.contrib.rnn.BasicLSTMCell(lstmUnits)
lstmCell = tf.contrib.rnn.DropoutWrapper(cell=lstmCell, output_keep_prob=0.75)
value, _ = tf.nn.dynamic_rnn(lstmCell, tf.cast(data, tf.float32), dtype=tf.float32)
weight = tf.Variable(tf.truncated_normal([lstmUnits, numClasses]))
bias = tf.Variable(tf.constant(0.1, shape=[numClasses]))
value = tf.transpose(value, [1, 0, 2])
last = tf.gather(value, int(value.get_shape()[0]) - 1)
prediction = (tf.matmul(last, weight) + bias)
correctPred = tf.equal(tf.argmax(prediction,1), tf.argmax(labels,1))
accuracy = tf.reduce_mean(tf.cast(correctPred, tf.float32))
loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=prediction, labels=labels))
optimizer = tf.train.AdamOptimizer().minimize(loss)
tf.summary.scalar('Loss', loss)
tf.summary.scalar('Accuracy', accuracy)
merged = tf.summary.merge_all()
logdir = "tensorboard/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + "/"
writer = tf.summary.FileWriter(logdir, sess.graph)
print('model created')

sess = tf.InteractiveSession()
saver = tf.train.Saver()
sess.run(tf.global_variables_initializer())

for i in range(iterations):
  #Next Batch of reviews
  nextBatch, nextBatchLabels = getTrainBatch();
  sess.run(optimizer, {input_data: nextBatch, labels: nextBatchLabels})

    #Write summary to Tensorboard
  if (i % 50 == 0):
    summary = sess.run(merged, {input_data: nextBatch, labels: nextBatchLabels})
    writer.add_summary(summary, i)

  #Save the network every 10,000 training iterations
  if (i % 10000 == 0 and i != 0):
    save_path = saver.save(sess, "models/pretrained_lstm.ckpt", global_step=i)
    print("saved to %s" % save_path)
writer.close()