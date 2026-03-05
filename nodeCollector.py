import ast
from enum import Enum
from segment import SegmentLabel
from nodeWraps import NodeWrap, IntegralDecl, ConstantDecl, LabelDecl
from customTypes import VarType
from collections import defaultdict


class NodeCollector(ast.NodeTransformer):

    wrapperClass = NodeWrap
     
    def __init__(self):
        self.nodes   = []
        self.extract = True

    
    def run(self, tree):
        self.visit(tree)
        return self.nodes


    def accept(self, node, *args, **kwargs):
        self.nodes.append(self.wrapperClass(node, *args, **kwargs))
        return None if self.extract else node
    
    
    def _processNode_(self, node):
        return None 
        

    
class ImportCollector(NodeCollector):
    # wrapperClass = ImportDecl
    
    def run(self, tree):
        self.visit_Import       = self._processNode_
        self.visit_ImportFrom   = self._processNode_
        return super().run(tree)
    
    
    def _processNode_(self, node):
        return self.accept(node)


class DeclarationCollector(NodeCollector):

    def __init__(self):
        super().__init__()
        self.originator = type(self).__name__
        
        
    def checkMultipleDefinitions(self, items):
        itemDict = defaultdict(list)
        for item in items: 
            itemDict[item.name].append(item)
        if len(itemDict) < len(items):
            for name, wraps in itemDict.items():
                if len(wraps) > 1:
                    for item in wraps[1:]:
                        item.addRemark("redefinition of immutable variable '%s'" % name, originator = self.originator)

                        
    def run(self, tree):
        self.visit_Assign = self._processNode_
        items = super().run(tree)
        self.checkMultipleDefinitions(items)
        return items 
    
    
class IntegralCollector(DeclarationCollector):        
    wrapperClass = IntegralDecl
    
    def run(self, tree):
        self.originator = "stateVarCheck"
        return super().run(tree)
    
    @staticmethod
    def matches(node):    
        return isinstance(node.value, ast.Call) and node.value.func.id == "INTGRL"
    
    
    def _processNode_(self, node):
        if self.matches(node):
            return self.accept(node)
        return node


        
class ConstantCollector(DeclarationCollector):        
    wrapperClass = ConstantDecl
    
    def run(self, tree, varType: VarType):
        self.varType    = varType
        self.originator = "%sCheck" % varType.name.capitalize()
        return super().run(tree)
    
    
    def _processNode_(self, node):
        if isinstance(node.value, ast.Call) and node.value.func.id == self.varType.name:
            return self.accept(node, self.varType)
        return node


        
class SectionCollector(NodeCollector):        
    wrapperClass = LabelDecl
    
    def run(self, tree):
        self.visit_Expr = self._processNode_
        return super().run(tree)
    
    
    def _processNode_(self, node):
        if isinstance(node.value, ast.Constant) and node.value.value in dir(SegmentLabel):
            return self.accept(node)
        return node


        
class VarlistCollector(NodeCollector):
    #wrapperClass = ConstantDecl
    
    def run(self, tree, varType: VarType, existing):
        self.varType        = varType
        self.visit_Expr     = self._processNode_
        items = super().run(tree)
        # self.checkMultipleDefinitions(items)
        return items 
    
    def _processNode_(self, node):
        if isinstance(node.value, ast.Call) and node.value.func.id == self.varType.name:
            s = "\n".join([ast.unparse(k) for k in node.value.keywords])
            for n in ast.parse(s).body:
                self.accept(n, name = n.targets[0].id, varType = self.varType, line = (node.lineno, node.end_lineno))
            return None
        return node
    