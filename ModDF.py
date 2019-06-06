import pandas as pd
from ulti import *
import shutil
import os 
import json


pd.set_option('display.max_columns',None) #a就是你要设置显示的最大列数参数
# pd.set_option('display.max_rows',b) #b就是你要设置显示的最大的行数参数
pd.set_option('display.width',None) #x就是你要设置的显示的宽度，防止轻易换行
# pd.set_option('display.height',y) #y就是你要设置的高度


class DotaModManager(object):
    """docstring for DotaModManager"""
    def __init__(self, arg = None):
        super(DotaModManager, self).__init__()
        self.arg = arg
        self.columns = ['name', 'version', 'using', 'decompression',' hash', 'path', 'state']
        self.reset_dataframe()
        # self.load_library()

    def __str__(self):
        return str(self.dataframe)

    def reset_dataframe(self):
        self.dataframe = pd.DataFrame(columns = self.columns)

    # 读取数据库信息json文件
    def load_library(self):
        self.dataframe = pd.read_json(r".\usr\lib.json")

    # 保存数据库信息json文件
    def save_library(self):
        self.dataframe.to_json(r".\usr\lib.json")

    # 读取配置文件
    def load_config(self):
        pass

    # 从资源文件夹找
    def auto_resource(self, extract = False): # 未完成
        with open('.\\usr\\modname.json', "r", encoding = 'utf-8') as f:
            modnames = json.load(f)


        rootDir = '.\\Resource\\Zip' 
        for filename in os.listdir(rootDir):
            pathname = os.path.join(rootDir, filename)
            if os.path.isfile(pathname): # 所有zip文件
                name = None
                ver = None
                for namekey in modnames.keys(): # 遍历所有Key
                    if namekey == filename: # 找到
                        name = modnames[namekey]
                        ver = find_ver(filename)
                self.add_resource(filename, name, extract = extract)




    def clear_resource(self):
        shutil.rmtree(r'.\Resource\Release')
        self.dataframe.iloc[:,3] = False
        self.save_library()
        os.makedirs(r'.\Resource\Release')


    # 添加资源文件
    def add_resource(self, path, name = None, ver = None, state = None, extract = False): # 未完成 
        true_path = '.\\Resource\\ZIP\\' + path

        if extract: # 是否解压
            extractMod(true_path)

        _name = name
        _version = ver
        _using = False
        _decompression = extract
        _hash = calcMD5(true_path)
        _path = true_path
        _state = state

        insertRow = pd.DataFrame([[_name, _version, _using, _decompression, _hash, _path, _state]], columns = self.columns)
        self.dataframe = self.dataframe.append(insertRow, ignore_index=True)


    # 由index解压目录
    def exrract_index(self, indexes):
        for index in indexes:
            path = self.dataframe.loc[index, 'path']
            extractMod(path)
            self.dataframe.loc[index, 'decompression'] = True

    def drop_resource(self, indexes):
        self.dataframe.drop(indexes, axis = 0, inplace = False) 




if __name__ == '__main__':
    dmm = DotaModManager()

    dmm.clear_resource()
    # dmm.add_resource('Akemi homura replaced queen of pain V1.01.zip', extract = True)
    # dmm.save_library()
    dmm.auto_resource(extract = True)
    dmm.save_library()
    print(dmm)