import glob
import errno
from cucco import Cucco
cucco = Cucco()

positive_files = './pos/*.txt'
negative_files = './neg/*.txt'
normalizations = [
  'remove_extra_white_spaces',
  'replace_punctuation',
  'replace_symbols',
  'remove_stop_words'
]
iterations = 0
files = glob.glob(negative_files)
for name in files:
  try:
    with open(name, "r+") as f:
      text = f.read().encode('utf8')
      words = text.split()

      a = [word for word in words if '@' not in word]
      a = [word for word in words if 'http' not in word]

      for i, word in enumerate(a):
        a[i] = a[i].replace("&amp;", "&")
        a[i] = a[i].replace("&lt;", "<")
        a[i] = a[i].replace("&gt;", ">")
        a[i] = a[i].replace("&quot;", '"')

      output = ' '.join(a)
      normalized_out = cucco.normalize(output, normalizations)
      f.seek(0)
      f.write(normalized_out.lower())
      f.truncate()
      f.close()
  except Exception as exc:
    print(str(exc))