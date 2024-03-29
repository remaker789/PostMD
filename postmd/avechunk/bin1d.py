import re
import pandas as pd
from ..system import MDFile
'''
This script is to deal with the data using comput chunk/atom and fix ave/chunk.
now I just right the Bin1d Class
- This script can only be used for constant chunk numbers. using a iter to save memory.
- For changed chunk numbers, I may used skip_rows..
'''

class Bin1d(MDFile):
    def __init__(self, path=None, timestep:float=1.0, dim:str=None, delta:float=None):
        """post-process the file generated from ``fix ave/chunk bin1d`` command.

        Args:
            path (str, optional): path to the file. Defaults to ``None``.
            timestep (float, optional): temperature you set in LAMMPS input file. Defaults to ``1.0`` [fs].            
            dim (str): the dimension of chunk: ``'x'``, ``'y'`` or ``'z'``.
            delta (float): the chunk size, in Angstrom.
        """
        super().__init__(path=path)
        self.timestep = timestep
        self.dim = dim
        self.delta = delta
        
                
                
    def read_file(self,
                  header:list=None, 
                  header_line:int=3,
                  **kwargs)->pd.DataFrame:
        """read file generated from ``fix ave/chunk bin1d`` command.
        
        Args:
            header (list, optional): a list of data headers. 
                                    Defaults to ``None``, means extracting headers from ``header_line``.
            header_line (int, optional): when ``header=None``, the content in ``line=<header_line>``
                                      will be used as the headers. Defaults to ``2``.
            **kwargs: received parameters of pd.read_csv().
                                      
        Returns:
            pd.DataFrame: DataFrame object read from the file.
                                                  
        Notes:
            There are some default setting in read files:
            - ``comment="#"`` in the files generated by ``fix ave/time``command in LAMMPS.
            - ``sep="\s+"`` set the separator to ``\s+``, matching one or more whitespace characters.
        """
        self._blocks = list([])
        # time_line = self._get_header(num_line_time)   # Timestep Number-of-chunks Total-count
        header = header if header else self._get_header(header_line)  # Chunk Coord1 Ncount ...
        chunknum = int(self._get_header(header_line+1)[0])
        with pd.read_csv(self.path, comment="#", sep='\s+', header=None, names=header, chunksize=chunknum+1, **kwargs) as reader:    
            for i, chunk in enumerate(reader):
                self._blocks.append({}) # set i-th index as dict
                self._blocks[i]["step"] = int(chunk.iloc[0,0])       # Timestep
                self._blocks[i]["nchunk"] = int(chunk.iloc[0,1])         # Number-of-chunks
                self._blocks[i]["total_count"] = chunk.iloc[0,2]    # Total-count
                self._blocks[i]["data"] = chunk.iloc[1:].reset_index(drop=True)
                
 
    
    ## apply func to self.content, #todo
    def apply_function(self, func):
        pass
        
    
    

    def __len__(self): 
        return len(self._blocks)
    def __getitem__(self, i):
        return self._blocks[i]