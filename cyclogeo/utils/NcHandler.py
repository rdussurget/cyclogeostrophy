'''
Created on 30 mai 2014

@author: rdussurget
'''
import importlib
from cyclogeo.utils.Dataset import Dataset
from collections import OrderedDict

class NcHandler(OrderedDict):
    
    def __init__(self,*args,**kwargs):
        
        super(NcHandler,self).__init__()
        self.AddFile(*args,**kwargs)
        
    def __del__(self):
        
        self.Close()

    def _import(self,*args,**kwargs):
        
        keys=kwargs.pop('_import',{})
        
        for k in keys:
            if isinstance(k,dict):
                for kk in k.keys(): self.__setattr__(kk,importlib.import_module(k[kk]))
            else : self.__setattr__(k,importlib.import_module(k))  

    def Close(self,*args):
        
        if len(args) == 0:
            toclose=self.keys()
        else : toclose=args
        
        #Force closing
        for f in toclose:
            try: self[f].close()
            except: pass
        
    def AddFile(self,*args,**kwargs):
        for i,a in enumerate(args):
            if len(a) > 1: f=a[0]
            else: f=a
            kw=OrderedDict()
            for kk in kwargs.keys(): kw[kk]=kwargs[kk][i]
            self[f]=Dataset(*a,**kw)

    def AppendData(self,**kwargs):
        
        for k in kwargs.keys():
            self.__setattr__(k,kwargs[k])
            
    def Copy(self,fin,fout):
        
        try:
            fi=self[fin]
            fo=self[fout]
        except KeyError : return "[ERROR]:"
        
        # copy nc-file global arguments.
        for attr in fi.ncattrs():
            fo.setncattr(attr,fi.getncattr(attr)[:]) 
            
        # Copy dimensions
        for dimname,dim in fi.dimensions.iteritems():
            if dim.isunlimited(): fo.createDimension(dimname,None)
            else: fo.createDimension(dimname,len(dim))
    
        # Copy variables
        for name in fi.variables:
            var = fi.variables[name]
            varout=fo.createVariable(name, var.dtype.char, var.dimensions)
            
            for attname in var.ncattrs():
                if attname == '_FillValue': continue
                else: setattr(varout,attname,getattr(var,attname))
            
            # Copy the static variables
            varout[:] = var[:]

    def Update(self,ncfile,attrdict={},vardict={},**kwargs):
        
        fi=self[ncfile]
        
        #Update attributes
        for attr in attrdict:
            try: fi.setncattr(attr,eval(attrdict[attr]))
            except SyntaxError: fi.setncattr(attr,attrdict[attr])
        
        for name,Vdict in vardict.iteritems():
            
            
            if not fi.variables.has_key(name):
                _dtype=Vdict.pop('_dtype','f') #Default float
                _dimensions=Vdict.pop('_dimensions',fi.dimensions.keys()[0]) #Default 1st dimension
                var = fi.createVariable(name, _dtype, _dimensions)
            else:
                var = fi.variables[name]
            
            for attname in Vdict.keys():
                
                if attname == '_FillValue': continue
                else :
                    val=Vdict.pop(attname)
                    try: val=eval(val)
                    except SyntaxError: val=val
                    except NameError: val=val
                    
                    if attname == "_data": var[:] = val
                    else: setattr(var,attname,val)
        