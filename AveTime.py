import numpy as np
import pandas as pd
from pathlib import Path
import re

class AveTime:
    def __init__(self, path=None, timestep = 1):  # timestep = 1fs
        self.timestep = timestep
        self.path = path
        self.judge_path()
        
        
    def set_path(self, path=None):
        self.path = path
        self.judge_path()
    
    

    def judge_path(self):
        """judge whether the path of object is accessable.
        """        
        if (self.path is None): # 判断path或者self.path是否为空
            raise ValueError("path can not be empty")
        elif not Path(self.path).is_file():
            raise ValueError(f"'{self.path}' is not a file")
        
            
    def get_names(self, num_line:int)->list: 
        """get the names used in dataframe when read files

        Args:
            num_line (int): the line including the column names of data

        Returns:
            list: a list of the column names of data
        """        
        with open(self.path) as f:
            for i, line in enumerate(f.readlines(),1):
                if i == num_line:
                    return re.split('\s+', line.strip())[1:]
            
            
    def read_file(self,path:str, names:list=None, num_line:int = 2, **kwargs)->pd.DataFrame:
        """read file and return DataFrame. 
            There are some default setting in read files:
            - comment="#" due to the nature of LAMMPS
            - sep="\s+" to match all space between data
            - **kwargs received parameters of read_csv and read_excel, depending on cases. 

        Args:
            path (str): path to the file
            names (list, optional): list of columns names of data. 
                                    Defaults to None, meaning using the content in num_line of file.
            num_line (int, optional): when names=None, the content in line=num_line
                                      will be used as the column names. Defaults to 2.

        Returns:
            pd.DataFrame: DataFrame object read from the file.
        """        
        names = names if names else self.get_names(num_line)
        # if path.endswith(('xls', 'xlsx')): #产生的数据基本上不可能是excel
        #     df = pd.read_excel(path, names =names, comment = "#", **kwargs) 
        # else:
        #     df = pd.read_csv(path, names =names, sep = '\s+', comment = "#", **kwargs)
        
        df = pd.read_csv(path, names =names, sep = '\s+', comment = "#", **kwargs)
        self.content = df
        return df



# path = r"D:\OneDrive\Github\MyRepos\PostMD\data\ave_time.dat"

# test = AveTime(path)
# print(test.get_names(2))
# df = test.read_file(path)
# print(df.head(5))