import glob
import errno

positive_files = './pos/*.txt'
negative_files = './neg/*.txt'

files = glob.glob(negative_files)
for name in files:
  try:
    with open(name, "r+") as f:
      words = f.read().split()

      a = [word for word in words if '@' not in word]
      a = [word for word in words if 'http' not in word]

      for i, word in enumerate(a):
        a[i] = a[i].replace("&amp;", "&")
        a[i] = a[i].replace("&lt;", "<")
        a[i] = a[i].replace("&gt;", ">")
        a[i] = a[i].replace("&quot;", '"')

      output = ' '.join(a)
      f.seek(0)
      f.write(output)
      f.truncate()
      f.close()
  except IOError as exc:
    raise