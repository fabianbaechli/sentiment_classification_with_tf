import io
file = io.open('train.csv','r', encoding='utf-8')
lines = file.read()
count_positive = 0
count_negative = 0

for line in lines.splitlines():
  sentiment = line.split(",")[1]
  text = line.split(",", 2)[2]
  path = ""
  if (sentiment == "1"):
    count_positive+=1
    path = './pos/'+str(count_positive)+'.txt'
  elif (sentiment == "0"):
    count_negative+=1
    path = './neg/'+str(count_positive)+'.txt'
  else:
    print(sentiment)
    print("INPUT FAILURE")
    break
  positive_file_to_write = open(path, "w")
  positive_file_to_write.write(text)
  positive_file_to_write.close()