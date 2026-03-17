import copy
from collections import defaultdict
from enum import Enum
from warnings import warn
import lib.ast_comments as ast

from csmp import errors
from csmp.precompiler.nodeWraps import NodeWrap
from lib.smallUtilities import walkSmarter


class KeywordStatus(Enum):
    UNDEFINED           = 0
    OK                  = 1
    ignored             =-2
    obsolete            =-3
    not_supported       =-4
    not_yet_supported   =-5
    undecided           =-6
    other               = -999
    
    
    def humanReadable(self):
        return self.name.replace("_", " ")


class KeywordLabels(Enum):    
    initial         = "INITIAL segment"
    dynamic         = "DYNAMIC segment"
    terminal        = "TERMINAL segment"
    common          = "'common block'"
    constants       = "constant definitions"
    parameters      = "parameter definitions"
    incons          = "incon definitions"
    functions       = "function definitions"
    generators      = "function generator objects"
    initStates      = "state variable creation"
    memoryObjects   = "memory object creation"        
    historyObjects  = "history object creation"        
    systemParams    = "parametrize the model"
    restoreValues   = "current values of state variables"
    update          = "update rates"

    def capitalize(self):
        # capitalize first character but leave the rest as it is:
        s = self.name
        return s[0].upper() + s[1:]


    def mainSegment(self):
        cls = type(self)
        return self in (cls.initial, cls.dynamic, cls.terminal)
    
    
    

class KeywordClass(NodeWrap): # TODO doubtfully distinct from Keyword
    classes   = {}                  # registered classed
    instances = defaultdict(list)   # instances per class (to generate an index)
    
    
    def __init__(self, node: ast.AST, name: str = None, **moreArgs):
        super().__init__(node, **moreArgs)
        self.name    = name
        instanceList = KeywordClass.instances[self._instanceLabel()]
        instanceList.append(self)
        self.index   = instanceList.index(self)
        if isinstance(self.node, ast.Assign):
            self._base_ = self.node.value
        elif isinstance(self.node, ast.Expr):
            self._base_ = self.node.value
        else:
            raise Exception(type(self.node))
        
        
    @classmethod
    def _instanceLabel(cls):
        return cls.__name__

    
    @classmethod
    def _clear(cls):
        cls.instances[cls._instanceLabel()].clear()
        
        
    @classmethod
    def clearAll(cls):
        cls.instances.clear()
        
    
    @classmethod
    def className(cls, format = 0):
        fmt = {1: str.capitalize, 2: str.lower}
        if type(cls) != type:
            cls = cls.__class__
        
        cap = fmt.get(format, str)
        return cap(cls.__name__)    

    @classmethod    
    def __class_getitem__(cls, name):
        return cls.classes.get(name)

    @classmethod
    def initialize(cls):
        # register class:
        Keyword.classes[cls.__name__] = cls
        
        # initialize categories:
        cls.categories = set()
        for cat in KeywordLabels:
            if hasattr(cls, f"transform{cat.capitalize()}"):
                cls.categories.add(cat)
        
        if cls.status == KeywordStatus.UNDEFINED:
            cls.status = KeywordStatus.OK if cls.categories else KeywordStatus.not_yet_supported

        if cls.declaration is None:
            cls.declaration = "set" + cls.className().capitalize()
            
        
    
class Keyword(KeywordClass):                   
    status      = KeywordStatus.UNDEFINED
    categories  = set()
    extract     = True
    declaration = None
    astClasses  = [ast.Expr] # supported classes to create from
    
    
    def _copyNode(self):
        newNode = copy.deepcopy(self.node)
        self.sync(newNode)
        return newNode


    def _nodeFromString(self, source):
        mod    = ast.parse(source)
        result = mod.body[0]
        self.sync(result)
        return result

    
    def _getArgs(self):
        return ",".join([ast.unparse(arg) for arg in self._base_.args])

    
    def _getKwds(self):
        return ",".join([ast.unparse(arg) for arg in self._base_.keywords])

    
    def _allArguments(self):
        return ",".join([ast.unparse(arg) for arg in self._base_.args + self._base_.keywords])

    def _varlist(self):
        return ",".join([f"'{arg.id}'" for arg in self._base_.args])
    
    

    def inplace(self):
        if self.status == KeywordStatus.not_supported:
            raise errors.PrecompilerError(f"{self.className()} is not supported in CSMPy")
        
        if self.status == KeywordStatus.ignored:
            warn(f"{self.className()} is ignored", category=SyntaxWarning)
            return None
        
        if self.status.value <= KeywordStatus.not_yet_supported.value:
            warn(f"{self.className()} has status '{self.status.humanReadable()}' in CSMPy and will not be proceessed now", category=SyntaxWarning)
            return None

        return self.transformInplace()
    
    
    def transformInplace(self):
        return None if self.extract else self.node


    def transform(self, category: KeywordLabels):
        if not category in self.categories:
            return self._errorWrap("EROR:", f"cannot transform {self.keyword.name} to {category.name}")
            # raise errors.ProgramError(f"cannot transform {self.keyword.name} to {category.name}")
        
        methodName  = f"transform{category.capitalize()}"
        method      = getattr(self, methodName, None)
        if method is None:
            raise errors.NotYetImplementedError(f"{self.className()}.{methodName}()")
        
        return method()



class AssigningStatement(Keyword):
    astClasses  = [ast.Assign] # supported classes to create from

    def __init__(self, node, *args):
        if not ("targets" in node._fields):
            raise errors.PrecompilerError("syntax not understood")

    def _getTargets(self):
        return [p.id for p in walkSmarter(self.node.targets[0], [ast.Name])]
    
    
class ConstantDeclaration(Keyword):
    ''' common ancestor for CONSTANT, PARAM and INCON (perhaps more in the future)
    
    This class evolved to be a bit more complex than other keywords, due to the 
    facts that
    - constants can be declared in a compound syntax
    - the statements can appear as assigments or as expressions
    - the resulting code must make depencencies explicit to the sorter (and thus to Python)
    - the resulting code must make the assigned values easily accessible for evaluation
      in the precompiler phase.
    
    The compound syntax (e.g.  CONSTANT(a = 1, b = 2...)) is undesirable since it does not
    make the names and values explicit; therefore the KeywordCollector immediately splits
    such statements into their atomic form (a = CONSTANT(1); b = CONSTANT(2) ...)
    '''
    
    def _keywordArgsToAssignments(self): # TODO: mostly obsolete; refactoring desired.
        if (len(self._base_.args) == 1) and self.name:
            value = ast.unparse(self._base_.args[0])
            return self._nodeFromString(f"{self.name} = {value}")
            
        # status = confused ...
        if Lister.exists():  # @UndefinedVariable
            self.addRemark(f"invalid {self.className()}-declaration")
        return self.node
        
        
    def toString(self): # NOT __str__ !!
        return self.list()

    def getValue(self):
        return ast.unparse(self._base_.args[0])
    
    
    def getName(self):
        return ast.unparse(self._base_.targets[0].id)
    
    
    def list(self):
        return ast.unparse(self._keywordArgsToAssignments())
        return f"{self.name} = {self.toString()})"


