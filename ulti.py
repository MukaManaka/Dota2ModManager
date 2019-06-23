import zipfile
import hashlib
import shutil
import os 
import re

mod_dirnames = ['materials','models','panorama','particles','resource','soundevents','sounds']

error_index = 0 # 错误的个数

# 非英文检测
def unEngDetect(src, drt):
    pass


def find_ver(name):
    rule = r'V(\d+\.\d+)'
    st = re.findall(rule, name)[0]
    return st
    

# 解压文件
def zipextra(zipfilePath, rootDir = r'.\temp'):
    with zipfile.ZipFile(zipfilePath,'r') as file_zip:
        for file in file_zip.namelist():
            file_zip.extract(file, rootDir)
            # print(file)


def movedir(src, drt, replpath):
    for dirpath, dirnames, filenames in os.walk(src):
        for filepath in filenames:
            pathname = os.path.join(dirpath, filepath)
            # print('root',pathname)
            drt_path = os.path.dirname(pathname.replace(replpath, drt))
            if not os.path.exists(drt_path): # 如果路径不存在 创建路径
                os.makedirs(drt_path)
            try:
                shutil.move(pathname, drt_path)
            except Exception as e:
                print(e)



def extractMod(zipfilePath, rootDir = r'.\temp'):
    zipextra(zipfilePath)
    for dirpath, dirnames, filenames in os.walk(rootDir):
        for dirname in dirnames:
            for mod_dir in mod_dirnames:
                if mod_dir == dirname: # 找到文件
                    pathname = os.path.join(dirpath, dirname)
                    # 移动文件
                    movedir(pathname, r'.\Resource\Release', dirpath)
                    print(f'找到文件 {pathname}')
    # 删除 temp
    shutil.rmtree(rootDir)




def calcMD5(filepath):
    md5obj = hashlib.md5()
    with open(filepath,'rb') as file:
        chunk = 0
        while chunk != b'':
            # read only 1024 bytes at a time
            chunk = file.read(1024)
            md5obj.update(chunk)    
    hash = md5obj.hexdigest()
    #print(hash)
    return hash






if __name__ == '__main__':
    # extractMod('.\\Resource\\ZIP\\Akemi homura replaced queen of pain V1.01.zip')
    zipextra('.\\Resource\\ZIP\\Akemi homura replaced queen of pain V1.01.zip')
    pass
