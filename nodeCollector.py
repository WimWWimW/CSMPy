import ast
from enum import Enum
from segment import SegmentLabel
from nodeWraps import NodeWrap, ImportDecl, IntegralDecl, ConstantDecl,\
    LabelDecl
from customTypes import VarType


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
    wrapperClass = ImportDecl
    
    def run(self, tree):
        self.visit_Import       = self._processNode_
        self.visit_ImportFrom   = self._processNode_
        return super().run(tree)
    
    
    def _processNode_(self, node):
        return self.accept(node)


class IntegralCollector(NodeCollector):        
    wrapperClass = IntegralDecl
    
    def run(self, tree):
        # self.extract      = False
        self.visit_Assign = self._processNode_
        return super().run(tree)
    
    @staticmethod
    def matches(node):    
        return isinstance(node.value, ast.Call) and node.value.func.id == "INTGRL"
    
    
    def _processNode_(self, node):
        if self.matches(node):
            return self.accept(node)
        return node


        
class ConstantCollector(NodeCollector):        
    wrapperClass = ConstantDecl
    
    def run(self, tree, varType: VarType):
        self.varType    = varType
        self.visit_Assign = self._processNode_
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


        
