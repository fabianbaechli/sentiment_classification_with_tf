# Readme
## Was
Ich habe eine Recurrent Neuronal Network implementiert, welches auf Sentiment Classification trainiert ist.
Ich las zu diesem Zweck verschiedenste Theorie-Resourcen, um mein Verständnis zu dem Thema natural language processing (NLP) zu verbessern.
Die Erkentnisse aus dieser Theorie-Recherche hielt ich im File sentiment_classification_with_tf/sentiment_classification_with_tf/documentation/about_text_mining.md fest.

## Was ist sentiment classification?
Sentiment classification ist ein Untergebiet der natural language processing.

Natural language processing ist der Versuch, Computern das Prozessieren von Menschlichen Sprachen beizubringen.
Mit dem Aufkommen von Neuronalen Netzen erlebte auch NLP eine Art Renaissance.
Für NLP wurde eine spezielle Art von Neuronalen Netzen implementiert, welche den in jeder Sprache vorhandenen "flüchtigen" Aspekt berücksichtigt.
Mit flüchtig ist hierbei gemeint, dass ein Wort, welches spät im Satz kommt, die vorhergehende Bedeutung grundlegend ändern kann.
Diese neuronalen Netzwerke werden "recurrent neuronal network" (RNN) genannt.

Sentiment classification ist das Einordnen eines Textinputs auf eine "Empfindung". 
In meinem Fall habe ich als mögliche classifications "positiv" und "negativ" gewählt.
Das heisst, mein RNN teilt Text Texte in positiv und negativ ein.

## Vorgehen
1. Herunterladen eines Word-Vector Files (https://nlp.stanford.edu/projects/glove/)
2. Splitten der Wörter und Vektoren in separate Files
3. Erstellen einer ID-Matrix
4. Herunterladen von Training Daten (https://www.kaggle.com/utathya/imdb-review-dataset)
5. Training
