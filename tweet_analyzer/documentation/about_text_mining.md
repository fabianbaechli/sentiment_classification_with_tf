# About text mining
## About this file
The purpose of this file is to get a better understanding about the many different aspects of text analysis.
The goal is to apply the newly gained knowledge on some tweets which the twitter bot gathers to hopefully 
arrive at interesting insights about what people like to read from different political people.

## Text mining
### What is text mining
Text mining is the use of algorithms to derive high-quality information of a given set of texts.
A term which also get's thrown around much in this field is the so called data mining.
The difference between data mining and text mining is, that __data mining is designed to deal with structured text like XML while text mining's goal is to deal with unstructured text (like tweets)__
There are many different forms of text mining, but what is very interesting for this particular project is
the so called [concept mining](https://en.wikipedia.org/wiki/Concept_mining).

### What is concept mining
Much of the following text is abstracted from 
[this](https://pdfs.semanticscholar.org/eb5c/8ae3000a76ec678bd0178fedf4e9b402708c.pdf) document.

Concept mining is the mapping of words to concepts. It pays attention to the "meaning" of a
text rather than just statistically analyzing it's words.
The whole process relies heavily on artificial intelligence

> The concept-based model can effectively discriminate between non-important terms with
> respect to sentence semantics and terms which hold the concepts that represent the
> sentence meaning.

This means, I think (I'm rather new to this topic and this quote is from a research paper),
that just because a word get's thrown around a lot in a sentence, doesn't necessarily mean, that
this word represents the "meaning" of a sentence the best.

## High dimensional space and vector space model
High dimensional space is used to represent a dataset with many different attributes. Every attribute
maps to a dimension. In text analysis this would mean that you can represent a text in high dimensional
space by assigning a dimension to every word (term vector). This is where the term 'high' in high
dimensional springs from. After you've mapped all the terms in the document in a high dimensional space,
you can start doing all kinds of fun things with it, for example comparing two data sets and determine
their similarity by  mapping the whole document to a vector (document vector). The mapping of words
to a vector is called 'word embedding'. Naturally you'd want to cluster words with similar meaning
close to each other.

Mapping a document in high dimensional space could be done like this: represent every document by a
vector _dtf = (tf1, tf2, , tfn)_, where _tfi_ is the frequency of the _ith_ term.

### Word2Vec
Word2Vec is a model which maps words to vectors (word embedding). It is context based. Words with
similar context will be placed close to each other. There is a Node.JS implementation of this google
library [here](https://github.com/Planeshifter/node-word2vec). The output of the Word2Vec model is called
an embedding matrix. This Vector matrix can then be used as an input for a Deep Learning based approach
to a Natural Language Processing task.

## RNN
A recurrent neuronal network is different from a neuronal network. Natural language processing is very
temporal. That means, that the meaning of a word, which comes later in the sentence than the current
position, may greatly influence everything that came before. If you take the sentence 'I love how you
cheated on me you loser', from a NLP perspective, the sentence is very positive at first but then the
meaning changes completely.

A recurrent neuronal network takes this temporal nature of Natural Language Processing into account.
It achieves this by:
- Associating every word in a sentence with a specific time step
- Associating a hidden state vector with every time step (ht)
  - The hidden state vector seeks to summarize information from previous time steps
  - The classic xt vector summarizes information of just one term
- Implementing a hidden state function which sums the current word vector and the hidden state vector
  from the previous term.

## Stop words
Stop words are words which are not believed to add any significance to a sentence. They are mostly common
words like 'the', 'and', 'a'. Most of the times, they are removed before analyzing a dataset.

## Stemming algorithm
Stemming algorithms transform any word into it's base form. One of the most popular stemming algorithm is
called Porter stemmer.

## Text clustering
Document clustering is an _unsupervised_ task. This means that in the training phase, no correct output
has to be given (in this case, the correct output would be the correct cluster, to which the document should
be mapped to).

The cluster in this case is a collection of documents with a high level of similarity (high in-cluster 
similarity). The best way of clustering documents is the _agglomerative hierarchical clustering_.

### IDF
The inverse document frequency calculates the meaningfulness of a term for the clustering. If a highly
uncommon word is used in two different documents, these two documents have a higher probability of being
similar than two documents which both have the word 'and' in them. The IDF is calculated like this:

<a href="https://www.codecogs.com/eqnedit.php?latex=IDF_{t}&space;=&space;log\left(&space;\frac{N_{D}&space;}{f_{t}}&space;\right)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?IDF_{t}&space;=&space;log\left(&space;\frac{N_{D}&space;}{f_{t}}&space;\right)" title="IDF_{t} = log\left( \frac{N_{D} }{f_{t}} \right)" /></a>

Where <a href="https://www.codecogs.com/eqnedit.php?latex=N_{d}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?N_{d}" title="N_{d}" /></a> is the number of documents and <a href="https://www.codecogs.com/eqnedit.php?latex=f_{t}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?f_{t}" title="f_{t}" /></a> the number of documents which contain
the term <a href="https://www.codecogs.com/eqnedit.php?latex=t" target="_blank"><img src="https://latex.codecogs.com/gif.latex?t" title="t" /></a>.

## Terms which are unclear to me
- Term weighting
- Sliding window
