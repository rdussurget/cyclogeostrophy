import os, yaml, re
from collections import OrderedDict

from yaml.constructor import Constructor, MappingNode, ConstructorError, SequenceNode, ScalarNode

# from yaml_anydict import Loader_map_as_anydict, dump_anydict_as_map

def omap_constructor(loader, node):
    return loader.construct_pairs(node)

# 'copied from constructor.BaseConstructor, replacing {} with self.anydict()'
# def construct_mapping(loader, node, deep=False):
#     if not isinstance(node, MappingNode):
#         raise ConstructorError(None, None,
#                 "expected a mapping node, but found %s" % node.id,
#                 node.start_mark)
#     mapping = OrderedDict()
#     for key_node, value_node in node.value:
#         key = loader.construct_object(key_node, deep=deep)
#         try:
#             hash(key)
#         except TypeError as exc:
#             raise ConstructorError("while constructing a mapping", node.start_mark,
#                     "found unacceptable key (%s)" % exc, key_node.start_mark)
#         value = loader.construct_object(value_node, deep=deep)
#         mapping[key] = value
#     return mapping
# 
# def construct_yaml_map(loader, node):
#     data = OrderedDict()
#     yield data
#     value = construct_mapping(loader,node)
#     data.update(value)
 
class OrderedDictYAMLLoader(yaml.Loader):
    """
    A YAML loader that loads mappings into ordered dictionaries.
    """
     
    def __init__(self, *args, **kwargs):
        self._root = os.path.split(args[0].name)[0]
        yaml.Loader.__init__(self, *args, **kwargs)
         
        self.add_constructor(u'!include', type(self).include)
        self.add_constructor(u'tag:yaml.org,2002:map', type(self).construct_yaml_map)
        self.add_constructor(u'tag:yaml.org,2002:omap', type(self).construct_yaml_map)
        
        
        
     
    #===========================================================================
    # Ordered dict stuff
    #===========================================================================
    def construct_yaml_map(self, node):
        data = OrderedDict()
        yield data
        value = self.construct_mapping(node)
        data.update(value)
     
    def construct_mapping(self, node, deep=False):
        if isinstance(node, yaml.MappingNode):
            self.flatten_mapping(node)
        else:
            raise yaml.constructor.ConstructorError(None, None,
                                                    'expected a mapping node, but found %s' % node.id, node.start_mark)
     
        mapping = OrderedDict()
        try : 
            for key_node, value_node in node.value:
#                 print 'toto', key_node, value_node, node.tag, node.id
                pass
        except ValueError :
            print 'ValueError with node %s' % node
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
#             print key
#             for nn in node.value: print nn[0].value
            try:
                hash(key)
            except TypeError, exc:
                raise yaml.constructor.ConstructorError('while constructing a mapping',
                                                        node.start_mark, 'found unacceptable key (%s)' % exc, key_node.start_mark)
            value = self.construct_object(value_node, deep=deep)
            mapping[key] = value
        
        return mapping
    
    #===========================================================================
    # Include stuff
    #===========================================================================
    def include(self, node):
        if   isinstance(node, yaml.ScalarNode):
            return self.extractFile(self.construct_scalar(node)) 
        elif isinstance(node, yaml.SequenceNode):
            result = []
            for filename in self.construct_sequence(node):
                result += self.extractFile(filename)
            return result
 
        elif isinstance(node, yaml.MappingNode):
            result = {}
            for k,v in self.construct_mapping(node).iteritems():
                result[k] = self.extractFile(v)
            return result
 
        else:
            print "Error:: unrecognised node type in !include statement"
            raise yaml.constructor.ConstructorError
 
    def extractFile(self, filename):
        filepath = os.path.join(self._root, filename)
        with open(filepath, 'r') as f:
            return yaml.load(f, OrderedDictYAMLLoader)

#     def flatten_mapping(self, node):
#         merge = []
#         index = 0
#         while index < len(node.value):
#             key_node, value_node = node.value[index]
#             if key_node.tag == u'tag:yaml.org,2002:merge':
#                 del node.value[index]
# #                 if isinstance(value_node, ScalarNode):
# #                     value = self.extractFile(self.construct_scalar(value_node))
# #                     value_node=MappingNode(node.tag,value,value_node.start_mark,None,node.flow_style)
#                 if isinstance(value_node, MappingNode):
#                     self.flatten_mapping(value_node)
#                     merge.extend(value_node.value)
#                 elif isinstance(value_node, SequenceNode):
#                     submerge = []
#                     for subnode in value_node.value:
#                         if not isinstance(subnode, MappingNode):
#                             raise ConstructorError("while constructing a mapping",
#                                     node.start_mark,
#                                     "expected a mapping for merging, but found %s"
#                                     % subnode.id, subnode.start_mark)
#                         self.flatten_mapping(subnode)
#                         submerge.append(subnode.value)
#                     submerge.reverse()
#                     for value in submerge:
#                         merge.extend(value)
# #                 elif isinstance(value_node, ScalarNode):
# #                     value = self.extractFile(self.construct_scalar(value_node))
# #                     seq=MappingNode(node.tag,value,value_node.start_mark,None,node.flow_style)
# # #                     self.flatten_mapping(seq)
# #                     value_node=seq
# #                     self.flatten_mapping(value_node)
# # #                     value_node.value=seq
# #                     merge.extend(value_node.value)
# # #                     value_node.value = seq     
# # #                     merge.extend(seq)
#                 else:
#                     raise ConstructorError("while constructing a mapping", node.start_mark,
#                             "expected a mapping or list of mappings for merging, but found %s"
#                             % value_node.id, value_node.start_mark)
#             elif key_node.tag == u'tag:yaml.org,2002:value':
#                 key_node.tag = u'tag:yaml.org,2002:str'
#                 index += 1
#             else:
#                 index += 1
#         if merge:
#             node.value = merge + node.value

# class Loader(yaml.SafeLoader):
# 
# #     anydict = OrderedDict()
#     
#     def __init__(self, stream):
#         self._root = os.path.split(stream.name)[0]
#         super(Loader, self).__init__(stream)
#         yaml.add_constructor('!include', Loader.include)
# #         self.add_constructor(u'tag:yaml.org,2002:map', construct_yaml_map)
# #         yaml.add_constructor(u'!omap', omap_constructor)
#         pass
# #         self.load_map_as_anydict()
# #         Loader.add_constructor('tag:yaml.org,2002:merge', Loader.merge)
#         #Loader.add_constructor('!import',  Loader.include)
#  
# #     @classmethod        #and call this
# #     def load_map_as_anydict(self):
# #         yaml.add_constructor( 'tag:yaml.org,2002:map', self.construct_yaml_map)
# #         pass
# 
#     def include(self, node):
#         if   isinstance(node, yaml.ScalarNode):
#             return self.extractFile(self.construct_scalar(node))
#  
#         elif isinstance(node, yaml.SequenceNode):
#             result = []
#             for filename in self.construct_sequence(node):
#                 result += self.extractFile(filename)
#             return result
#  
#         elif isinstance(node, yaml.MappingNode):
#             result = {}
#             for k,v in self.construct_mapping(node).iteritems():
#                 result[k] = self.extractFile(v)
#             return result
#  
#         else:
#             print "Error:: unrecognised node type in !include statement"
#             raise yaml.constructor.ConstructorError
#  
#     def extractFile(self, filename):
#         filepath = os.path.join(self._root, filename)
#         with open(filepath, 'r') as f:
#             return yaml.load(f, Loader)
#     
#     #def __call__(self):
#         #print "in_call"
#         #Loader.load_map_as_anydict()
#         #dump_anydict_as_map(OrderedDict)
#         #return self

def updateParam(data,value):

    V=value
    
    r=re.compile('\%{[A-Z_a-z:0-9*?]+}') #
#     r=re.compile('\%{.+}') #matches any character between braces
    
    try: occur=r.findall(V)
    except: return V
    
    noccur=0
    
    while len(r.findall(V)) > noccur:
        for pat in r.findall(V) :
            cmd='data'
            key=pat[2:-1]
            for k in key.split(':'): cmd+="['%s']" % k
            try :
                V=V.replace(pat,"%s" % eval(cmd))
#                 V=eval(V)
            except:
                print "%s not found" % cmd
                noccur+=1 #this allow passing to any other occurences and to step out when we have replaced the most expressions we could
    
    #UPDATE AT THIS POINT OR NOT??
    #--> eval shall not be called at this point when using Processor (as it does it later on)
#     try: return eval(V)
#     except :return V
    try:
        res=eval(V)
        if isinstance(res,type(any)): res=V
        return res
    except: return V

# def traverse_tree(dictionary, id=None):
#     for key, value in dictionary.items():
#         if key == 'id':
#             if value == id:
#                 print dictionary
#         else:
#              traverse_tree(value, id)
#     return


def updateDict(*args,**kwargs):
    
    f_param=updateParam
    for k in kwargs.keys(): f_param=kwargs.pop(k)
     
    if len(args) == 1 :
        dIn=args[0]
        d=args[0]
    else:
        dIn,d=args
         
    for k in d.keys():
#         print d[k]
        if isinstance(d[k],dict):
            dum={k:updateDict(dIn,d[k])}
        elif isinstance(d[k],(list,tuple)):
            dum={k:[]}
            for dd in d[k]:
                if isinstance(dd,dict): dum[k]+=[updateDict(dIn,dd)]
                else : dum[k]+=[f_param(dIn,dd)]
        else:
            dum={k:f_param(dIn,d[k])}
         
        d.update(dum)
 
    return d

