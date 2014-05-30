import netCDF4, numpy as np
from cyclogeo.utils.AGrid import AGrid
'''
Created on 28 mai 2014

@author: rdussurget
'''

class Dataset(netCDF4.Dataset):
    '''
    classdocs
    '''
    
    def getNCVar(self,VarName,**kwargs):
        factor=kwargs.pop('factor',1.0)
        transform=kwargs.pop('transform',None)
        mask=kwargs.pop('mask',None)
        
        v=self.variables[VarName]
        
        VAR=np.ma.array(v[:])
        VAR*=factor
        if transform :
            try: VAR=eval(transform)
            except: pass
        if mask :
            try:
                mask=eval(mask)
                VAR.data[mask]=VAR.fill_value
                VAR.mask[mask]=True
            except: pass
        
        return AGrid(VAR,**kwargs)
        