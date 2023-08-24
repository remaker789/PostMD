#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''This script is to process the files generated from log or dump files.
@Author  :   Shusong Zhang
@Email   :   sszhang@mail.nwpu.edu.cn, zhangshusong789@gmail.com
@File    :   FileOperation.py
@Time    :   2023/05/05 10:46:11
'''

import re, os
from pathlib import Path

# class Dir:
#     def __init__(self, dir):
#         self.dir = dir
#         self.Path = Path(self.dir)
#         if not self.Path.is_dir():
#             raise ValueError("The keyword dir must be a directory")
    
#     # @staticmethod             
#     # def dig_next_depth(Path, pattern):
#     #     pattern = '*/'+pattern # bug: 不知道*/对应linux系统是否适用。
#     #     return Path.glob(pattern) # 返回dir下面所有files
                
        
#     def get_path(self, 
#                  pattern:str = None, 
#                  mode = 'full', 
#                  rex=False, 
#                  recursive_hier='all',
#                  out = "str") -> list :
#         """get filepaths according to pattern

#         Args:
#             pattern (str, optional): pattern used to math the filename in Dir. Defaults to None.
#             mode (str, optional): the match criterion of pattern. Defaults to 'full'. 
#                                   full match if mode=='all';
#                                   match prefix if mode=='prefix';
#                                   match suffix if mode=="suffix';
#                                   fnmatch mode if mode=="custom". see https://docs.python.org/zh-cn/3/library/fnmatch.html#module-fnmatch
#             re (bool, optional): use RegularExpression if re is True, else fnmatch mode. Defaults to False.
#             recursive_hier (str, optional): The recursive hierarchy to dig. Defaults to 'all'. 
#                                             all depth will be searched if recursive_hier='all';
#                                             the specified depth will be searched if recusive_hier is int (the base depth is 0);
                                            
                                            
#             out (str, optional): _description_. Defaults to "str".

#         Raises:
#             ValueError: _description_
#             ValueError: _description_
#             ValueError: _description_

#         Returns:
#             list: _description_
#         """        
#         if pattern is None:
#             raise ValueError("A pattern is desired to get the filepaths")
        
#         # fnmatch if re is False; 
#         if not rex:
#             if mode == "full":       # full match
#                 pattern = pattern
#             elif mode == "prefix":   # match prefix
#                 pattern = pattern+"*"
#             elif mode == "suffix":   # match suffix
#                 pattern = '*'+pattern    
#             elif mode == "custom":   # custom pattern
#                 pattern = pattern
#             else:
#                 raise ValueError("input mode is not supported!")
#         else: # re的还没有做。。。
#             mode == None
#             print("RegularExpression is used!")
            
#         self.short_pattern = {"pattern": pattern, "re": rex}
#         self.re = rex
        
#         if recursive_hier == 'all':
#             pattern = '**/' + pattern # 递归所有目录
#             _paths = self.Path.glob(pattern) # 返回dir下面所有files

#         elif isinstance(recursive_hier, int):
#             pattern = recursive_hier*'*/'+pattern # bug: 不知道*/对应linux系统是否适用。
#             _paths = self.Path.glob(pattern) # 返回dir下面所有files

#         elif isinstance(recursive_hier, str): # 目前最大允许递归到第9层目录
#             _paths = []
#             if re.match('\d\*\d',recursive_hier): # 从first_depth检索到end_depth
#                 first_depth = int(recursive_hier[0])
#                 end_depth = int(recursive_hier[-1])
#                 for depth in range(first_depth, end_depth+1):
#                     depth_pattern = depth*'*/'+pattern
#                     _paths += self.Path.glob(depth_pattern)
                    
#             elif re.match('\*\d', recursive_hier): # 从第0层检索到end_depth
#                 first_depth = 0
#                 end_depth = int(recursive_hier[-1])
#                 for depth in range(first_depth, end_depth+1):
#                     depth_pattern = depth*'*/'+pattern
#                     _paths += self.Path.glob(depth_pattern)
#             elif re.match('\d\*',recursive_hier): # 从first_depth检索到最后
#                 first_depth = int(recursive_hier[0])
#                 end_depth = 100 # 将最大层设置成100，只要没超过100层，应该就可以吧。。。
#                 for depth in range(first_depth, end_depth):
#                     depth_pattern = depth*'*/'+pattern
#                     _paths += self.Path.glob(depth_pattern)
#             elif re.match('\d+', recursive_hier): # 只检索第n层
#                 depth_pattern = int(recursive_hier)*'*/'+pattern
#                 _paths += self.Path.glob(depth_pattern) # 返回dir下面所有files
#             else:
#                 raise ValueError("the fommat of input string is not supported")
            
#         # elif 如果recursive_hier是可迭代对象，对里面每一个数值进行迭代
        
#         else:
#             raise ValueError("Input recursive_hier is not supported.")
        
        
        
        
#         # 选出files
#         if out == 'str':
#             files = [str(_path) for _path in _paths if _path.is_file() ]
#             # dirs = [str(_path) for _path in _paths if _path.is_dir() ]
#         else: 
#             files = [_path for _path in _paths if _path.is_file() ]
#             # dirs = [_path for _path in _paths if _path.is_dir() ]
#         return files
    

class LogFile:
    def __init__(self) -> None:
        self.lammps_version=None
        self.path=None
        
        
        
    def set_path(self, path=None):
        self.path = path
        self.judge_path()
        print(f"You are processing the file: '{self.path}'")

    def judge_path(self):
        """judge whether the path of object is accessable.
        """
        if (self.path is None):  # 判断path或者self.path是否为空
            raise ValueError("path can not be empty!")
        elif not Path(self.path).is_file():
            raise ValueError(f"'{self.path}' is not a file!")    
        
        
    def get_lammps_version(self):
        """get the version of lammps used.
        """     
        self.judge_path()   
        with open(self.path, encoding='utf-8') as f:
            self.lammps_version = f.readline()
            print(f"The version of LAMMPS: {self.lammps_version}")
    

    def extract_thermodata(self,*, block_start = "Per MPI rank", block_end = "Loop time of", path=None, output="extracted-log.lammps"):        
        """extract the thermo data from log file

        Args:
            block_start (str, optional): the start string of the block of thermo data. Defaults to "Per MPI rank".
            block_end (str, optional): the end string of the block of thermo data. Defaults to "Loop time of".
            paths (str, optional): the path to the log file. Default to None, which means use self.path
            
        Notes: 
        1. block_start='Step' and block_end="Loop time of" usually works for most case in LAMMPS (29 Oct 2020). 
           If the block changed with lammps, you can change it with keyword arguments.
        2. If the block of thermo data contain the WARNING, for example, sub-domain..., this function can not omit the WARNING.
           Maybe a good choice is to add a judgement depend on the percent of characters exceeding 50% with Regular Expression!
        """
        
        path = path if path else self.path
        self.set_path(path)
        output_path = os.path.join(os.path.dirname(path), output)
        with open(self.path, encoding='utf-8') as logfile:
            lines_block_start=[] # the list storing the line number of block start
            lines_block_end=[]   # the list storing the line number of block end
            num_block=0 # count the number of blocks
            line_block_start=0
            line_block_end=0
            write=False
            text=""
            for i, line in enumerate(logfile.readlines()):
                # todo 看看能不能再精简代码结构。。。现在还是有点麻烦
                if line.startswith(block_end):
                    write=False
                    line_block_end=i-1
                    lines_block_end.append(line_block_end+1) # the line in python starts from 0

                if not line.startswith(block_start):
                    if  i == line_block_start and len(lines_block_end) != 0: # avoid output the header second time.
                        continue
                    
                    if write:
                        text=text+line
                    else:
                        continue
                else:
                    write=True
                    line_block_start=i+1
                    lines_block_start.append(line_block_start+1) # the line in python starts from 0

                
            output_path= os.path.join(os.path.dirname(self.path), output)
            with open(output_path, 'w+') as output:
                output.write(text)
                
        print(f"The line number of block start: {lines_block_start}")   
        print(f"The line number of block end:   {lines_block_end}")   
        print("---------- Extracting logfile succeed! -----------")
        print(f"The extracted file: '{output_path}'")
