import ast
import sys
from pathlib import Path

from lib.smallUtilities import flatten
from csmp.precompiler.lister import Lister
from csmp.precompiler.segment import SegmentLabel
from csmp.precompiler.statementBase import StatementCategory
from csmp.precompiler.template import TemplateBuilder
import itertools


class PrecompilerOutput:
    
    def __init__(self, path, options):
        self.options = options
        self.path = Path(path)
    
    
    def writeToFile(self, file: str | Path, *args, **kwargs):
        fileName = self.path / file
        with fileName.open("w") as f:
            self.write(f, *args, **kwargs)
        print(f"created file {fileName}")
    
    
    def writeToConsole(self, *args, **kwargs):
        self.write(sys.stdout, *args, **kwargs)
    
    
    def write(self, file, *args, **kwargs):
        ...

    
class WriteListfile(PrecompilerOutput):
    
    @Lister.withContextError
    def write(self, file, loader, summary = False):
        Lister().report(loader.getSource(), file = file, onlyMarkedLines = summary)
        print("%8d error(s)\n%8d warning(s)" % Lister().count(), file = file)
        
        
        
class WriteSummary(WriteListfile):
        
    def _getConstantValues(self, constants):
        '''
        Evaluate the hard-defined values of constants, parameters and incons.
        :return: dict
        '''
        constants = self.consts + self.params + self.incons
        tmpSource = "def dummy(): ...\n" + "\n".join([s.toString() for s in constants])
        result    = {}
        exec(tmpSource, locals = result)
        return result 
            
        
    def writeSummary(self, file, loader, constants):
        modelFileName       = self.loader.file
        errors, warnings    = self.results
        completed           = "succesfully completed" if self.succes else "failed"
        stateVars           = ", ".join([v.name for v in sorted(self.states, key = lambda n: n.name)])
        
        print("\n\n", file = file)
        print(f"Parsing of {modelFileName} {completed} with {errors} error(s) and {warnings} warning(s).\n", file = file)
        print(f"state variables: {stateVars}\n", file = file)
        
        consts = self._getConstantValues(itertools.chain(constants))
        format = lambda coll: ([" %-8s = %-12s " % (k.name, consts.get(k.name, -99999)) for k in sorted(coll, key = lambda n: n.name)])
        items  = tuple([format(c) for c in constants])
        
        print("   %-22s "*3 % ("CONST", "PARAM", "INCON"), file = file)
        for values in itertools.zip_longest(*items, fillvalue = " "*25):
            print(*values, file = file)
            
        super().write(file, loader, True)
        print("\n\n", file = file)
                
            
    
class WriteRunnable(PrecompilerOutput):
    
    @Lister.withContextError
    def write(self, file, segments, statements):
        
        def common():
            variables = segments[SegmentLabel.INITIAL].getAssignments()
            s = "global %s" % ", ".join(variables) if variables else "# (nothing to do)" 
            node = ast.parse(s)
            return [node.body[0]] if node.body else []

        template    = Path(self.options.template)
        comment     = self.options.templateComment
        placeHolder = self.options.templatePlcHldr
        builder     = TemplateBuilder(template, segmentComment = comment, placeholders = placeHolder)
        
        builder.replace(StatementCategory.common, common())
        builder.replace(StatementCategory.initial,    [w.node for w in segments.initial.getItems()],  False)
        builder.replace(StatementCategory.dynamic,    [w.node for w in segments.dynamic.getItems()],  False)
        builder.replace(StatementCategory.terminal,   [w.node for w in segments.terminal.getItems()], False)

        for cat in StatementCategory: # this loops through _all_ cats and destroys any remaining placeholders
            items       = statements[cat]
            transformed = flatten([item.transform(cat) for item in items])
            builder.replace(cat, transformed, True)

        builder.write(file)

        

        
        