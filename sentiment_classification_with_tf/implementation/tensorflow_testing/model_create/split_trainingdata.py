import io
file = io.open('train_new.csv','r', encoding='utf-8-sig')
lines = file.read()
count_positive = 0
count_negative = 0

for line in lines.splitlines():
  sentiment = line.split(",")[0]
  text = line.split(",", 2)[1]
  path = ""
  if (int(sentiment) == 4):
    count_positive+=1
    path = './pos/'+str(count_positive)+'.txt'
  elif (int(sentiment) == 0):
    count_negative+=1
    path = './neg/'+str(count_negative)+'.txt'
  else:
    print(sentiment.decode('utf8'))
    print("INPUT FAILURE")
    break
  positive_file_to_write = open(path, "w")
  positive_file_to_write.write(text.encode('utf-8'))
  positive_file_to_write.close()