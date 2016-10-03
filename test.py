import re
text = '''konghang

konghang'''
print(text)

remove_blankline = re.compile("\n+")

x = re.sub(remove_blankline, '\n', text)
print(x)
