#!/usr/bin/python

import sys
import datetime
import numpy as np
import matplotlib.pyplot as plt
from collections import OrderedDict
#from mpl_toolkits.basemap import Basemap
from cyclogeo.utils import Dataset, AGrid, NcHandler, LoadYaml


#~ fh=sys.argv[1]
fuv=sys.argv[1]
fout=sys.argv[2]

h=NcHandler(*zip(*((fuv,fout),('r','w'))),
            **{'clobber':(False,True)})


#~ H=h[fh].getNCVar('Grid_0001',factor=1.0/100,mask='np.abs(VAR)>10',transform='np.roll(VAR,720,axis=0)',periodicX=True,periodicY=False)
ug=h[fuv].getNCVar('Grid_0001',factor=1.0/100,mask='np.abs(VAR)>1000',transform='np.roll(VAR,720,axis=0)',periodicX=True,periodicY=False)
vg=h[fuv].getNCVar('Grid_0002',factor=1.0/100,mask='np.abs(VAR)>1000',transform='np.roll(VAR,720,axis=0)',periodicX=True,periodicY=False)
LatStep=h[fuv].variables['LatLonStep'][0]
LonStep=h[fuv].variables['LatLonStep'][1]
Lat=h[fuv].getNCVar('NbLatitudes',transform='VAR[None,:]',periodicX=True ,periodicY=False)
Lon=h[fuv].getNCVar('NbLongitudes',transform='np.roll(np.mod(VAR[:,None]+180,360)-180,720,axis=0)',periodicX=False,periodicY=True)
# h[fh].close()

# compute the gravity acceleration (WGS84 formula from wikipedia)
g=AGrid(9.7803267714*(1+0.00193185138639*np.sin(Lat.data/180*np.pi)**2)/np.sqrt(1-0.00669437999013*np.sin(Lat.data/180*np.pi)**2),periodicX=True)

# get scale factors for derivatives
# Radius of the earth from WGS84 formulae.
f=1/298.257223563
a=6378137
b=a*(1-f)
Er=AGrid(a/np.sqrt(1+b**2/a**2*np.tan(Lat.data/180*np.pi)**2),periodicX=True)

dlondx=AGrid(180/np.pi/Er.data/LonStep,periodicX=True)
dlatdy=180/np.pi/6371000/LatStep

# Coriolis parameter at H-points
fC=AGrid(2*2*np.pi/86400*np.sin(Lat.data/180*np.pi),periodicX=True)

#A convenient way of flagging at low latitudes...
fC.data[np.abs(Lat.data)<=2]=np.NaN

un=ug+0; vn=vg+0;
duold=np.zeros(ug.data.shape);duold[:,:]=np.Inf
dvold=np.zeros(vg.data.shape);dvold[:,:]=np.Inf
nbiteru=np.zeros(ug.data.shape)
nbiterv=np.zeros(vg.data.shape)

iter=-1

#Never do more than 20 iterations
while iter <= 20:
    
    iter+=1
    
    dxux=dlondx*un.Dx()
    dyux=dlatdy*un.Dy()
    dxuy=dlondx*vn.Dx()
    dyuy=dlatdy*vn.Dy()
    
    ugradux=un*dxux+vn*dyux
    ugraduy=un*dxuy+vn*dyuy
    
    un1=ug-ugraduy/fC
    vn1=vg+ugradux/fC

    du=(un1-un).data;dv=(vn1-vn).data
    
    #idivu keeps track of the places where the solution worsens, and convergence has not been achieved yet.
    #iconvu keeps track of the places where the solution gets better
    #iendu keeps track of the places where convergence has been achieved.
    idivu =np.abs(du)>=duold;idivv =np.abs(dv)>=dvold
    iconvu=np.abs(du)< duold;iconvv=np.abs(dv)< dvold
    iendu =np.abs(du)< 1e-2 ;iendv =np.abs(dv)< 1e-2
    idivu*=-iendu           ;idivv*=-iendv;
    
    # If we can have an improvement, we take it
    un.data[iconvu]=un1.data[iconvu];vn.data[iconvv]=vn1.data[iconvv]
    duold[iconvu]=du[iconvu];dvold[iconvv]=dv[iconvv]
    nbiteru[iconvu*(-iendu)]+=1;nbiterv[iconvv*(-iendv)]+=1;
    
    #~ print('u',np.sum(-(idivu+iendu+np.isnan(un1.data))))
    #~ print('v',np.sum(-(idivv+iendv+np.isnan(vn1.data))))

    if np.sum(-(idivu+iendu+np.isnan(un1.data)))<=20 and np.sum(-(idivv+iendv+np.isnan(vn1.data)))<=20:
        break



#convert back speeds to cm/s
un*=100.
vn*=100.


#Save data    
fun_cast=np.uint8
fu=fv=np.ma.zeros(un.data.shape,dtype=fun_cast,fill_value=fun_cast(-1))
un.data.mask=un.data.mask | idivu
vn.data.mask=vn.data.mask | idivv
fu[:]=nbiteru.astype(fun_cast) ; fu.mask=idivu
fv[:]=nbiterv.astype(fun_cast) ; fv.mask=idivv


h.Copy(fuv,fout)
h.AppendData(**{'un':np.roll(un.data,-720,axis=0),
                'vn':np.roll(vn.data,-720,axis=0),
                'fu':np.roll(fu,-720,axis=0),
                'fv':np.roll(fv,-720,axis=0)})
    
kwargs=LoadYaml()
h._import(**kwargs)
h.Update(fout,**kwargs)

    


