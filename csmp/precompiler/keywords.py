"""
This modue defines the CSMP keywords, i.e. statements, that require some action to be taken that
includes more than only returning a function result.

The Keyword's class structure takes a leaf from the book of ast: The methods they define determine
to which categories (KeywordLabels) they pertain. Such methods conform the naming format

def transformLabelname(self): ...

"""

# from csmp.customTypes import IntegrationMethod
import lib.ast_comments as ast
from lib.smallUtilities import dump, walkSmarter

from csmp.precompiler.keywordsBase import Keyword, KeywordStatus, KeywordLabels, ConstantDeclaration
from csmp.precompiler.lister import Lister
from csmp import errors

def symbols():
    return [n for n in globals() if n == n.upper() and not n.startswith("_") ]


class CONSTANT(ConstantDeclaration):
    def transformConstants(self):
        return self._keywordArgsToAssignments()


class PARAM(ConstantDeclaration):
    def transformParameters(self):
        return self._keywordArgsToAssignments()


class INCON(ConstantDeclaration):
    def transformIncons(self):
        return self._keywordArgsToAssignments()



class INTGRL(Keyword):

    def transformInitStates(self):
        args = self._getArgs() 
        return self._nodeFromString(f"self.createStateVariable({self.index}, '{self.name}', {args})")

        
    def transformRestoreValues(self):
        return self._nodeFromString(f"{self.name} = self.getState({self.index})")
        
        
    def transformUpdate(self):
        rate = ast.unparse(self._base_.args[1])
        return self._nodeFromString(f"self.setCurrentRate({self.index}, {rate})")
        
        

class FUNCTION(Keyword):

    def transformFunctions(self):
        args = self._getArgs() 
        return self._nodeFromString(f"self.createCsmpFunction({self.index}, '{self.name}', {args})")



        
class AFGEN(Keyword):        
    # formally this is not a keyword but a function. But it behaves like a keyword
    # in that it has to be predefined. Also it's got to be linked to its FUNCTION
    # object before writing the runnable model.
    
    # TODO: ought to be found by ast.Call, not by assign...
    
    def __init__(self, node: ast.AST, name: str, **kwargs):
        super().__init__(node, name, **kwargs)
        self.linkedFunction = -1

    def link(self, functions):
        functionName = self._base_.args[0].id
        self.linkedFunction = functions.get(functionName, -99999)
        
    
    def transformGenerators(self):
        args = self._getKwds() 
        return self._nodeFromString(f"self.create{self.className(1)}({self.index}, function = {self.linkedFunction}, {args})")

        
    def transformInplace(self):
        # e.g.: REDF = self.funcGenerators[0].getValue(LAI * 4 - R1)
        arg = ast.unparse(self._base_.args[1]) 
        return self._nodeFromString(f"{self.name} = self.funcGenerators[{self.index}].getValue({arg})")



        
class NLFGEN(AFGEN):        
    # formally this is not a keyword but a function. But it behaves like a keyword
    # in that it has to be predefined. Also it's got to be linked to its FUNCTION
    # object before writing the runnable model.
    pass
    
    
    

class TABLE(Keyword):
    ...


class OVERLAY(Keyword):
    status  = KeywordStatus.not_supported



# CONTROL statements:
class RENAME(Keyword):
    ...
    

class FIXED(Keyword):
    status  = KeywordStatus.obsolete



class MEMORY(Keyword):
    '''
    CSMPy syntax:
    
    MEMORY(<function call>, <initial values>)
    '''
    
    def __init__(self, node, *args, **kwargs):
        if isinstance(node, ast.Expr):
            raise errors.PrecompilerError(f"a {self.className(2)} function must have at least one return value")
        super().__init__(node, *args, **kwargs)
        self._declaration = self._createObject() # for early error detection
        
        
    def _createObject(self):
        def fail(msg):
            self.addRemark(msg)
            raise errors.PrecompilerError(msg)
        
        size = lambda node: (len(node) if isinstance(node, (list,)) else 
                             len(node.elts) if isinstance(node, (ast.List, ast.Tuple)) else
                             0) 
         
        targets = size(self.node.targets[0])
        args    = self.node.value.args
        function= args[0].func.id 
        
        if size(args) == 2:
            initVal = args[1]
            initSize = size(initVal)
            if initSize != targets:
                raise errors.PrecompilerError(f"{self.className()}: invalid number of initial values ({initSize})")
        else:
            fail(f"{self.className()}: invalid number of arguments")
        
        initVal = ast.unparse(initVal)
        call    = f"self.create{self.className(1)}Function"
        return f"{call}({self.index}, call = {function}, initial = {initVal})"


    def transformMemoryObjects(self):
        return self._nodeFromString(self._declaration)
    
        
    def transformInplace(self):
        targets = ", ".join([p.id for p in walkSmarter(self.node.targets[0], [ast.Name])])
        args    = ", ".join([ast.unparse(a) for a in self.node.value.args[0].args])
        call    = f"self.{self.className(2)}Function"
        return self._nodeFromString(f"{targets} = {call}[{self.index}]({args})")


class HISTORY(Keyword):
    ...



class STORAGE(Keyword):
    status  = KeywordStatus.obsolete



class DECK(Keyword):
    status  = KeywordStatus.not_supported


class __OherKeyword__(Keyword):
    status  = KeywordStatus.other
class MACRO(__OherKeyword__): pass 
class INITIAL(__OherKeyword__): pass 
class DYNAMIC(__OherKeyword__): pass 
class TERMINAL(__OherKeyword__): pass 
class SORT(__OherKeyword__): pass 
class NOSORT(__OherKeyword__): pass 


class END(Keyword):
    status  = KeywordStatus.ignored


class CONTINUE(Keyword):
    status  = KeywordStatus.not_supported


class PROCEDURE(Keyword):
    status  = KeywordStatus.obsolete


class STOP(Keyword):
    status  = KeywordStatus.ignored


class ENDJOB(Keyword):
    status  = KeywordStatus.ignored


# ENDJOB STACK
class COMMON(Keyword):
    status  = KeywordStatus.undecided


# COMMON MEM  
class DATA(Keyword):
    status  = KeywordStatus.obsolete


# Execution control statements:
class ExecutionControl(Keyword):

    def transformSystemParams(self):
        args = self._allArguments() 
        return self._nodeFromString(f"self.set{self.className().capitalize()}({args})")


class TIMER(ExecutionControl):
    pass

class FINISH(ExecutionControl):
    pass

class RELERR(Keyword):
    ...

class ABSERR(Keyword):
    ...


class METHOD(ExecutionControl):
    pass


class TITLE(ExecutionControl):
    pass

class Varlist(Keyword):
    @staticmethod
    def __execute__(*varNames): return

    def transformSystemParams(self):
        args = self._varlist() 
        return self._nodeFromString(f"self.set{self.className().capitalize()}({args})")

# Output control statements:
class PRINT(Varlist):
    pass

class OUTPUT(Keyword):
    pass

class PREPARE(Keyword):
    ...

class PRTPLOT(Keyword):
    ...

class LABEL(Keyword):
    ...

class RANGE(Keyword):
    ...

class RESET(Keyword):
    status  = KeywordStatus.not_supported


# ----------------------------------------------------------------------------------------------

def registerAndInitializeKeywords(): 
    for n, c in globals().items(): 
        if n == n.upper() and not n.startswith("_") and issubclass(c, Keyword):
            c.initialize()

registerAndInitializeKeywords()

# ----------------------------------------------------------------------------------------------


if __name__ == '__main__':
    import re
    
    for c in Keyword.classes.values():
        print(c.className(1), "-->", c.status)
        
        
    for s in "TIME, DELT, DELMIN, FINTIM, PRDEL, OUTDEL".split(", "):
        print("%s = '%s'" % (s, s.status), end = ", ")
    