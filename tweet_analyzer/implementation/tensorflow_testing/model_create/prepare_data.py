import glob
import errno
from cucco import Cucco
cucco = Cucco()

positive_files = './pos/*.txt'
negative_files = './neg/*.txt'
normalizations = [
  'remove_accent_marks',
  'remove_extra_whitespaces',
  'remove_stop_words',
  'replace_charachters',
  'replace_emails',
  'replace_emojis',
  'replace_hyphens',
  'replace_punctuation',
  'replace_symbols',
  'replace_urls'
]
iterations = 0
files = glob.glob(negative_files)
for name in files:
  with open(name, "r+") as f:
    text = f.read().decode('utf8')
    words = text.split(" ")

    a = [word for word in words if '@'.decode('utf-8') not in word]

    for i, word in enumerate(a):
      a[i] = a[i].replace("&amp;", "&")
      a[i] = a[i].replace("&lt;", "<")
      a[i] = a[i].replace("&gt;", ">")
      a[i] = a[i].replace("&quot;", '"')

    output = ' '.join(a)

    normalized_out = cucco.normalize(output, normalizations)
    print(normalized_out)
    f.seek(0)
    f.write(normalized_out.lower().encode('utf-8'))
    f.truncate()
    f.close()