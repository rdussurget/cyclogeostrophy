# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 17:58:34 2014

@author: lmarie
"""

import numpy as np
from numbers import Number
        
class IncompatibleShapesException(Exception):
    def __init__(self,text):
        self.value=text
    def __str__(self):
        return self.value

class UnknownException(Exception):
    def __init__(self,text):
        self.value=text
    def __str__(self):
        return self.value




class  AGrid:
    """
    Class to encapsulate fields defined on an Arakawa A-Grid.
    The point location convention corresponds to that used in the ROMS model, i.e
    
       ^ 2nd index increases
       |
       |
       X---------X
       |         |
       |         |
       |  H,U,V  |
       |         |
       |         |
       X---------X  -> 1st index increases """
   
    
    def __init__(self,data=None,\
                 periodicX=False,periodicY=False,\
                 ghostvalueE=np.NaN,ghostvalueW=np.NaN,\
                 ghostvalueN=np.NaN,ghostvalueS=np.NaN):
                     
        self.data =data
        
        self.periodicX=periodicX
        self.periodicY=periodicY
        
        self.ghostvalueE=self.data.fill_value
        self.ghostvalueW=self.data.fill_value
        self.ghostvalueN=self.data.fill_value
        self.ghostvalueS=self.data.fill_value

    def __neg__(self):
        return AGrid(-self.data,\
                     periodicX=self.periodicX, \
                     periodicY=self.periodicY,\
                     ghostvalueE=self.ghostvalueE,ghostvalueW=self.ghostvalueW,\
                     ghostvalueN=self.ghostvalueN,ghostvalueS=self.ghostvalueS)
                     
    def __mul__(self,B):
        """ Function that returns a A-grid object containing the product of two A-grid variables.
        """

        if isinstance(B,Number):
            return AGrid(self.data*B,\
                         periodicX=self.periodicX, \
                         periodicY=self.periodicY,\
                         ghostvalueE=self.ghostvalueE,ghostvalueW=self.ghostvalueW,\
                         ghostvalueN=self.ghostvalueN,ghostvalueS=self.ghostvalueS)
                                              
        # check the multiplication is feasible.
        # either the variables have the same shapes,
        # or one is a meridian-wise line that is periodic in the latitudinal direction
        #
                                              
        if self.data.shape[0]!=B.data.shape[0] and not ((self.data.shape[0]==1 and self.periodicX) or (B.data.shape[0]==1 and B.periodicX)):
            raise IncompatibleShapesException('Incompatible variable shapes: self.shape = '+str(self.data.shape)+', B.shape = '+str(B.data.shape))

        # or one is a parallel-wise line that is periodic in the meridional direction and they are on the V,H line or the Psi,U line
        if self.data.shape[1]!=B.data.shape[1] and not ((self.data.shape[1]==1 and self.periodicY) or (B.data.shape[1]==1 and B.periodicY)):
            raise IncompatibleShapesException('Incompatible variable shapes: self.shape = '+str(self.data.shape)+', B.shape = '+str(B.data.shape))

        # easy case. both have the same size.
        # then both variables must be at the same point inside the cell
        if self.data.shape==B.data.shape:                
            return AGrid(self.data*B.data,\
                         periodicX=self.periodicX and B.periodicX, \
                         periodicY=self.periodicY and B.periodicY,\
                         ghostvalueE=self.ghostvalueE,ghostvalueW=self.ghostvalueW,\
                         ghostvalueN=self.ghostvalueN,ghostvalueS=self.ghostvalueS)

        #Trouble is in the X-direction                         
        if self.data.shape[1]==B.data.shape[1]:
            if self.data.shape[0]==1 and self.periodicX:
                tmp=np.tile(self.data,(B.data.shape[0],1))
                return AGrid(tmp*B.data,\
                             periodicX=self.periodicX and B.periodicX, \
                             periodicY=self.periodicY and B.periodicY,\
                             ghostvalueE=B.ghostvalueE,ghostvalueW=B.ghostvalueW,\
                             ghostvalueN=B.ghostvalueN,ghostvalueS=B.ghostvalueS)

            if B.data.shape[0]==1 and B.periodicX:
                tmp=np.tile(B.data,(self.data.shape[0],1))
                return AGrid(self.data*tmp,\
                             periodicX=self.periodicX and B.periodicX, \
                             periodicY=self.periodicY and B.periodicY,\
                             ghostvalueE=self.ghostvalueE,ghostvalueW=self.ghostvalueW,\
                             ghostvalueN=self.ghostvalueN,ghostvalueS=self.ghostvalueS)

          #Trouble is in the Y-direction                         
        if self.data.shape[0]==B.data.shape[0]:
            if self.data.shape[1]==1 and self.periodicY:
                tmp=np.tile(self.data,(1,B.data.shape[1]))
                return AGrid(tmp*B.data,\
                             periodicX=self.periodicX and B.periodicX, \
                             periodicY=self.periodicY and B.periodicY,\
                             ghostvalueE=B.ghostvalueE,ghostvalueW=B.ghostvalueW,\
                             ghostvalueN=B.ghostvalueN,ghostvalueS=B.ghostvalueS)

            if B.data.shape[1]==1 and B.periodicX:
                tmp=np.tile(B.data,(1,self.data.shape[1]))
                return AGrid(self.data*tmp,\
                             periodicX=self.periodicX and B.periodicX, \
                             periodicY=self.periodicY and B.periodicY,\
                             ghostvalueE=self.ghostvalueE,ghostvalueW=self.ghostvalueW,\
                             ghostvalueN=self.ghostvalueN,ghostvalueS=self.ghostvalueS)
                             
        raise UnknownException('Unknown exception in __mul__')

    
    # Use the multiplication operator to define the result of self/B
    def __div__(self,B):
        if isinstance(B,Number):
            return self*(1.0/B)
        else:
            return self*AGrid(1.0/B.data,\
                              periodicX=B.periodicX,\
                              periodicY=B.periodicY,\
                              ghostvalueE=B.ghostvalueE,ghostvalueW=B.ghostvalueW,\
                              ghostvalueN=B.ghostvalueN,ghostvalueS=B.ghostvalueS)

    def __add__(self,B):
        """ Function that returns a A-grid object containing the sum of two A-grid variables.
        """
        if isinstance(B,Number):
            return AGrid(self.data+B,\
                         periodicX=self.periodicX, \
                         periodicY=self.periodicY,\
                         ghostvalueE=self.ghostvalueE,ghostvalueW=self.ghostvalueW,\
                         ghostvalueN=self.ghostvalueN,ghostvalueS=self.ghostvalueS)
                                              
        # check the multiplication is feasible.
        # either the variables have the same shapes,
        # or one is a meridian-wise line that is periodic in the latitudinal direction
        #
                                              
        if self.data.shape[0]!=B.data.shape[0] and not ((self.data.shape[0]==1 and self.periodicX) or (B.data.shape[0]==1 and B.periodicX)):
            raise IncompatibleShapesException('Incompatible variable shapes: self.shape = '+str(self.data.shape)+', B.shape = '+str(B.data.shape))

        # or one is a parallel-wise line that is periodic in the meridional direction and they are on the V,H line or the Psi,U line
        if self.data.shape[1]!=B.data.shape[1] and not ((self.data.shape[1]==1 and self.periodicY) or (B.data.shape[1]==1 and B.periodicY)):
            raise IncompatibleShapesException('Incompatible variable shapes: self.shape = '+str(self.data.shape)+', B.shape = '+str(B.data.shape))

        # easy case. both have the same size.
        # then both variables must be at the same point inside the cell
        if self.data.shape==B.data.shape:                
            return AGrid(self.data+B.data,\
                         periodicX=self.periodicX and B.periodicX, \
                         periodicY=self.periodicY and B.periodicY,\
                         ghostvalueE=self.ghostvalueE,ghostvalueW=self.ghostvalueW,\
                         ghostvalueN=self.ghostvalueN,ghostvalueS=self.ghostvalueS)

        #Trouble is in the X-direction                         
        if self.data.shape[1]==B.data.shape[1]:
            if self.data.shape[0]==1 and self.periodicX:
                tmp=np.tile(self.data,(B.data.shape[0],1))
                return AGrid(tmp+B.data,\
                             periodicX=self.periodicX and B.periodicX, \
                             periodicY=self.periodicY and B.periodicY,\
                             ghostvalueE=B.ghostvalueE,ghostvalueW=B.ghostvalueW,\
                             ghostvalueN=B.ghostvalueN,ghostvalueS=B.ghostvalueS)

            if B.data.shape[0]==1 and B.periodicX:
                tmp=np.tile(B.data,(self.data.shape[0],1))
                return AGrid(self.data+tmp,\
                             periodicX=self.periodicX and B.periodicX, \
                             periodicY=self.periodicY and B.periodicY,\
                             ghostvalueE=self.ghostvalueE,ghostvalueW=self.ghostvalueW,\
                             ghostvalueN=self.ghostvalueN,ghostvalueS=self.ghostvalueS)

          #Trouble is in the Y-direction                         
        if self.data.shape[0]==B.data.shape[0]:
            if self.data.shape[1]==1 and self.periodicY:
                tmp=np.tile(self.data,(1,B.data.shape[1]))
                return AGrid(tmp+B.data,\
                             periodicX=self.periodicX and B.periodicX, \
                             periodicY=self.periodicY and B.periodicY,\
                             ghostvalueE=B.ghostvalueE,ghostvalueW=B.ghostvalueW,\
                             ghostvalueN=B.ghostvalueN,ghostvalueS=B.ghostvalueS)

            if B.data.shape[1]==1 and B.periodicX:
                tmp=np.tile(B.data,(1,self.data.shape[1]))
                return AGrid(self.data+tmp,\
                             periodicX=self.periodicX and B.periodicX, \
                             periodicY=self.periodicY and B.periodicY,\
                             ghostvalueE=self.ghostvalueE,ghostvalueW=self.ghostvalueW,\
                             ghostvalueN=self.ghostvalueN,ghostvalueS=self.ghostvalueS)
                             
        raise UnknownException('Unknown exception in __add__')

    # Use the addition operator to define the result of self-B
    def __sub__(self,B):
        if isinstance(B,Number):
            return self+(-B)
        else:
            return self+AGrid(-B.data,\
                              periodicX=B.periodicX,\
                              periodicY=B.periodicY,\
                              ghostvalueE=B.ghostvalueE,ghostvalueW=B.ghostvalueW,\
                              ghostvalueN=B.ghostvalueN,ghostvalueS=B.ghostvalueS)

        
    def Dx(self):
                      
        if self.periodicX:
            ghostW=self.data[-1,:]
            ghostE=self.data[0,:]
        else:
            ghostW=np.ma.array(np.ndarray((1,self.data.shape[1])))
            ghostW[None,:]=self.ghostvalueW
            ghostE=np.ma.array(np.ndarray((1,self.data.shape[1])))
            ghostE[None,:]=self.ghostvalueE
                
        tmp=np.vstack((ghostW,self.data,ghostE))
        tmp=(tmp[2:,:]-tmp[0:-2,])/2
            
        return AGrid(tmp,\
                     periodicX=self.periodicX,periodicY=self.periodicY,\
                     ghostvalueE=self.ghostvalueE,ghostvalueW=self.ghostvalueW,\
                     ghostvalueN=self.ghostvalueN,ghostvalueS=self.ghostvalueS)

    def Dy(self):
        
        if self.periodicY:
            ghostS=self.data[:,-1]
            ghostN=self.data[:, 0]
        else:
            ghostS=np.ma.array(np.ndarray((self.data.shape[0],1)))
            ghostS[:,None]=self.ghostvalueS
            ghostN=np.ma.array(np.ndarray((self.data.shape[0],1)))
            ghostN[:,None]=self.ghostvalueN
                
        tmp=np.ma.hstack((ghostS,self.data,ghostN))
        tmp=(tmp[:,2:]-tmp[:,0:-2])/2
            
        return AGrid(tmp,\
                     periodicX=self.periodicX,periodicY=self.periodicY,\
                     ghostvalueE=self.ghostvalueE,ghostvalueW=self.ghostvalueW,\
                     ghostvalueN=self.ghostvalueN,ghostvalueS=self.ghostvalueS)
            
    # point-wise multiplication is commutative, so overload __rmul__ as well.
    __rmul__ = __mul__
