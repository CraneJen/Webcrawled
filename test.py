import os
# os.mkdir('/home/cj/test')
BADE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(os.getcwd())
print(os.path.dirname(os.path.abspath('__file__')))
print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
File_Dir = os.path.join(BADE_DIR, 'Python3')
if not os.path.exists(File_Dir):
    os.mkdir(File_Dir)
