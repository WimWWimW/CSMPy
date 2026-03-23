from csmp.precompiler.csmpStatements import PARAM, CONSTANT, INCON, FUNCTION, TABLE, OVERLAY, RENAME, FIXED, MEMORY, HISTORY, STORAGE, DECK, MACRO, END, \
    CONTINUE, PROCEDURE, STOP, ENDJOB, COMMON, DATA, TIMER, FINISH, RELERR, ABSERR, METHOD, PRINT, OUTPUT, TITLE, PREPARE, PRTPLOT, LABEL, RANGE, RESET,\
    AFGEN, NLFGEN # these two were moved to keywords since they require class instantiation 

from csmp.functions import ABS, ALOG, ALOG10, AMAX0, AMAX1, AMIN0, AMIN1, AND, ATAN, CMPXPL, COMPAR, COS, DEADSP, DELAY, DERIV, EOR, EQUIV, EXP, \
    FCNSW, GAUSS, HSTRSS, IABS, IMPL, IMPULS, INSW, LEDLAG, LIMIT, MAX0, MAX1, MIN0, MIN1, MODINT, NAND, NOR, NOT, OUTSW, PULSE, RAMP, REALPL, \
    RNDGEN, RST, SIN, SINE, SQRT, STEP, TANH, ZHOLD

from csmp.rts.linearExtrapolators import Clip, LastSegment, Regression
from csmp.rts import CSMP_Model




import warnings,sys, inspect
from lib.settings import Settings
from lib.options import Options
from lib import options
from csmp.precompiler import Precompiler

def simpleWarning(message, category, filename, lineno, line=None):
    return f"{category.__name__}: {message}\n"

warnings.formatwarning = simpleWarning




IS_RELEASE = not True  # set this value to True in releases to prevent user-overload

def lessSimpleErrors(type, value, tb):
    try:
        # print(f"{type.__name__}: {value}", file = sys.stderr)
        # reduced error tracing with still some info:
        last_frame  = tb
        while last_frame.tb_next:
            last_frame = last_frame.tb_next
        instance    = last_frame.tb_frame.f_locals.get('self')
        cls         = instance.__class__
        fileName    = inspect.getfile(cls).split("/")[-1]
        print(f"{type.__name__}: {value} [{cls.__name__} in {fileName}]", file = sys.stdout)
    except:
        # if that didn't work out, call original:
        savedHook(type, value, tb)


if IS_RELEASE:
    savedHook       = sys.excepthook 
    sys.excepthook  = lessSimpleErrors
else:
    sys.tracebacklimit = 300
    



class CsmpOptions(Options):
    
    def __init__(self, settings):
        super().__init__("")
        self.settings = settings
        self.listFile = self._getFileOptions("precompiler", "listFile")
        self.summary  = self._getFileOptions("precompiler", "summary")
        self.sorted   = self._getFileOptions("precompiler", "sorted")
        self.unsorted = self._getFileOptions("precompiler", "unsorted")
        self.debugSeg = self._getFileOptions("precompiler", "debugSeg")
        
        self.template        = self.settings.get("templates", "template")
        self.templateComment = self.settings.get("templates", "segmentComment")
        self.templatePlcHldr = self.settings.get("templates", "placeholder")
            

    def _getFileOptions(self, section, key):
        setting = self.settings.get(section, key, "").replace(", ", ",").split(',')
        return dict(scrn = "show" in setting,
                    file = "save" in setting)


class CSMPy:
    
    def __init__(self):
        self.options  = CsmpOptions(Settings("./", "csmp.config"))
        self.compiled = False
        self.complete = False
    
    def compile(self, model):
        self.compiled = False
        self.complete = False
        mdl = Precompiler(self.options)
        mdl.compile(model)
        self.compiled = mdl.succes
        self.model    = mdl
        
        
        
        
        