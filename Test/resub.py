import re

pattern = re.compile('say')
s = 'i say, hello world!'

print(re.sub(pattern, 'pay', s))
