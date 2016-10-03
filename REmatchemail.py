import re
email = input("Inpu Email: ")
pattern = re.compile(r'(\w+)@(\w+).(\w+)', re.S)
content = re.findall(pattern, email)
print(content)
if re.match(pattern, email):
    print('match')
else:
    print('sorry')
