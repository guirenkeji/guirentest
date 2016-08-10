import os
import shutil
def del_files(path):
#    os.removedir('.svn')
    for root , dirs, files in os.walk(path):
        for dir in dirs:
            print dir
            if dir=='.svn':
#                  svn路径
                 svnpath = os.path.join(root,dir)
#                  文件删除
                 shutil.rmtree(svnpath)
            print dir
#  print ("Delete File: " + os.path.join(root, name))
# test
if __name__ == "__main__":
    path = './cfgicloud/workspace/'
    del_files(path)