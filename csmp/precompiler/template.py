import inspect
import itertools
from io import StringIO
from pathlib import Path

import lib.ast_comments as ast
from csmp import errors


class TemplateBuilder(ast.NodeTransformer):

    def __init__(self, template, segmentComment = None, placeholders = None):
        ''' turn a generic model template with placeholder labels into valid source code.
        :param template:
        '''

        if isinstance(template, type):
            source      = inspect.getsource(template)
            self.code   = ast.parse(source)
            
        elif isinstance(template, Path):
            self.code   = self.loadTemplatefile(template)
            
        elif isinstance(template, str):
            self.code   = self.loadString(template)
            
        else:
            raise errors.ProgramError("unsupported template of type '%s'" % (type(template).__name__))
        
        self.segmentComment = segmentComment if segmentComment is not None else "--- {0}: ----------" 
        self.placeholders   = placeholders   if placeholders   is not None else ":{0}:"
        # change name of class in template
        self.code.body[0].name  = self.code.body[0].name.replace("Template", "")
        
        
    
    def replace(self, label, items: list, keepLabel = True):
        # items = itertools.chain(items)
        subst = items.body if isinstance(items, ast.Module) else items             
        
        cmt = "# " + self.segmentComment.format(label.value)
        tag = self.placeholders.format(label.name)
        
        def comment(node):
            result = [ast.Comment(value = "",  inline = False)] # blank line (works!)
            if keepLabel:
                result.append(ast.Comment(value = cmt, inline = False))
            for node in result: 
                ast.copy_location(result[0], node)
            return result

            
        def replaceBranch(node):
            if isinstance(node.value, ast.Constant) and (node.value.value == tag):
                items = comment(node)
                for stmt in subst:
                    items.append(ast.copy_location(stmt, node))
                return items
                
            else:
                return node
        
        self.visit_Expr = replaceBranch
        self.visit(self.code)
        ast.fix_missing_locations(self.code)

        
    def write(self, file):
        print(ast.unparse(self.code), file = file)

        
    def toString(self):
        ss = StringIO()
        self.write(ss)
        return ss.getvalue()

    

    def loadTemplatefile(self, template: Path):
        with template.open("r") as t:
            return self.loadString(t.read())
        
            
    def loadString(self, source):
        matches = []
        try:
            tree = ast.parse(source)
        except SyntaxError as e:
            if Path(source).exists():
                raise errors.ProgramError(f"{source} appears to be a path but was passed as string")
            else:
                raise errors.PrecompilerError.fromSyntaxError(e, "syntax error in template")
            
        except Exception as e:
            raise errors.PrecompilerError(e.args)
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                parentage = [b.id == "CSMP_Model" for b in node.bases]
                if any(parentage):
                    matches.append(node)
                
        if len(matches) == 1:
            return matches[0]
        
        raise errors.PrecompilerError("template must contain exactly one model class (direct descendant of CSMP_Model)")

    # # extra prox to run the created program TODO: NYUsed
    # def getClass(self, **compilerArgs):    
    #     obj = compile(self.code, filename="<ast>", mode="exec", **compilerArgs)
    #     namespace = {}
    #     exec(obj, namespace)
    #     return namespace[self.template.__name__]
    #
    #
    # def getObject(self, *args, **kwargs):
    #     c = self.getClass()
    #     return c(*args, **kwargs)




        
        
if __name__ == '__main__':
    import sys
    # from templates.simulationModelTemplate import SimulationModelTemplate
    from csmp.precompiler.keywordsBase import KeywordLabels
    from pathlib import Path
    
    # tpl     = SimulationModelTemplate
    tpl     = Path("../../templates/simulationModelTemplate.py")
    src     = "a = 1\nb = 2\nc = 'character'\n"
    subst   = ast.parse(src)
    b       = TemplateBuilder(tpl, segmentComment=" ### {} ###")
    b.replace(KeywordLabels.parameters, subst, keepLabel=True)
    b.write(sys.stdout)

    
    
    