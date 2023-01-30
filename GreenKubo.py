import numpy as np
from AveTime import *
from scipy.integrate import simpson, trapezoid


# 一般来说GreenKubo是对平衡态下某些参数的自相关函数进行时间上的积分。
class GreenKubo(AveTime):
    def __init__(self, path=None, timestep=1):
        super().__init__(path, timestep)
        self.acf=None
        self.t=None

    
    
    def read_file(self, names:list=None, num_line:int = 2, **kwargs)->pd.DataFrame:
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
        path = self.path
        # if path.endswith(('xls', 'xlsx')): #产生的数据基本上不可能是excel
        #     df = pd.read_excel(path, names =names, comment = "#", **kwargs) 
        # else:
        #     df = pd.read_csv(path, names =names, sep = '\s+', comment = "#", **kwargs)
        
        df = pd.read_csv(path, names =names, sep = '\s+', comment = "#", **kwargs)
        self.content = df
        return df
    
    
    # # after using fix ave/correlate ave running
    # def integrate(self, *, Nevery:int=None, Nrepeat:int=None, Nfreq:int=None, 
    #               overwrite:bool=True, col_time:int or str = 1, col_data:int or str=None):
    #     print('''The data must be genetated using "ave running" in fix ave/correlate commmand''')
        
    #     if overwrite:
    #         # ! 不确定fix ave/correlate中的names是第几行。
    #         df = self.read_file(self.path, names=None, num_line=2)
    #     else:
    #         pass     # todo: 不是overwrite的数据，只需要取最后一个block
        
    # 这里的integrate只是用来对acf进行积分
    def integrate_acf(self, acf=None, t=None, *, method="simpson"):
        # 我想建一个输出所有method的方法
        acf = acf if self.acf is None else self.acf
        t = t if self.t is None else self.t
        
        if acf is None:
            raise ValueError("Please input acf!!!")
        if acf is None:
            raise ValueError("Please input t!!!")
                
        if method == "simpson":
            _int = simpson(y=acf, x=t)
        elif method == "trap":
            _int = trapezoid(y=acf, x=t)
        else:
            raise ValueError(f"method '{method}' is not supported yet!")
        return _int
# 是否要创建一个File类？   
import statsmodels.api as sm        
test = GreenKubo(r"D:\OneDrive\Github\MyRepos\PostMD\data\friction.txt")
df = test.read_file(num_line=2)
acf = sm.tsa.stattools.acovf(df.iloc[:,3], nlag=2000)
inte = test.integrate_acf(acf, np.arange(1, len(acf)+1))
print(inte)
 
    