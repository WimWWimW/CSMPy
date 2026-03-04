import sys
from logging import ERROR, WARNING, INFO, _levelToName as levelName
from collections import defaultdict
from lib.singleton import Singleton


class Lister(metaclass = Singleton):
    FINAL   = -1
    INITIAL = -2

    @staticmethod        
    def withContextError(method):
        # @decorator to sent contextual information to Lister
        def wrapper(*args, **kwargs):
            try:
                method(*args, **kwargs)
            except Exception as e:        
                context      = method.__name__
                if context.startswith("_"): context = context[1:]
                Lister().addError(str(e), Lister.FINAL, context)
                raise
        return wrapper
        
        
    def __init__(self):
        self.messages   = {}
            
            
    def start(self):
        factory = lambda : defaultdict(list)
        self.messages = defaultdict(factory)

        
    def addMessage(self, level: int, message: str, sourceLine: int, originator: str):
        self.messages[sourceLine][level].append((message, originator))
    
    def addError(self, message: str, sourceLine: int, originator: str):
        self.addMessage(ERROR, message, sourceLine, originator)
        
    def addWarning(self, message: str, sourceLine: int, originator: str):
        self.addMessage(WARNING, message, sourceLine, originator)
        
    def addInfo(self, message: str, sourceLine: int, originator: str):
        self.addMessage(INFO, message, sourceLine, originator)
        
        
    def report(self, code, file = sys.stdout, lineOffset = 1):
        decoration = {ERROR: "**", WARNING: "!!", INFO: ">>"}
        def printRemarks(line):
            n = 0
            all = self.messages.get(line, {})
            for level in (ERROR, WARNING, INFO):
                lvl = all.get(level, [])
                for msg in lvl:
                    print("%s %s: %s (%s)" % (decoration.get(level, "??"), levelName[level], *msg), file = file)
                    n += 1
            return (n > 0) # anything done
        
        
        code = code.split("\n")

        printRemarks(self.INITIAL)
        print("\n", file = file)
        
        for i, line in enumerate(code):
            print("%04d" % (i + 1), line, file = file)
            if printRemarks(i + lineOffset):
                print("")
        
        print("\n", file = file)
        printRemarks(self.FINAL)
        
                    
                    
          
    def count(self):
        errors = warnings = 0
        for lineMsg in self.messages.values():
            errors      += len(lineMsg.get(ERROR,   []))
            warnings    += len(lineMsg.get(WARNING, []))
        
        return errors, warnings
    
        
                
if __name__ == '__main__':
                        
    l = Lister()
    l.start()        
    l.addWarning("started", 19, "test")
    l.addError("error", 25, "test")
    l.addWarning("warning", 25, "test")
    
    print(l.messages)
    s = sys.modules[__name__]
    import inspect
    l.report(inspect.getsource(s))
    print(l.count())