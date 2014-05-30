import yaml as Y, os
from cyclogeo.utils.yaml_loader import updateDict, OrderedDictYAMLLoader as Loader

def LoadYaml(yaml=None):
    
    if not yaml : yaml= os.path.join(os.path.dirname(__file__),'nc.yaml')
    with open(yaml,'r') as yaml:
        res=Y.load(yaml, Loader)
        
    return res 

