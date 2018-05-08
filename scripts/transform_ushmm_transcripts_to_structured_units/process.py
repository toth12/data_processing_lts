import pdb
import re
text=open('input.txt').read()
text=' '.join(text.split())
text=re.split('Q:|A:',text)
pdb.set_trace()